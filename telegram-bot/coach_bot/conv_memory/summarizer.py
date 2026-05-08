import asyncio
import logging
from datetime import datetime, timedelta
from anthropic import Anthropic
from .store import ConversationStore

logger = logging.getLogger(__name__)
_MODEL = "claude-haiku-4-5-20251001"


class MemorySummarizer:
    """
    Generates and persists daily + weekly summaries from raw conversation turns.
    Summaries are kept indefinitely; only raw turns rotate after 365 days.
    """

    def __init__(self, store: ConversationStore, api_key: str):
        self.store = store
        self.client = Anthropic(api_key=api_key)

    # ── public interface ──────────────────────────────────────────────

    async def run_daily_jobs(self):
        """Call this once per day (e.g., at 02:00). Idempotent."""
        await self.maybe_summarize_yesterday()
        await self.maybe_summarize_last_week()
        self.store.purge_old_raw(days=365)

    async def maybe_summarize_yesterday(self):
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        if self.store.summary_exists("daily", yesterday):
            return
        turns = self.store.get_turns_for_date(yesterday)
        if not turns:
            return
        await self._create_daily_summary(yesterday, turns)

    async def maybe_summarize_last_week(self):
        today = datetime.now()
        if today.weekday() != 0:  # only Mondays
            return
        last_week = today - timedelta(days=7)
        lw = last_week.isocalendar()
        pkey = f"{lw[0]}-W{lw[1]:02d}"
        if self.store.summary_exists("weekly", pkey):
            return
        dailies = self.store.get_recent_summaries("daily", 7)
        week_dailies = [
            d for d in dailies
            if self._same_week(d["pkey"], last_week)
        ]
        if not week_dailies:
            return
        await self._create_weekly_summary(pkey, week_dailies)

    # ── internal ──────────────────────────────────────────────────────

    async def _create_daily_summary(self, date: str, turns: list[dict]):
        text = "\n---\n".join(
            f"Tú: {t['user_msg'][:300]}\nCoach: {t['bot_resp'][:400]}"
            for t in turns[:20]
        )
        prompt = (
            f"Resume en 4-6 bullets concisos los temas clave de estas conversaciones del {date}. "
            "Incluye con números exactos: entrenamientos realizados y marcas, datos de VFC/sueño, "
            "decisiones importantes, actualizaciones de perfil, estado notable. "
            "Sé muy específico. Sin preámbulos.\n\n"
            f"{text[:3500]}"
        )
        try:
            loop = asyncio.get_running_loop()
            resp = await loop.run_in_executor(
                None,
                lambda: self.client.messages.create(
                    model=_MODEL,
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}],
                ),
            )
            self.store.save_summary("daily", date, resp.content[0].text.strip())
            logger.info(f"[Summarizer] Daily summary saved for {date}")
        except Exception as e:
            logger.error(f"[Summarizer] Daily summary failed for {date}: {e}")

    async def _create_weekly_summary(self, pkey: str, dailies: list[dict]):
        text = "\n".join(f"{d['pkey']}: {d['body']}" for d in dailies)
        prompt = (
            f"Resume en 6-8 bullets la semana {pkey}. "
            "Sintetiza: progresión de fuerza (con números), tendencia VFC, adherencia nutricional, "
            "hábitos y adherencia protocolo Allen Carr si aplica, eventos clave. "
            "Sin preámbulos.\n\n"
            f"{text[:2500]}"
        )
        try:
            loop = asyncio.get_running_loop()
            resp = await loop.run_in_executor(
                None,
                lambda: self.client.messages.create(
                    model=_MODEL,
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}],
                ),
            )
            self.store.save_summary("weekly", pkey, resp.content[0].text.strip())
            logger.info(f"[Summarizer] Weekly summary saved for {pkey}")
        except Exception as e:
            logger.error(f"[Summarizer] Weekly summary failed for {pkey}: {e}")

    @staticmethod
    def _same_week(date_str: str, ref: datetime) -> bool:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            return d.isocalendar()[:2] == ref.isocalendar()[:2]
        except ValueError:
            return False
