import asyncio
from abc import ABC, abstractmethod
from anthropic import Anthropic

NO_CONTRIBUTION = "NO_APORTACION"


class BaseAgent(ABC):
    MEMORY_FILES: list[str] = []
    EMOJI: str = "🤖"
    LABEL: str = "Agente"
    MODEL_FULL = "claude-sonnet-4-6"
    MODEL_BRIEF = "claude-haiku-4-5-20251001"
    MAX_TOKENS_FULL = 1000
    MAX_TOKENS_BRIEF = 300

    def __init__(self, repo_path: str, api_key: str):
        from coach_bot.memory_reader import MemoryReader
        self.client = Anthropic(api_key=api_key)
        self.memory = MemoryReader(repo_path)
        self.repo_path = repo_path

    @abstractmethod
    def get_system_prompt(self) -> str: ...

    @abstractmethod
    def is_relevant(self, input_type: str) -> bool: ...

    async def analyze(self, context: dict, full: bool = True) -> str | None:
        if not full and not self.is_relevant(context.get("input_type", "text")):
            return None
        memory_context = self.memory.read_files(self.MEMORY_FILES)
        conv_context = context.get("conv_context", "")
        messages = self._build_messages(context, memory_context, full, conv_context)
        model = self.MODEL_FULL if full else self.MODEL_BRIEF
        max_tokens = self.MAX_TOKENS_FULL if full else self.MAX_TOKENS_BRIEF
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=self.get_system_prompt(),
                messages=messages,
            ),
        )
        text = response.content[0].text.strip()
        if text == NO_CONTRIBUTION:
            return None
        return text

    def _build_messages(
        self, context: dict, memory: str, full: bool, conv_context: str = ""
    ) -> list:
        content = []
        images = context.get("images") or (
            [{"base64": context["image_base64"], "media_type": context.get("image_media_type", "image/jpeg")}]
            if context.get("image_base64") else []
        )
        for img in images:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": img.get("media_type", "image/jpeg"),
                    "data": img["base64"],
                },
            })
        task_text = context.get("text", "Analiza el input proporcionado.")
        if not full:
            task_text = (
                f"Analiza este input desde tu dominio especializado. "
                f"Si tienes algo concreto y accionable que añadir, escríbelo en 2-3 frases directas, sin títulos ni cabeceras. "
                f"Si NO tienes nada relevante o el agente principal ya lo cubre, responde EXACTAMENTE: {NO_CONTRIBUTION}\n\n"
                f"{task_text}"
            )
        parts = []
        if memory:
            parts.append(f"MEMORIA DEL USUARIO:\n{memory}")
        if conv_context:
            parts.append(conv_context)
        parts.append(f"INPUT:\n{task_text}")
        content.append({"type": "text", "text": "\n\n".join(parts)})
        return [{"role": "user", "content": content}]
