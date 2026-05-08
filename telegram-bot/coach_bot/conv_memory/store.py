import sqlite3
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationStore:
    """
    SQLite + FTS5 store for conversation history.
    Rolling 365-day window on raw turns; summaries kept indefinitely.
    """

    def __init__(self, store_path: str):
        self._db = Path(store_path) / "conversations.db"
        Path(store_path).mkdir(parents=True, exist_ok=True)
        self._init_db()

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
        ts = datetime.now().isoformat(timespec="seconds")
        with self._conn() as c:
            c.execute(
                "INSERT INTO turns(chat_id,ts,user_msg,bot_resp,itype) VALUES(?,?,?,?,?)",
                (chat_id, ts, user_msg, bot_resp, itype),
            )
            c.execute(
                "INSERT INTO turns_fts(user_msg,bot_resp,ts,chat_id) VALUES(?,?,?,?)",
                (user_msg, bot_resp, ts, str(chat_id)),
            )

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
            logger.warning(f"[ConversationStore] FTS query failed ({fts_q!r}): {e}")
            return []

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

    # ── helpers ───────────────────────────────────────────────────────

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
        # Wrap each word in double quotes for exact-token match in FTS5
        return " OR ".join(f'"{w}"' for w in words)
