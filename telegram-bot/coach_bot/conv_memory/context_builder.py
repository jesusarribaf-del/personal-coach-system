from datetime import datetime
from .store import ConversationStore

# Context budget limits (characters, not tokens)
_MAX_RECENT_TURNS   = 10
_MAX_DAILY_SUMS     = 5
_MAX_WEEKLY_SUMS    = 4
_MAX_RELEVANT       = 4
_LEN_USER           = 250
_LEN_BOT            = 350
_LEN_DAILY          = 280
_LEN_WEEKLY         = 380


class ContextBuilder:
    """Assembles conversation history context for agent prompts."""

    def __init__(self, store: ConversationStore):
        self.store = store

    def build(self, chat_id: int, query: str) -> str:
        parts: list[str] = []

        # ① Raw turns: today + yesterday ─────────────────────────────
        recent = self.store.get_recent(chat_id, hours=48)[-_MAX_RECENT_TURNS:]
        if recent:
            today = datetime.now().date().isoformat()
            today_turns  = [r for r in recent if r["ts"].startswith(today)]
            yest_turns   = [r for r in recent if not r["ts"].startswith(today)]

            if today_turns:
                parts.append("### Hoy")
                for t in today_turns:
                    hm = t["ts"][11:16]
                    parts.append(f"[{hm}] Tú: {t['user_msg'][:_LEN_USER]}")
                    parts.append(f"[{hm}] Coach: {t['bot_resp'][:_LEN_BOT]}")

            if yest_turns:
                parts.append("### Ayer")
                for t in yest_turns[-4:]:
                    hm = t["ts"][:10] + " " + t["ts"][11:16]
                    parts.append(f"[{hm}] Tú: {t['user_msg'][:_LEN_USER]}")
                    parts.append(f"[{hm}] Coach: {t['bot_resp'][:_LEN_BOT]}")

        # ② Daily summaries (last 5 days) ─────────────────────────────
        daily = self.store.get_recent_summaries("daily", _MAX_DAILY_SUMS)
        if daily:
            parts.append("\n### Últimos días (resumen)")
            for s in daily:
                parts.append(f"**{s['pkey']}**: {s['body'][:_LEN_DAILY]}")

        # ③ Weekly summaries (last 4 weeks) ───────────────────────────
        weekly = self.store.get_recent_summaries("weekly", _MAX_WEEKLY_SUMS)
        if weekly:
            parts.append("\n### Semanas recientes (resumen)")
            for s in weekly:
                parts.append(f"**{s['pkey']}**: {s['body'][:_LEN_WEEKLY]}")

        # ④ Semantically relevant past exchanges ──────────────────────
        relevant = self.store.search_relevant(query, n=_MAX_RELEVANT)
        if relevant:
            parts.append("\n### Conversaciones anteriores relevantes")
            for t in relevant:
                parts.append(f"[{t['ts'][:10]}] Tú: {t['user_msg'][:_LEN_USER]}")
                parts.append(f"[{t['ts'][:10]}] Coach: {t['bot_resp'][:_LEN_BOT]}")

        if not parts:
            return ""

        return "## HISTORIAL DE CONVERSACIONES\n" + "\n".join(parts) + "\n\n"
