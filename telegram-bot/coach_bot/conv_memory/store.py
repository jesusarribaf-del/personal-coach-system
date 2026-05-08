import sqlite3
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationStore:
    """
    SQLite + FTS5  (structured storage, keyword fallback)
    ChromaDB       (vector index — semantic search, optional)
    Voyage AI      (embedding model, optional — activates ChromaDB path)

    Si voyage_api_key es None, el sistema funciona igual usando FTS5.
    Si está configurado, search_relevant() usa búsqueda semántica con
    FTS5 como fallback automático en caso de error de red o API.
    """

    def __init__(self, store_path: str, voyage_api_key: str | None = None):
        self._db = Path(store_path) / "conversations.db"
        Path(store_path).mkdir(parents=True, exist_ok=True)
        self._init_db()

        self._vo  = None
        self._col = None

        if voyage_api_key:
            try:
                import voyageai
                import chromadb
                self._vo = voyageai.Client(api_key=voyage_api_key)
                chroma   = chromadb.PersistentClient(
                    path=str(Path(store_path) / "chroma")
                )
                self._col = chroma.get_or_create_collection(
                    name="turns",
                    metadata={"hnsw:space": "cosine"},
                )
                logger.info("[ConversationStore] Semantic search activo (Voyage AI + ChromaDB)")
            except ImportError as e:
                logger.warning(f"[ConversationStore] chromadb/voyageai no disponible: {e}. Usando FTS5.")
            except Exception as e:
                logger.warning(f"[ConversationStore] Error iniciando ChromaDB: {e}. Usando FTS5.")

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

                CREATE TABLE IF NOT EXISTS summaries (
                    ptype TEXT NOT NULL,
                    pkey  TEXT NOT NULL,
                    body  TEXT NOT NULL,
                    ts    TEXT NOT NULL,
                    PRIMARY KEY (ptype, pkey)
                );
            """)

    # ── writes ────────────────────────────────────────────────────────

    def add_turn(self, chat_id: int, user_msg: str, bot_resp: str, itype: str = "text"):
        ts     = datetime.now().isoformat(timespec="seconds")
        doc_id = f"{ts}_{chat_id}"

        # 1. SQLite + FTS5 (siempre)
        with self._conn() as c:
            c.execute(
                "INSERT INTO turns(chat_id,ts,user_msg,bot_resp,itype) VALUES(?,?,?,?,?)",
                (chat_id, ts, user_msg, bot_resp, itype),
            )
            c.execute(
                "INSERT INTO turns_fts(user_msg,bot_resp,ts,chat_id) VALUES(?,?,?,?)",
                (user_msg, bot_resp, ts, str(chat_id)),
            )

        # 2. ChromaDB via Voyage AI (si está configurado)
        if self._vo and self._col is not None:
            try:
                doc    = f"Usuario: {user_msg[:600]}\nCoach: {bot_resp[:800]}"
                result = self._vo.embed(
                    [doc],
                    model="voyage-3-lite",
                    input_type="document",
                )
                self._col.add(
                    ids=[doc_id],
                    embeddings=[result.embeddings[0]],
                    metadatas=[{"chat_id": str(chat_id), "ts": ts}],
                    documents=[doc],
                )
            except Exception as e:
                logger.warning(f"[ConversationStore] ChromaDB embed falló (datos en FTS5): {e}")

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

        # ChromaDB: borrar vectores antiguos
        if self._col is not None:
            try:
                self._col.delete(where={"ts": {"$lt": cutoff}})
            except Exception as e:
                logger.warning(f"[ConversationStore] ChromaDB purge falló: {e}")

        # SQLite: borrar turns + FTS index
        with self._conn() as c:
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
        if self._vo and self._col is not None:
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
        total = self._col.count()
        if total == 0:
            return []

        since = (datetime.now() - timedelta(days=days_back)).isoformat(timespec="seconds")
        today = datetime.now().date().isoformat()

        try:
            emb = self._vo.embed(
                [query],
                model="voyage-3-lite",
                input_type="query",
            ).embeddings[0]

            # Traer más resultados de los necesarios y filtrar por fecha en Python
            # (más robusto que depender de where filters de ChromaDB)
            fetch_n = min(n * 4, total)
            raw     = self._col.query(
                query_embeddings=[emb],
                n_results=fetch_n,
                include=["metadatas", "documents"],
            )

            out: list[dict] = []
            for meta, doc in zip(raw["metadatas"][0], raw["documents"][0]):
                ts = meta.get("ts", "")
                if ts < since or ts.startswith(today):
                    continue
                # Reconstruir user_msg y bot_resp desde el documento almacenado
                parts    = doc.split("\nCoach: ", 1)
                user_msg = parts[0].replace("Usuario: ", "", 1) if parts else doc
                bot_resp = parts[1] if len(parts) > 1 else ""
                out.append({"ts": ts, "user_msg": user_msg, "bot_resp": bot_resp})
                if len(out) >= n:
                    break

            return out

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
