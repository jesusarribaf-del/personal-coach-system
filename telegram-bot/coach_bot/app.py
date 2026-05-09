import asyncio
import importlib
import logging
import sys
import threading
from datetime import time
import appdaemon.plugins.hass.hassapi as hass

logger = logging.getLogger(__name__)

_COACH_BOT_SUBMODULES = [
    "coach_bot.bot_handlers",
    "coach_bot.synthesizer",
    "coach_bot.orchestrator",
    "coach_bot.memory_reader",
    "coach_bot.agents.base",
    "coach_bot.agents.sleep",
    "coach_bot.agents.strength",
    "coach_bot.agents.nutrition",
    "coach_bot.agents.meditation",
    "coach_bot.agents.decisions",
    "coach_bot.agents.motivation",
    "coach_bot.agents.productivity",
    "coach_bot.agents.identity",
    "coach_bot.agents.memory_curator",
    "coach_bot.agents.life_coworker",
    "coach_bot.agents.report_designer",
    "coach_bot.agents.addiction_coach",
]


def _reload_submodules():
    """Fuerza reimport de todos los submódulos en cada recarga de AppDaemon."""
    for mod in _COACH_BOT_SUBMODULES:
        if mod in sys.modules:
            try:
                importlib.reload(sys.modules[mod])
            except Exception:
                del sys.modules[mod]


class CoachBotApp(hass.Hass):
    """AppDaemon entry point. Runs the Telegram bot in a daemon thread with its own event loop."""

    def initialize(self):
        _reload_submodules()
        self.bot_token = self.args["bot_token"]
        self.api_key = self.args["anthropic_api_key"]
        self.repo_path = self.args["repo_path"]
        self.authorized_chat_id = int(self.args["authorized_chat_id"])
        self.store_path = self.args.get("store_path", "/config/coach_bot_staging/conv_store")
        self.voyage_api_key = self.args.get("voyage_api_key")
        self._shutdown_event = None
        self._bot_app = None

        self.log("CoachBot: iniciando...")
        self._bot_thread = threading.Thread(target=self._run_bot, daemon=True, name="coach-bot")
        self._bot_thread.start()

        self.run_daily(self._trigger_daily_jobs, time(2, 0, 0))

    def terminate(self):
        """AppDaemon llama esto al detener/recargar la app. Cierra el bot limpiamente."""
        self.log("CoachBot: cerrando bot...")
        loop = getattr(self, "_bot_loop", None)
        event = getattr(self, "_shutdown_event", None)
        if loop and loop.is_running() and event is not None:
            loop.call_soon_threadsafe(event.set)
        if hasattr(self, "_bot_thread") and self._bot_thread.is_alive():
            self._bot_thread.join(timeout=10)
        self.log("CoachBot: bot cerrado.")

    def _trigger_daily_jobs(self, kwargs):
        if hasattr(self, "_summarizer") and self._summarizer:
            loop = getattr(self, "_bot_loop", None)
            if loop and loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    self._summarizer.run_daily_jobs(), loop
                )

    def _run_bot(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._bot_loop = loop
        try:
            loop.run_until_complete(self._start_telegram())
        except Exception as e:
            self.log(f"CoachBot ERROR: {e}", level="ERROR")
        finally:
            loop.close()

    async def _start_telegram(self):
        from telegram.ext import Application, MessageHandler, CommandHandler, filters
        from coach_bot.bot_handlers import BotHandlers
        from coach_bot.conv_memory import ConversationStore, ContextBuilder, MemorySummarizer

        store = ConversationStore(self.store_path, voyage_api_key=self.voyage_api_key)
        ctx_builder = ContextBuilder(store)
        self._summarizer = MemorySummarizer(store, self.api_key)

        handlers = BotHandlers(
            self.repo_path,
            self.api_key,
            self.authorized_chat_id,
            store=store,
            context_builder=ctx_builder,
        )

        self._bot_app = Application.builder().token(self.bot_token).build()
        app = self._bot_app
        self._shutdown_event = asyncio.Event()

        app.add_handler(CommandHandler("start", handlers.cmd_start))
        app.add_handler(CommandHandler("agentes", handlers.cmd_agentes))
        app.add_handler(CommandHandler("memoria", handlers.cmd_memoria))
        app.add_handler(CommandHandler("actualizar", handlers.cmd_actualizar))
        app.add_handler(CommandHandler("reporte", handlers.cmd_reporte))
        app.add_handler(
            MessageHandler(filters.TEXT | filters.PHOTO, handlers.handle_message)
        )

        self.log("CoachBot: bot iniciado, escuchando Telegram...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        await self._shutdown_event.wait()
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
