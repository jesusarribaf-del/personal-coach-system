import asyncio
import base64
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from coach_bot.orchestrator import Orchestrator
from coach_bot.synthesizer import synthesize_unified
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
from coach_bot.agents.report_designer import ReportDesigner
from coach_bot.agents.addiction_coach import AddictionCoach

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
    "report_designer": ("📊", "Reporte"),
    "addiction_coach": ("🕊️", "Allen Carr"),
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
        "report_designer": ReportDesigner(repo_path, api_key),
        "addiction_coach": AddictionCoach(repo_path, api_key),
    }


class BotHandlers:
    def __init__(
        self,
        repo_path: str,
        api_key: str,
        authorized_chat_id: int,
        store=None,
        context_builder=None,
    ):
        self.orchestrator = Orchestrator()
        self.agents = build_agents(repo_path, api_key)
        self.api_key = api_key
        self.authorized_chat_id = authorized_chat_id
        self.repo_path = repo_path
        self._pending_memory: dict[int, dict] = {}
        self._store = store
        self._ctx_builder = context_builder
        self._media_groups: dict[str, dict] = {}
        self._media_group_tasks: dict[str, asyncio.Task] = {}

    def _is_authorized(self, update: Update) -> bool:
        return update.effective_chat.id == self.authorized_chat_id

    def _extract_memory_proposal(self, text: str) -> dict | None:
        if "ACTUALIZAR MEMORIA" not in text and "ACTUALIZAR →" not in text:
            return None
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if "ACTUALIZAR" in line and "memory/" in line:
                file_part = [p for p in line.split() if "memory/" in p]
                if not file_part:
                    continue
                filename = file_part[0].replace("→", "").strip()
                content = "\n".join(lines[i + 1:]).strip()
                return {"file": filename, "content": content}
        return None

    async def _apply_memory_update(self, message, proposal: dict):
        import os
        import subprocess
        filepath = os.path.join(self.repo_path, proposal["file"])
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(f"\n\n{proposal['content']}")
            subprocess.run(
                ["git", "-C", self.repo_path, "add", proposal["file"]],
                capture_output=True
            )
            subprocess.run(
                ["git", "-C", self.repo_path, "commit", "-m",
                 f"memory: update {proposal['file']} via Telegram bot"],
                capture_output=True
            )
            subprocess.run(
                ["git", "-C", self.repo_path, "push", "origin", "main"],
                capture_output=True
            )
            await message.reply_text(
                f"✅ Memoria actualizada: `{proposal['file']}`",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            await message.reply_text(f"⚠️ Error al actualizar memoria: {e}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return

        message = update.message

        text_lower = (message.text or "").lower().strip()
        if message.chat_id in self._pending_memory and text_lower in ("sí", "si", "yes", "s", "y"):
            await self._apply_memory_update(message, self._pending_memory.pop(message.chat_id))
            return
        if message.chat_id in self._pending_memory and text_lower in ("no", "n"):
            self._pending_memory.pop(message.chat_id)
            await message.reply_text("❌ Propuesta descartada.")
            return

        if message.media_group_id:
            await self._buffer_media_group(message, context)
            return

        await context.bot.send_chat_action(chat_id=message.chat_id, action="typing")
        photos = [message.photo[-1]] if message.photo else []
        text = message.text or message.caption or ""
        await self._run_agents(message, context, photos=photos, text=text)

    async def _buffer_media_group(self, message, context):
        gid = message.media_group_id
        if gid not in self._media_groups:
            self._media_groups[gid] = {"first": message, "photos": [], "text": ""}
        grp = self._media_groups[gid]
        if message.photo:
            grp["photos"].append(message.photo[-1])
        if message.caption and not grp["text"]:
            grp["text"] = message.caption
        if gid in self._media_group_tasks:
            self._media_group_tasks[gid].cancel()
        self._media_group_tasks[gid] = asyncio.create_task(self._flush_group(gid, context))

    async def _flush_group(self, gid: str, context):
        try:
            await asyncio.sleep(1.5)
        except asyncio.CancelledError:
            return
        grp = self._media_groups.pop(gid, None)
        self._media_group_tasks.pop(gid, None)
        if not grp:
            return
        msg = grp["first"]
        await context.bot.send_chat_action(chat_id=msg.chat_id, action="typing")
        await self._run_agents(msg, context, photos=grp["photos"], text=grp["text"])

    async def _send_long(self, message, text: str, chunk: int = 4000):
        """Envía texto dividiéndolo si supera el límite de Telegram (4096 chars)."""
        if len(text) <= chunk:
            try:
                await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                await message.reply_text(text)
            return
        parts = []
        while text:
            if len(text) <= chunk:
                parts.append(text)
                break
            split_at = text.rfind("\n", 0, chunk)
            if split_at == -1:
                split_at = chunk
            parts.append(text[:split_at])
            text = text[split_at:].lstrip("\n")
        for part in parts:
            try:
                await message.reply_text(part, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                await message.reply_text(part)

    async def _run_agents(self, message, context, photos: list, text: str):
        msg_context = {"text": text}

        if self._ctx_builder and text:
            loop = asyncio.get_running_loop()
            msg_context["conv_context"] = await loop.run_in_executor(
                None, lambda: self._ctx_builder.build(message.chat_id, text)
            )

        if photos:
            images = []
            for photo in photos:
                file = await context.bot.get_file(photo.file_id)
                photo_bytes = await file.download_as_bytearray()
                images.append({
                    "base64": base64.b64encode(photo_bytes).decode(),
                    "media_type": "image/jpeg",
                })
            msg_context["images"] = images
            msg_context["image_base64"] = images[0]["base64"]
            msg_context["image_media_type"] = images[0]["media_type"]

        input_type = self.orchestrator.classify_from(text=text, has_photo=bool(photos))
        msg_context["input_type"] = input_type.value

        primary_key = self.orchestrator.get_primary_key(input_type)
        secondary_keys = self.orchestrator.get_secondary_keys(input_type, text=text)

        primary_agent = self.agents[primary_key]

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

        if isinstance(primary_result, BaseException):
            primary_result = "Error al obtener análisis. Inténtalo de nuevo."

        response = await synthesize_unified(self.api_key, primary_result, secondary_labeled)

        await self._send_long(message, response)

        if self._store:
            try:
                saved_text = primary_result if isinstance(primary_result, str) else response
                await asyncio.get_running_loop().run_in_executor(
                    None,
                    lambda: self._store.add_turn(
                        message.chat_id, text, saved_text, input_type.value
                    ),
                )
            except Exception as e:
                logger.warning(f"[BotHandlers] Could not save turn: {e}")

        memory_proposal = self._extract_memory_proposal(primary_result if isinstance(primary_result, str) else "")
        if memory_proposal:
            self._pending_memory[message.chat_id] = memory_proposal
            proposal_text = (
                f"\n\n📝 *Propuesta de memoria*\n"
                f"`{memory_proposal['file']}`\n"
                f"```\n{memory_proposal['content'][:400]}\n```\n"
                f"¿Confirmas? Responde *sí* o *no*"
            )
            try:
                await message.reply_text(proposal_text, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                await message.reply_text(proposal_text)

    async def cmd_reporte(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return
        message = update.message
        await context.bot.send_chat_action(chat_id=message.chat_id, action="typing")
        msg_context = {
            "text": message.text or "/reporte",
            "input_type": "report",
        }
        agent = self.agents["report_designer"]
        result = await agent.analyze(msg_context, full=True)
        try:
            await message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await message.reply_text(result)

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_authorized(update):
            return
        text = (
            "👋 *Personal Coach activo*\n\n"
            "Mándame una foto de AutoSleep, Jefit o Strava y te doy el análisis del día.\n"
            "También puedes escribirme directamente.\n\n"
            "*Comandos:*\n"
            "/agentes — ver todos los agentes\n"
            "/memoria — resumen de tu perfil\n"
            "/actualizar — sincronizar memoria desde GitHub\n"
            "/reporte — reporte completo\n"
            "/reporte semanal — resumen de la semana\n"
            "/reporte mensual — resumen del mes\n"
            "/reporte entreno — análisis de entrenamiento\n"
            "/reporte nutricion — análisis de nutrición\n"
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
        try:
            result = subprocess.run(
                ["git", "-C", self.repo_path, "pull", "origin", "main"],
                capture_output=True, text=True, timeout=30
            )
            msg = "✅ Memoria sincronizada." if result.returncode == 0 else f"⚠️ Error: {result.stderr[:200]}"
        except FileNotFoundError:
            msg = "⚠️ git no disponible en el contenedor. Usa la automation de HA para sincronizar."
        except Exception as e:
            msg = f"⚠️ Error: {e}"
        await update.message.reply_text(msg)
