import sqlite3
import logging
import struct
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationStore:
    """
    SQLite + FTS5  (structured storage, keyword search)
    SQLite BLOB    (vector storage — semantic search via Voyage AI + numpy)

    Si voyage_api_key es None, search_relevant() usa FTS5.
    Si está configurado, guarda embeddings en SQLite y usa coseno con numpy.
    numpy y voyageai se importan en tiempo de ejecución (no en import time).
    """

    def __init__(self, store_path: str, voyage_api_key: str | None = None):
        self._db = Path(store_path) / "conversations.db"
        Path(store_path).mkdir(parents=True, exist_ok=True)
        self._init_db()

        self._vo = None

        if voyage_api_key:
            try:
                import voyageai
                self._vo = voyageai.Client(api_key=voyage_api_key)
                logger.info("[ConversationStore] Semantic search activo (Voyage AI + SQLite)")
            except ImportError:
                logger.warning("[ConversationStore] voyageai no disponible. Usando FTS5.")
            except Exception as e:
                logger.warning(f"[ConversationStore] Error iniciando Voyage AI: {e}. Usando FTS5.")

    # ── connection ────────────────────────────────────────────────────

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(str(self._db), check_same_thread=False, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self._conn() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS turns (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id  INTEGER NOT NULL,
                    ts       TEXT    NOT NULL,
                    user_msg TEXT    NOT NULL,
                    bot_resp TEXT    NOT NULL,
                    itype    TEXT    DEFAULT 'text'
                );
                CREATE INDEX IF NOT EXISTS idx_turns_cid_ts ON turns(chat_id, ts);
                CREATE INDEX IF NOT EXISTS idx_turns_ts     ON turns(ts);

                CREATE VIRTUAL TABLE IF NOT EXISTS turns_fts USING fts5(
                    user_msg,
                    bot_resp,
                    ts      UNINDEXED,
                    chat_id UNINDEXED,
                    tokenize = "unicode61 remove_diacritics 0"
                );

                CREATE TABLE IF NOT EXISTS embeddings (
                    turn_id   INTEGER PRIMARY KEY REFERENCES turns(id) ON DELETE CASCADE,
                    ts        TEXT NOT NULL,
                    chat_id   INTEGER NOT NULL,
                    vector    BLOB NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_emb_ts ON embeddings(ts);

                CREATE TABLE IF NOT EXISTS summaries (
                    ptype TEXT NOT NULL,
                    pkey  TEXT NOT NULL,
                    body  TEXT NOT NULL,
                    ts    TEXT NOT NULL,
                    PRIMARY KEY (ptype, pkey)
                );
            """)

    # ── serialisation ─────────────────────────────────────────────────

    @staticmethod
    def _vec_to_blob(vec: list[float]) -> bytes:
        return struct.pack(f"{len(vec)}f", *vec)

    @staticmethod
    def _blob_to_vec(blob: bytes) -> list[float]:
        n = len(blob) // 4
        return list(struct.unpack(f"{n}f", blob))

    # ── writes ────────────────────────────────────────────────────────

    def add_turn(self, chat_id: int, user_msg: str, bot_resp: str, itype: str = "text"):
        ts = datetime.now().isoformat(timespec="seconds")

        # 1. SQLite + FTS5 (siempre)
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO turns(chat_id,ts,user_msg,bot_resp,itype) VALUES(?,?,?,?,?)",
                (chat_id, ts, user_msg, bot_resp, itype),
            )
            turn_id = cur.lastrowid
            c.execute(
                "INSERT INTO turns_fts(user_msg,bot_resp,ts,chat_id) VALUES(?,?,?,?)",
                (user_msg, bot_resp, ts, str(chat_id)),
            )

        # 2. Embedding en SQLite (si Voyage AI disponible)
        if self._vo:
            try:
                doc = f"Usuario: {user_msg[:600]}\nCoach: {bot_resp[:800]}"
                result = self._vo.embed([doc], model="voyage-3-lite", input_type="document")
                blob = self._vec_to_blob(result.embeddings[0])
                with self._conn() as c:
                    c.execute(
                        "INSERT OR IGNORE INTO embeddings(turn_id,ts,chat_id,vector) VALUES(?,?,?,?)",
                        (turn_id, ts, chat_id, blob),
                    )
            except Exception as e:
                logger.warning(f"[ConversationStore] Embed falló (datos en FTS5): {e}")

    def save_summary(self, ptype: str, pkey: str, body: str):
        ts = datetime.now().isoformat(timespec="seconds")
        with self._conn() as c:
            c.execute(
                "INSERT INTO summaries(ptype,pkey,body,ts) VALUES(?,?,?,?) "
                "ON CONFLICT(ptype,pkey) DO UPDATE SET body=excluded.body, ts=excluded.ts",
                (ptype, pkey, body, ts),
            )

    def purge_old_raw(self, days: int = 365):
        cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
        with self._conn() as c:
            c.execute("DELETE FROM embeddings WHERE ts < ?", (cutoff,))
            c.execute("DELETE FROM turns_fts WHERE ts < ?", (cutoff,))
            c.execute("DELETE FROM turns WHERE ts < ?", (cutoff,))
        logger.info(f"[ConversationStore] Purged raw turns older than {days} days")

    # ── reads ─────────────────────────────────────────────────────────

    def get_recent(self, chat_id: int, hours: int = 48) -> list[dict]:
        since = (datetime.now() - timedelta(hours=hours)).isoformat(timespec="seconds")
        with self._conn() as c:
            rows = c.execute(
                "SELECT ts,user_msg,bot_resp FROM turns "
                "WHERE chat_id=? AND ts>=? ORDER BY ts ASC",
                (chat_id, since),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_turns_for_date(self, date_str: str) -> list[dict]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT ts,user_msg,bot_resp FROM turns "
                "WHERE ts LIKE ? ORDER BY ts ASC",
                (f"{date_str}%",),
            ).fetchall()
        return [dict(r) for r in rows]

    def search_relevant(self, query: str, n: int = 4, days_back: int = 365) -> list[dict]:
        """Semántico si Voyage AI está activo; FTS5 como fallback."""
        if self._vo:
            return self._search_semantic(query, n, days_back)
        return self._search_fts(query, n, days_back)

    def get_recent_summaries(self, ptype: str, n: int) -> list[dict]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT pkey,body FROM summaries WHERE ptype=? ORDER BY pkey DESC LIMIT ?",
                (ptype, n),
            ).fetchall()
        return [dict(r) for r in reversed(rows)]

    def summary_exists(self, ptype: str, pkey: str) -> bool:
        with self._conn() as c:
            row = c.execute(
                "SELECT 1 FROM summaries WHERE ptype=? AND pkey=?",
                (ptype, pkey),
            ).fetchone()
        return row is not None

    # ── semantic search ───────────────────────────────────────────────

    def _search_semantic(self, query: str, n: int, days_back: int) -> list[dict]:
        since = (datetime.now() - timedelta(days=days_back)).isoformat(timespec="seconds")
        today = datetime.now().date().isoformat()

        try:
            import numpy as np

            # Embedding de la query
            q_emb = self._vo.embed([query], model="voyage-3-lite", input_type="query")
            q_vec = np.array(q_emb.embeddings[0], dtype=np.float32)
            q_norm = q_vec / (np.linalg.norm(q_vec) + 1e-10)

            # Cargar candidatos del rango de fechas (excluye hoy)
            with self._conn() as c:
                rows = c.execute(
                    "SELECT e.ts, e.vector, t.user_msg, t.bot_resp "
                    "FROM embeddings e JOIN turns t ON t.id = e.turn_id "
                    "WHERE e.ts >= ? AND e.ts NOT LIKE ? "
                    "ORDER BY e.ts DESC LIMIT 500",
                    (since, f"{today}%"),
                ).fetchall()

            if not rows:
                return self._search_fts(query, n, days_back)

            # Calcular similitud de coseno con numpy (vectorizado)
            blobs  = [self._blob_to_vec(r["vector"]) for r in rows]
            matrix = np.array(blobs, dtype=np.float32)
            norms  = np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10
            scores = (matrix / norms) @ q_norm

            # Top-N por score
            top_idx = np.argsort(scores)[::-1][:n]
            return [
                {
                    "ts":       rows[i]["ts"],
                    "user_msg": rows[i]["user_msg"],
                    "bot_resp": rows[i]["bot_resp"],
                }
                for i in top_idx
            ]

        except Exception as e:
            logger.warning(f"[ConversationStore] Semantic search falló, usando FTS5: {e}")
            return self._search_fts(query, n, days_back)

    # ── keyword search (fallback) ─────────────────────────────────────

    def _search_fts(self, query: str, n: int, days_back: int) -> list[dict]:
        fts_q = self._fts_query(query)
        if not fts_q:
            return []
        since = (datetime.now() - timedelta(days=days_back)).isoformat(timespec="seconds")
        today = datetime.now().date().isoformat()
        try:
            with self._conn() as c:
                rows = c.execute(
                    "SELECT ts,user_msg,bot_resp FROM turns_fts "
                    "WHERE turns_fts MATCH ? AND ts>=? AND ts NOT LIKE ? "
                    "ORDER BY rank LIMIT ?",
                    (fts_q, since, f"{today}%", n),
                ).fetchall()
            return [dict(r) for r in rows]
        except sqlite3.OperationalError as e:
            logger.warning(f"[ConversationStore] FTS query falló ({fts_q!r}): {e}")
            return []

    @staticmethod
    def _fts_query(text: str) -> str:
        strip_chars = '.,;:!?¿¡"\'/\\()[]{}*+-=<>'
        words = [
            w.strip(strip_chars)
            for w in text.split()
            if len(w.strip(strip_chars)) > 3
        ][:10]
        if not words:
            return ""
        return " OR ".join(f'"{w}"' for w in words)
