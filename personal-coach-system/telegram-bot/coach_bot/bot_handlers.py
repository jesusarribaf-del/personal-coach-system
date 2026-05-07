import asyncio
import base64
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from coach_bot.orchestrator import Orchestrator, InputType
from coach_bot.synthesizer import synthesize
from coach_bot.agents.sleep import SleepCoach
from coach_bot.agents.strength import StrengthCoach
from coach_bot.agents.nutrition import NutritionCoach
from coach_bot.agents.meditation import MeditationGuide
from coach_bot.agents.decisions import DecisionAdvisor
from coach_bot.agents.motivation import MotivationCoach
from coach_bot.agents.productivity import ProductivityBuilder
from coach_bot.agents.identity import IdentityCoach
from coach_bot.agents.memory_curator import MemoryCurator
from coach_bot.agents.life_coworker import LifeCoworker

logger = logging.getLogger(__name__)

AGENT_LABELS = {
    "sleep": ("💤", "Descanso"),
    "strength": ("🏋️", "Entreno"),
    "nutrition": ("🥗", "Nutrición"),
    "meditation": ("🧘", "Meditación"),
    "decisions": ("🎯", "Decisión"),
    "motivation": ("🔥", "Disciplina"),
    "productivity": ("📋", "Productividad"),
    "identity": ("🌟", "Perspectiva"),
    "memory_curator": ("🗂️", "Memoria"),
    "life_coworker": ("🧠", "Coach"),
}


def build_agents(repo_path: str, api_key: str) -> dict:
    return {
        "sleep": SleepCoach(repo_path, api_key),
        "strength": StrengthCoach(repo_path, api_key),
        "nutrition": NutritionCoach(repo_path, api_key),
        "meditation": MeditationGuide(repo_path, api_key),
        "decisions": DecisionAdvisor(repo_path, api_key),
        "motivation": MotivationCoach(repo_path, api_key),
        "productivity": ProductivityBuilder(repo_path, api_key),
        "identity": IdentityCoach(repo_path, api_key),
        "memory_curator": MemoryCurator(repo_path, api_key),
        "life_coworker": LifeCoworker(repo_path, api_key),
    }


class BotHandlers:
    def __init__(self, repo_path: str, api_key: str, authorized_chat_id: int):
        self.orchestrator = Orchestrator()
        self.agents = build_agents(repo_path, api_key)
        self.authorized_chat_id = authorized_chat_id
        self.repo_path = repo_path
        self._pending_memory: dict[int, dict] = {}

    def _is_authorized(self, update: Update) -> bool:
        return update.effective_chat.id == self.authorized_chat_id

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return

        message = update.message
        await context.bot.send_chat_action(chat_id=message.chat_id, action="typing")

        msg_context = {"text": message.text or message.caption or ""}

        if message.photo:
            photo = message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            photo_bytes = await file.download_as_bytearray()
            msg_context["image_base64"] = base64.b64encode(photo_bytes).decode()
            msg_context["image_media_type"] = "image/jpeg"

        input_type = self.orchestrator.classify(message)
        msg_context["input_type"] = input_type.value

        primary_key = self.orchestrator.get_primary_key(input_type)
        secondary_keys = self.orchestrator.get_secondary_keys(input_type)

        primary_agent = self.agents[primary_key]
        primary_emoji, primary_label_name = AGENT_LABELS[primary_key]
        primary_label = f"{primary_emoji} {primary_label_name}"

        secondary_tasks = [
            (k, self.agents[k].analyze(msg_context, full=False))
            for k in secondary_keys
            if k in self.agents
        ]

        primary_result, *sec_results = await asyncio.gather(
            primary_agent.analyze(msg_context, full=True),
            *[t[1] for t in secondary_tasks],
            return_exceptions=True,
        )

        secondary_labeled = []
        for i, (key, _) in enumerate(secondary_tasks):
            result = sec_results[i]
            if isinstance(result, str) and result.strip():
                emoji, name = AGENT_LABELS[key]
                secondary_labeled.append((f"{emoji} {name}", result))

        if isinstance(primary_result, Exception):
            primary_result = "Error al obtener análisis. Inténtalo de nuevo."

        response = synthesize(
            primary_text=primary_result,
            primary_label=primary_label,
            secondary_results=secondary_labeled,
        )

        await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return
        text = (
            "👋 *Personal Coach activo*\n\n"
            "Mándame una foto de AutoSleep, Jefit o Strava y te doy el análisis del día.\n"
            "También puedes escribirme directamente.\n\n"
            "*Comandos:*\n"
            "/agentes — agentes disponibles\n"
            "/memoria — resumen de tu perfil\n"
            "/actualizar — sincronizar memoria desde GitHub\n"
            "/reporte semanal — reporte semanal PDF (próximamente)\n"
        )
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    async def cmd_agentes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return
        lines = ["*Agentes activos:*\n"]
        for key, (emoji, name) in AGENT_LABELS.items():
            lines.append(f"{emoji} {name}")
        await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

    async def cmd_memoria(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return
        from coach_bot.memory_reader import MemoryReader
        reader = MemoryReader(self.repo_path)
        summary = reader.read_files(["personal-profile.md", "goals-roadmap.md"])
        await update.message.reply_text(
            f"🗂️ *Memoria actual:*\n\n{summary[:3000]}", parse_mode=ParseMode.MARKDOWN
        )

    async def cmd_actualizar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return
        import subprocess
        result = subprocess.run(
            ["git", "-C", "/config/personal-coach-system", "pull", "origin", "main"],
            capture_output=True, text=True
        )
        msg = "✅ Memoria sincronizada." if result.returncode == 0 else f"⚠️ Error: {result.stderr[:200]}"
        await update.message.reply_text(msg)
