import asyncio
import datetime
import sys
from anthropic import Anthropic


async def synthesize_unified(
    api_key: str,
    primary_text: str,
    secondary_results: list[tuple[str, str | None]],
) -> str:
    fmt = "%#d %b" if sys.platform == "win32" else "%-d %b"
    date_str = datetime.date.today().strftime(fmt)

    secondary_texts = [text for _, text in secondary_results if text and text.strip()]

    if not secondary_texts:
        return f"*{date_str}*\n\n{primary_text}"

    combined = primary_text + "\n\n---\n\n" + "\n\n---\n\n".join(secondary_texts)

    loop = asyncio.get_running_loop()
    client = Anthropic(api_key=api_key)

    response = await loop.run_in_executor(
        None,
        lambda: client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1200,
            system=(
                "Sintetiza los siguientes análisis de agentes especializados en UN único mensaje "
                "de Telegram para el coach personal de Jesús. "
                "Escribe como un solo coach hablando directamente, en lenguaje natural y fluido. "
                "Reglas: "
                "un solo bloque de texto sin títulos ni emojis de sección; "
                "elimina solo la información duplicada, NUNCA un protocolo o detalle único: "
                "protocolos concretos (luz matutina, respiración, corte de cafeína), "
                "mecanismos fisiológicos, números, horarios, ejercicios y técnicas específicas "
                "deben aparecer en el resultado aunque alarguen el mensaje; "
                "prioriza lo más accionable para HOY; "
                "tono directo sin preambles. "
                "Límite absoluto: 3800 caracteres (límite de Telegram)."
            ),
            messages=[{
                "role": "user",
                "content": f"Fecha: {date_str}\n\n{combined}"
            }],
        ),
    )

    return f"*{date_str}*\n\n" + response.content[0].text.strip()
