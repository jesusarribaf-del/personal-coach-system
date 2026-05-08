from enum import Enum

class InputType(Enum):
    SLEEP_IMAGE = "sleep"
    WORKOUT_STRENGTH = "strength"
    WORKOUT_CARDIO = "cardio"
    TEXT = "text"
    REPORT = "report"

_SLEEP_KEYWORDS = {"autosleep", "sueño", "dormir", "hvr", "hrv", "sleep"}
_STRENGTH_KEYWORDS = {"jefit", "fuerza", "gym", "pesas", "serie", "rep", "kg", "peso muerto", "sentadilla", "banca"}
_CARDIO_KEYWORDS = {"strava", "cardio", "correr", "running", "bici", "km", "ritmo", "pace"}

_PRIMARY: dict[InputType, str] = {
    InputType.SLEEP_IMAGE: "sleep",
    InputType.WORKOUT_STRENGTH: "strength",
    InputType.WORKOUT_CARDIO: "strength",
    InputType.TEXT: "life_coworker",
    InputType.REPORT: "life_coworker",
}

_SECONDARY: dict[InputType, list[str]] = {
    InputType.SLEEP_IMAGE: ["strength", "nutrition", "meditation"],
    InputType.WORKOUT_STRENGTH: ["nutrition", "sleep", "motivation"],
    InputType.WORKOUT_CARDIO: ["nutrition", "sleep"],
    InputType.TEXT: ["strength", "nutrition", "sleep", "meditation", "decisions", "motivation"],
    InputType.REPORT: [],
}

class Orchestrator:
    def classify(self, message) -> InputType:
        text = (getattr(message, "text", None) or getattr(message, "caption", None) or "").lower().strip()
        if any(text.startswith(k) for k in {"/reporte"}):
            return InputType.REPORT
        if getattr(message, "photo", None):
            for kw in _SLEEP_KEYWORDS:
                if kw in text:
                    return InputType.SLEEP_IMAGE
            for kw in _STRENGTH_KEYWORDS:
                if kw in text:
                    return InputType.WORKOUT_STRENGTH
            for kw in _CARDIO_KEYWORDS:
                if kw in text:
                    return InputType.WORKOUT_CARDIO
            return InputType.SLEEP_IMAGE  # default foto sin caption
        for kw in _SLEEP_KEYWORDS:
            if kw in text:
                return InputType.SLEEP_IMAGE
        for kw in _CARDIO_KEYWORDS:
            if kw in text:
                return InputType.WORKOUT_CARDIO
        return InputType.TEXT

    def get_primary_key(self, input_type: InputType) -> str:
        return _PRIMARY[input_type]

    def get_secondary_keys(self, input_type: InputType) -> list[str]:
        return _SECONDARY.get(input_type, [])
