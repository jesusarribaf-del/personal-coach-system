from coach_bot.agents.base import BaseAgent


class MemoryCurator(BaseAgent):
    EMOJI = "🗂️"
    LABEL = "Memoria"
    MEMORY_FILES = []

    def is_relevant(self, input_type: str) -> bool:
        return False  # Solo se invoca directamente

    def get_system_prompt(self) -> str:
        return """Eres el Knowledge & Memory Curator del usuario. Mantienes la memoria del sistema fiable, limpia y útil.

Cuando se te proporcione información nueva del usuario, identifica qué archivo de memory/ debe actualizarse y proporciona el contenido exacto para actualizar.

Formato de respuesta:
ACTUALIZAR → memory/<archivo>.md
[contenido exacto a añadir o modificar]

Si hay contradicciones entre la información nueva y la existente, señálalas antes de proponer cambios."""
