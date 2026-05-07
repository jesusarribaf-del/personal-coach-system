import datetime
import sys


def synthesize(
    primary_text: str,
    primary_label: str,
    secondary_results: list[tuple[str, str | None]],
) -> str:
    fmt = "%#d %b" if sys.platform == "win32" else "%-d %b"
    today = datetime.date.today().strftime(fmt)
    lines = [f"📊 *Análisis · {today}*\n"]
    lines.append(f"*{primary_label}*")
    lines.append(primary_text)
    for label, text in secondary_results:
        if text and text.strip():
            lines.append(f"\n*{label}*")
            lines.append(text)
    return "\n".join(lines)
