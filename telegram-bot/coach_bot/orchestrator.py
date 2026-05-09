from enum import Enum

class InputType(Enum):
    SLEEP_IMAGE = "sleep"
    WORKOUT_STRENGTH = "strength"
    WORKOUT_CARDIO = "cardio"
    TEXT = "text"
    REPORT = "report"
    ADDICTION = "addiction"

_SLEEP_KEYWORDS = {"autosleep", "sueño", "dormir", "hvr", "hrv", "sleep"}
_STRENGTH_KEYWORDS = {"jefit", "fuerza", "gym", "pesas", "serie", "rep", "kg", "peso muerto", "sentadilla", "banca"}
_CARDIO_KEYWORDS = {"strava", "cardio", "correr", "running", "bici", "km", "ritmo", "pace"}
_REPORT_KEYWORDS = {
    "reporte", "informe", "resumen semanal", "resumen mensual", "balance semanal",
    "balance del mes", "balance de la semana", "analítica", "estadísticas",
    "cómo ha ido la semana", "cómo ha ido el mes", "dame un reporte",
    "dame un informe", "analiza mi progresión", "analiza mi semana",
    "analiza mi mes", "progreso del mes", "progreso de la semana",
}
_ADDICTION_KEYWORDS = {
    "cannabis", "marihuana", "hierba", "porro", "hash", "thc",
    "tabaco", "cigarro", "cigarrillo", "fumar", "nicotina",
    "abstinencia", "mono", "recaída", "recaer",
    "adicción", "dependencia", "allen carr", "easyway",
    "pequeño monstruo", "gran monstruo", "dejar de fumar", "dejar el cannabis",
}

_PRIMARY: dict[InputType, str] = {
    InputType.SLEEP_IMAGE: "sleep",
    InputType.WORKOUT_STRENGTH: "strength",
    InputType.WORKOUT_CARDIO: "strength",
    InputType.TEXT: "life_coworker",
    InputType.REPORT: "report_designer",
    InputType.ADDICTION: "addiction_coach",
}

_SECONDARY: dict[InputType, list[str]] = {
    InputType.SLEEP_IMAGE: ["strength", "nutrition", "meditation"],
    InputType.WORKOUT_STRENGTH: ["nutrition", "sleep", "motivation"],
    InputType.WORKOUT_CARDIO: ["nutrition", "sleep"],
    InputType.TEXT: ["strength", "nutrition", "sleep", "meditation", "decisions", "motivation", "memory_curator"],
    InputType.REPORT: [],
    InputType.ADDICTION: [],
}

# Secundarios de contexto: se añaden cuando el texto menciona adicción aunque el tipo primario sea otro
_ADDICTION_SECONDARY_TYPES = {InputType.SLEEP_IMAGE, InputType.WORKOUT_STRENGTH, InputType.WORKOUT_CARDIO, InputType.TEXT}


class Orchestrator:
    def classify_from(self, text: str = "", has_photo: bool = False) -> InputType:
        t = text.lower().strip()
        if t.startswith("/reporte"):
            return InputType.REPORT
        if any(kw in t for kw in _REPORT_KEYWORDS):
            return InputType.REPORT
        if has_photo:
            for kw in _SLEEP_KEYWORDS:
                if kw in t:
                    return InputType.SLEEP_IMAGE
            for kw in _STRENGTH_KEYWORDS:
                if kw in t:
                    return InputType.WORKOUT_STRENGTH
            for kw in _CARDIO_KEYWORDS:
                if kw in t:
                    return InputType.WORKOUT_CARDIO
            return InputType.SLEEP_IMAGE
        # Sin foto: comprobar addición antes del fallback a TEXT
        if any(kw in t for kw in _ADDICTION_KEYWORDS):
            return InputType.ADDICTION
        for kw in _SLEEP_KEYWORDS:
            if kw in t:
                return InputType.SLEEP_IMAGE
        for kw in _CARDIO_KEYWORDS:
            if kw in t:
                return InputType.WORKOUT_CARDIO
        return InputType.TEXT

    def classify(self, message) -> InputType:
        text = getattr(message, "text", None) or getattr(message, "caption", None) or ""
        has_photo = bool(getattr(message, "photo", None))
        return self.classify_from(text=text, has_photo=has_photo)

    def get_primary_key(self, input_type: InputType) -> str:
        return _PRIMARY[input_type]

    def get_secondary_keys(self, input_type: InputType, text: str = "") -> list[str]:
        keys = list(_SECONDARY.get(input_type, []))
        # Inyectar addiction_coach como secundario si el texto menciona adicción
        # y el tipo primario no es ya addiction
        if (input_type in _ADDICTION_SECONDARY_TYPES
                and any(kw in text.lower() for kw in _ADDICTION_KEYWORDS)
                and "addiction_coach" not in keys):
            keys.insert(0, "addiction_coach")
        return keys
