import asyncio
import logging
import threading

logger = logging.getLogger(__name__)


class CoachBotApp:
    """AppDaemon entry point. Wraps the Telegram bot in a dedicated thread with its own event loop."""

    def initialize(self):
        import appdaemon.plugins.hass.hassapi as hass  # noqa: F401 — imported at runtime on RPi
        self.bot_token = self.args["bot_token"]
        self.api_key = self.args["anthropic_api_key"]
        self.repo_path = self.args["repo_path"]
        self.authorized_chat_id = int(self.args["authorized_chat_id"])

        self.log("CoachBot: iniciando...")
        self._bot_thread = threading.Thread(target=self._run_bot, daemon=True, name="coach-bot")
        self._bot_thread.start()

    def _run_bot(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._start_telegram())
        except Exception as e:
            self.log(f"CoachBot ERROR: {e}", level="ERROR")
        finally:
            loop.close()

    async def _start_telegram(self):
        from telegram.ext import Application, MessageHandler, CommandHandler, filters
        from coach_bot.bot_handlers import BotHandlers

        handlers = BotHandlers(self.repo_path, self.api_key, self.authorized_chat_id)

        app = Application.builder().token(self.bot_token).build()

        app.add_handler(CommandHandler("start", handlers.cmd_start))
        app.add_handler(CommandHandler("agentes", handlers.cmd_agentes))
        app.add_handler(CommandHandler("memoria", handlers.cmd_memoria))
        app.add_handler(CommandHandler("actualizar", handlers.cmd_actualizar))
        app.add_handler(
            MessageHandler(filters.TEXT | filters.PHOTO, handlers.handle_message)
        )

        self.log("CoachBot: bot iniciado, escuchando Telegram...")
        async with app:
            await app.initialize()
            await app.start()
            await app.updater.start_polling(drop_pending_updates=True)
            await asyncio.Event().wait()
