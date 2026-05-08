# Telegram Coach Bot — Implementation Plan (Plan A: Bot Core + Agentes)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bot de Telegram corriendo en el RPi (AppDaemon) que recibe imágenes de AutoSleep, Jefit y Strava y responde con análisis multi-agente usando los 9 agentes especializados del proyecto.

**Architecture:** AppDaemon add-on gestiona el ciclo de vida. El bot corre en un hilo dedicado con su propio event loop asyncio. El orquestador clasifica el input, lanza llamadas paralelas a Claude API con los agentes relevantes, y el sintetizador compone la respuesta final en secciones etiquetadas.

**Tech Stack:** `python-telegram-bot==20.7`, `anthropic`, `Pillow`, `pytest`, `pytest-asyncio`. Python 3.11 (AppDaemon add-on).

---

## Estructura de archivos

```
/config/appdaemon/apps/
  apps.yaml                         # config de la app AppDaemon
  coach_bot/
    __init__.py
    app.py                          # entrada AppDaemon — arranca el bot en hilo
    bot_handlers.py                 # handlers de Telegram (mensajes, comandos, fotos)
    orchestrator.py                 # clasifica input + routing a agentes
    synthesizer.py                  # combina respuestas multi-agente
    memory_reader.py                # lee archivos memory/ del repo
    agents/
      __init__.py
      base.py                       # clase base abstracta
      sleep.py                      # recovery-sleep-energy-coach
      strength.py                   # strength-conditioning-coach
      nutrition.py                  # muscle-cooking-nutrition-coach
      meditation.py                 # meditation-mindfulness-guide
      decisions.py                  # strategic-decision-advisor
      motivation.py                 # motivation-discipline-coach
      productivity.py               # productivity-systems-builder
      identity.py                   # identity-life-design-coach
      memory_curator.py             # knowledge-memory-curator
      life_coworker.py              # personal-life-co-worker (router principal)
tests/
  conftest.py
  test_memory_reader.py
  test_orchestrator.py
  test_synthesizer.py
  test_agents.py
```

> **Rutas en Windows (Samba):** `/config/` = `Z:\` en el PC. Editar archivos desde el PC en `Z:\appdaemon\apps\coach_bot\`.

---

## Task 1: Configuración del entorno AppDaemon en RPi

**Files:**
- Modify: `Z:\appdaemon\apps\apps.yaml` (crear si no existe)

### Paso 1.1 — Instalar el add-on AppDaemon en Home Assistant

- [ ] En HA → Ajustes → Add-ons → Tienda → buscar "AppDaemon" → Instalar.
- [ ] Activar "Inicio automático" y "Watchdog".

### Paso 1.2 — Configurar packages en la UI del add-on

- [ ] En el add-on AppDaemon → pestaña "Configuración", añadir:

```yaml
python_packages:
  - python-telegram-bot==20.7
  - anthropic==0.40.0
  - Pillow==10.4.0
  - pytest==8.3.3
  - pytest-asyncio==0.24.0
```

- [ ] Guardar y reiniciar el add-on.

### Paso 1.3 — Crear estructura de directorios

- [ ] Desde el PC con Samba (Z:), crear manualmente las carpetas:

```
Z:\appdaemon\apps\coach_bot\
Z:\appdaemon\apps\coach_bot\agents\
Z:\appdaemon\apps\tests\
```

### Paso 1.4 — Clonar el repo del proyecto en el RPi

- [ ] Desde SSH del add-on o terminal de HA, ejecutar:

```bash
cd /config
git clone https://github.com/jesusarribaf-del/personal-coach-system.git personal-coach-system
```

- [ ] Verificar que existe `/config/personal-coach-system/memory/personal-profile.md`.

### Paso 1.5 — Crear archivo de configuración de la app

- [ ] Crear `Z:\appdaemon\apps\apps.yaml`:

```yaml
coach_bot:
  module: coach_bot.app
  class: CoachBotApp
  bot_token: "TU_TOKEN_TELEGRAM_AQUI"
  anthropic_api_key: "TU_API_KEY_ANTHROPIC_AQUI"
  repo_path: "/config/personal-coach-system"
  authorized_chat_id: TU_CHAT_ID_AQUI
```

> **Cómo obtener `authorized_chat_id`:** envía un mensaje a @userinfobot en Telegram.
> **Bot token:** está en `C:\Users\jesus\CUsersjesustelegram_bot_orig.py`. Búscalo ahí.

### Paso 1.6 — Crear `__init__.py` vacíos

- [ ] Crear `Z:\appdaemon\apps\coach_bot\__init__.py` (vacío).
- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\__init__.py` (vacío).

---

## Task 2: Memory Reader

**Files:**
- Create: `/config/appdaemon/apps/coach_bot/memory_reader.py`
- Create: `/config/appdaemon/apps/tests/test_memory_reader.py`

### Paso 2.1 — Escribir el test

- [ ] Crear `Z:\appdaemon\apps\tests\test_memory_reader.py`:

```python
import pytest
import os
import tempfile
from coach_bot.memory_reader import MemoryReader

@pytest.fixture
def tmp_repo(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "personal-profile.md").write_text(
        "# Perfil personal\n\n- Nombre: Jesús\n- Edad: 30\n"
    )
    (memory_dir / "sleep-energy-log.md").write_text(
        "# Log sueño\n\n| 2026-05-07 | 7h | 23:00 | 06:00 | 0 | 4 | 4 | 100mg | no | ok |\n"
    )
    return str(tmp_path)

def test_read_single_file(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files(["personal-profile.md"])
    assert "Jesús" in content
    assert "## personal-profile.md" in content

def test_read_multiple_files(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files(["personal-profile.md", "sleep-energy-log.md"])
    assert "Jesús" in content
    assert "Log sueño" in content

def test_missing_file_skipped(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files(["personal-profile.md", "nonexistent.md"])
    assert "Jesús" in content
    assert "nonexistent" not in content

def test_empty_list(tmp_repo):
    reader = MemoryReader(tmp_repo)
    content = reader.read_files([])
    assert content == ""
```

### Paso 2.2 — Ejecutar test (debe fallar)

- [ ] Desde SSH/terminal: `cd /config && python -m pytest appdaemon/apps/tests/test_memory_reader.py -v`
- [ ] Esperado: `ModuleNotFoundError: No module named 'coach_bot'`

### Paso 2.3 — Implementar `memory_reader.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\memory_reader.py`:

```python
import os

class MemoryReader:
    def __init__(self, repo_path: str):
        self.memory_path = os.path.join(repo_path, "memory")

    def read_files(self, filenames: list[str]) -> str:
        if not filenames:
            return ""
        sections = []
        for filename in filenames:
            path = os.path.join(self.memory_path, filename)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                    sections.append(f"## {filename}\n{content}")
                except Exception:
                    pass
        return "\n\n---\n\n".join(sections)
```

### Paso 2.4 — Ejecutar test (debe pasar)

- [ ] `python -m pytest appdaemon/apps/tests/test_memory_reader.py -v`
- [ ] Esperado: 4 tests en verde.

### Paso 2.5 — Commit

```bash
git add appdaemon/apps/coach_bot/memory_reader.py appdaemon/apps/tests/test_memory_reader.py
git commit -m "feat: add MemoryReader module"
```

---

## Task 3: Base Agent y Synthesizer

**Files:**
- Create: `/config/appdaemon/apps/coach_bot/agents/base.py`
- Create: `/config/appdaemon/apps/coach_bot/synthesizer.py`
- Create: `/config/appdaemon/apps/tests/test_synthesizer.py`

### Paso 3.1 — Crear `agents/base.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\base.py`:

```python
import asyncio
from abc import ABC, abstractmethod
from anthropic import Anthropic
from coach_bot.memory_reader import MemoryReader

NO_CONTRIBUTION = "NO_APORTACION"

class BaseAgent(ABC):
    MEMORY_FILES: list[str] = []
    EMOJI: str = "🤖"
    LABEL: str = "Agente"
    MODEL_FULL = "claude-sonnet-4-6"
    MODEL_BRIEF = "claude-haiku-4-5-20251001"

    def __init__(self, repo_path: str, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.memory = MemoryReader(repo_path)

    @abstractmethod
    def get_system_prompt(self) -> str: ...

    @abstractmethod
    def is_relevant(self, input_type: str) -> bool: ...

    async def analyze(self, context: dict, full: bool = True) -> str | None:
        if not full and not self.is_relevant(context.get("input_type", "text")):
            return None

        memory_context = self.memory.read_files(self.MEMORY_FILES)
        messages = self._build_messages(context, memory_context, full)
        model = self.MODEL_FULL if full else self.MODEL_BRIEF
        max_tokens = 600 if full else 200

        loop = asyncio.get_event_loop()
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
        if not full and text == NO_CONTRIBUTION:
            return None
        return text

    def _build_messages(self, context: dict, memory: str, full: bool) -> list:
        content = []
        if context.get("image_base64"):
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": context.get("image_media_type", "image/jpeg"),
                    "data": context["image_base64"],
                },
            })

        task_text = context.get("text", "Analiza el input proporcionado.")
        if not full:
            task_text = (
                f"Analiza este input desde tu dominio especializado. "
                f"Si tienes algo concreto y accionable que añadir, hazlo en máximo 3 líneas. "
                f"Si NO tienes nada relevante que añadir desde tu dominio, responde EXACTAMENTE: {NO_CONTRIBUTION}\n\n"
                f"{task_text}"
            )

        prompt = f"MEMORIA DEL USUARIO:\n{memory}\n\nINPUT:\n{task_text}" if memory else task_text
        content.append({"type": "text", "text": prompt})
        return [{"role": "user", "content": content}]
```

### Paso 3.2 — Escribir test del synthesizer

- [ ] Crear `Z:\appdaemon\apps\tests\test_synthesizer.py`:

```python
from coach_bot.synthesizer import synthesize

def test_primary_only():
    result = synthesize(
        primary_text="Sueño profundo 7h. HRV 65. Recuperado.",
        primary_label="💤 Descanso",
        secondary_results=[]
    )
    assert "💤 Descanso" in result
    assert "Sueño profundo" in result

def test_primary_plus_secondary():
    result = synthesize(
        primary_text="HRV bajo. Día de carga reducida.",
        primary_label="💤 Descanso",
        secondary_results=[
            ("🏋️ Entreno", "Sesión técnica hoy, sin máximos."),
            ("🥗 Nutrición", "Prioriza carbohidratos en el desayuno."),
        ]
    )
    assert "💤 Descanso" in result
    assert "🏋️ Entreno" in result
    assert "🥗 Nutrición" in result

def test_none_secondaries_filtered():
    result = synthesize(
        primary_text="Todo bien.",
        primary_label="💤 Descanso",
        secondary_results=[("🏋️ Entreno", None)]
    )
    assert "🏋️ Entreno" not in result

def test_header_contains_date():
    result = synthesize(
        primary_text="Test.",
        primary_label="💤 Descanso",
        secondary_results=[]
    )
    import datetime
    today = datetime.date.today().strftime("%d %b")
    assert today in result or "📊" in result
```

### Paso 3.3 — Implementar `synthesizer.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\synthesizer.py`:

```python
import datetime

def synthesize(
    primary_text: str,
    primary_label: str,
    secondary_results: list[tuple[str, str | None]],
) -> str:
    today = datetime.date.today().strftime("%-d %b")
    lines = [f"📊 *Análisis · {today}*\n"]

    lines.append(f"*{primary_label}*")
    lines.append(primary_text)

    for label, text in secondary_results:
        if text and text.strip():
            lines.append(f"\n*{label}*")
            lines.append(text)

    return "\n".join(lines)
```

### Paso 3.4 — Ejecutar tests

- [ ] `python -m pytest appdaemon/apps/tests/test_synthesizer.py -v`
- [ ] Esperado: 4 tests en verde.

### Paso 3.5 — Commit

```bash
git add appdaemon/apps/coach_bot/agents/base.py appdaemon/apps/coach_bot/synthesizer.py appdaemon/apps/tests/test_synthesizer.py
git commit -m "feat: add BaseAgent and synthesizer"
```

---

## Task 4: Orchestrator

**Files:**
- Create: `/config/appdaemon/apps/coach_bot/orchestrator.py`
- Create: `/config/appdaemon/apps/tests/test_orchestrator.py`

### Paso 4.1 — Escribir tests del orchestrator

- [ ] Crear `Z:\appdaemon\apps\tests\test_orchestrator.py`:

```python
import pytest
from unittest.mock import MagicMock
from coach_bot.orchestrator import Orchestrator, InputType

def make_message(text=None, has_photo=False, caption=None):
    msg = MagicMock()
    msg.text = text
    msg.caption = caption
    msg.photo = [MagicMock()] if has_photo else []
    return msg

def test_classify_text():
    orc = Orchestrator()
    msg = make_message(text="no quiero entrenar hoy")
    assert orc.classify(msg) == InputType.TEXT

def test_classify_report():
    orc = Orchestrator()
    msg = make_message(text="/reporte semanal")
    assert orc.classify(msg) == InputType.REPORT

def test_classify_photo_no_caption():
    orc = Orchestrator()
    msg = make_message(has_photo=True)
    result = orc.classify(msg)
    assert result in (InputType.SLEEP_IMAGE, InputType.WORKOUT_STRENGTH, InputType.WORKOUT_CARDIO)

def test_classify_photo_sleep_caption():
    orc = Orchestrator()
    msg = make_message(has_photo=True, caption="autosleep")
    assert orc.classify(msg) == InputType.SLEEP_IMAGE

def test_classify_photo_jefit_caption():
    orc = Orchestrator()
    msg = make_message(has_photo=True, caption="jefit")
    assert orc.classify(msg) == InputType.WORKOUT_STRENGTH

def test_classify_photo_strava_caption():
    orc = Orchestrator()
    msg = make_message(has_photo=True, caption="strava")
    assert orc.classify(msg) == InputType.WORKOUT_CARDIO

def test_get_primary_agent_for_sleep():
    orc = Orchestrator()
    assert orc.get_primary_key(InputType.SLEEP_IMAGE) == "sleep"

def test_get_secondary_keys_for_sleep():
    orc = Orchestrator()
    keys = orc.get_secondary_keys(InputType.SLEEP_IMAGE)
    assert "strength" in keys
    assert "nutrition" in keys

def test_get_secondary_keys_for_strength():
    orc = Orchestrator()
    keys = orc.get_secondary_keys(InputType.WORKOUT_STRENGTH)
    assert "nutrition" in keys
    assert "sleep" in keys
```

### Paso 4.2 — Ejecutar (debe fallar)

- [ ] `python -m pytest appdaemon/apps/tests/test_orchestrator.py -v`
- [ ] Esperado: `ModuleNotFoundError`

### Paso 4.3 — Implementar `orchestrator.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\orchestrator.py`:

```python
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
_REPORT_KEYWORDS = {"/reporte"}

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
        text = (message.text or message.caption or "").lower().strip()

        if any(text.startswith(k) for k in _REPORT_KEYWORDS):
            return InputType.REPORT

        if message.photo:
            for kw in _SLEEP_KEYWORDS:
                if kw in text:
                    return InputType.SLEEP_IMAGE
            for kw in _STRENGTH_KEYWORDS:
                if kw in text:
                    return InputType.WORKOUT_STRENGTH
            for kw in _CARDIO_KEYWORDS:
                if kw in text:
                    return InputType.WORKOUT_CARDIO
            return InputType.SLEEP_IMAGE  # default for photos without caption

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
```

### Paso 4.4 — Ejecutar tests

- [ ] `python -m pytest appdaemon/apps/tests/test_orchestrator.py -v`
- [ ] Esperado: 9 tests en verde.

### Paso 4.5 — Commit

```bash
git add appdaemon/apps/coach_bot/orchestrator.py appdaemon/apps/tests/test_orchestrator.py
git commit -m "feat: add Orchestrator with input classification"
```

---

## Task 5: Módulos de los 9 agentes

**Files:**
- Create: `agents/sleep.py`, `agents/strength.py`, `agents/nutrition.py`, `agents/meditation.py`, `agents/decisions.py`, `agents/motivation.py`, `agents/productivity.py`, `agents/identity.py`, `agents/memory_curator.py`, `agents/life_coworker.py`
- Create: `tests/test_agents.py`

### Paso 5.1 — Crear `agents/sleep.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\sleep.py`:

```python
from coach_bot.agents.base import BaseAgent

class SleepCoach(BaseAgent):
    EMOJI = "💤"
    LABEL = "Descanso"
    MEMORY_FILES = ["personal-profile.md", "sleep-energy-log.md", "body-training-profile.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type in ("sleep", "strength", "cardio", "text")

    def get_system_prompt(self) -> str:
        return """Eres el Recovery, Sleep & Energy Coach del usuario. Vigilas el motor de fondo: sueño, fatiga y recuperación.

Eres experto en: higiene del sueño (luz, temperatura, horarios, pantallas), recuperación muscular (HRV, DOMS), estrés crónico, ritmos circadianos, energía diaria, cafeína (corte 8-10h antes de dormir), siestas y rutinas nocturnas.

Antes de aconsejar lee los datos de memoria proporcionados.

Diagnóstico: patrón de sueño real. Señales rojas: sueño <6h reiterado, fatiga crónica → propón evaluación médica.
Modula entrenamiento por sueño: si <6h dos noches, reducir intensidad.

Responde en español. Sé directo, sin preambles. Usa el formato:
💤 Descanso
[diagnóstico en 1-2 líneas]
[recomendación concreta]

Si en el contexto hay imagen de AutoSleep, analiza los datos visibles (HRV, horas, calidad, despertares).
No diagnostiques trastornos del sueño. Deriva si hay síntomas graves."""
```

### Paso 5.2 — Crear `agents/strength.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\strength.py`:

```python
from coach_bot.agents.base import BaseAgent

class StrengthCoach(BaseAgent):
    EMOJI = "🏋️"
    LABEL = "Entreno"
    MEMORY_FILES = ["personal-profile.md", "body-training-profile.md", "training-progress.md", "sleep-energy-log.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type in ("strength", "cardio", "sleep", "text")

    def get_system_prompt(self) -> str:
        return """Eres el Strength & Conditioning Coach del usuario. Especialista en entrenamiento integral.

Experto en: hipertrofia, fuerza máxima, biomecánica, prevención de lesiones, cardio (Z2, HIIT), boxeo, movilidad y programación de mesociclos (RIR/RPE).

Lee la memoria del usuario antes de aconsejar.

Técnica y seguridad antes que carga. Si sueño <6h dos días: reduce intensidad o cambia a sesión técnica.
En lesión o dolor agudo: stop, deriva a fisioterapeuta.

Responde en español. Sé directo. Usa el formato:
🏋️ Entreno
[diagnóstico en 1 línea si es revisión, o recomendación directa]
[plan concreto: tipo de sesión, ajustes, próximo paso]

Si hay imagen de Jefit, analiza el entrenamiento registrado (ejercicios, series, cargas, RIR).
Si hay imagen de Strava, analiza la sesión de cardio (distancia, ritmo, FC, zonas)."""
```

### Paso 5.3 — Crear `agents/nutrition.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\nutrition.py`:

```python
from coach_bot.agents.base import BaseAgent

class NutritionCoach(BaseAgent):
    EMOJI = "🥗"
    LABEL = "Nutrición"
    MEMORY_FILES = ["personal-profile.md", "nutrition-profile.md", "nutrition-progress.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type in ("sleep", "strength", "cardio", "text")

    def get_system_prompt(self) -> str:
        return """Eres el Muscle Cooking & Nutrition Coach del usuario. Especialista en comer bien, cocinar fácil y gastar poco.

Experto en: ganancia de masa muscular, proteína (fuentes baratas, timing), meal prep, batch cooking, compra inteligente y suplementación básica con evidencia (creatina, vitamina D, omega-3).

Lee la memoria del usuario antes de aconsejar.

Adherencia > optimización. Comida normal, sin extremismos. Proteína prioritaria (~30-40g por comida principal).
No prescribas dietas para patologías. Deriva a nutricionista clínico si hay condición médica.

Responde en español. Sé directo. Usa el formato:
🥗 Nutrición
[ajuste concreto del día o recomendación puntual]

Ejemplo: si el sueño fue malo (cortisol elevado), recomienda carbohidratos complejos en desayuno y evitar cafeína temprana."""
```

### Paso 5.4 — Crear `agents/meditation.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\meditation.py`:

```python
from coach_bot.agents.base import BaseAgent

class MeditationGuide(BaseAgent):
    EMOJI = "🧘"
    LABEL = "Meditación"
    MEMORY_FILES = ["personal-profile.md", "meditation-journal.md", "sleep-energy-log.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type in ("sleep", "text")

    def get_system_prompt(self) -> str:
        return """Eres el Meditation & Mindfulness Guide del usuario. Voz serena, profunda, práctica.

Experto en: meditación (anapana, body scan, atención abierta), respiración (4-7-8, box breathing, coherencia cardíaca), gestión de estrés, calma emocional y rutinas contemplativas.

Solo responde si el input sugiere: estrés, sueño fragmentado (3+ noches), ansiedad o petición explícita de práctica meditativa.
Si no hay señal clara de que tu aportación sea relevante hoy, responde: NO_APORTACION

Responde en español. Usa el formato:
🧘 Meditación
[práctica concreta: nombre, duración, 2-3 pasos]

No hagas afirmaciones médicas. No sustituyes terapia ni psiquiatría."""
```

### Paso 5.5 — Crear `agents/decisions.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\decisions.py`:

```python
from coach_bot.agents.base import BaseAgent

class DecisionAdvisor(BaseAgent):
    EMOJI = "🎯"
    LABEL = "Decisión"
    MODEL_FULL = "claude-opus-4-7"
    MEMORY_FILES = ["personal-profile.md", "goals-roadmap.md", "decision-log.md", "assumptions-and-risks.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type == "text"

    def get_system_prompt(self) -> str:
        return """Eres el Strategic Decision Advisor del usuario. Frío cuando hace falta. Racional. Honesto.

Experto en: pensamiento estratégico, decisiones bajo incertidumbre, coste de oportunidad, análisis de riesgos, escenarios best/base/worst, modelos mentales (regret minimization, pre-mortem, statu quo, costo hundido).

Solo actúa cuando el usuario pide ayuda con una decisión o dilema importante. Si el input es sobre sueño, entreno o nutrición rutinarios: NO_APORTACION

Separa cuatro capas: deseo, miedo, evidencia, estrategia.
No refuerces decisiones impulsivas. Distingue decisiones reversibles de irreversibles.
En decisiones legales, médicas o psicológicas relevantes: deriva a profesional.

Responde en español. Sé directo. Usa el formato:
🎯 Decisión
[reformulación de la decisión real]
[recomendación clara + próxima acción]"""
```

### Paso 5.6 — Crear `agents/motivation.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\motivation.py`:

```python
from coach_bot.agents.base import BaseAgent

class MotivationCoach(BaseAgent):
    EMOJI = "🔥"
    LABEL = "Disciplina"
    MEMORY_FILES = ["personal-profile.md", "habits-tracker.md", "goals-roadmap.md", "sleep-energy-log.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type in ("strength", "text")

    def get_system_prompt(self) -> str:
        return """Eres el Motivation & Discipline Coach del usuario. Motivador, pero no blando. Detectas excusas, no las consuelas.

Experto en: psicología del hábito, identidad personal, disciplina, procrastinación, constancia y sistemas de rendición de cuentas.

Distingue fatiga real (sueño, sobrecarga) de excusa (incomodidad, evasión). Tratarlas igual es un error.
Identidad > metas. Consistencia > perfección. Versión mínima viable del hábito.
Solo interviene si detectas excusa, procrastinación, falta de motivación o diseño de hábito. Si el input es neutro: NO_APORTACION

Responde en español. Usa el formato:
🔥 Disciplina
[diagnóstico honesto: excusa o fatiga real]
[acción mínima concreta: qué hacer en los próximos 10 minutos]"""
```

### Paso 5.7 — Crear `agents/productivity.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\productivity.py`:

```python
from coach_bot.agents.base import BaseAgent

class ProductivityBuilder(BaseAgent):
    EMOJI = "📋"
    LABEL = "Productividad"
    MEMORY_FILES = ["personal-profile.md", "goals-roadmap.md", "habits-tracker.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type == "text"

    def get_system_prompt(self) -> str:
        return """Eres el Productivity Systems Builder del usuario. Diseñas sistemas simples que funcionan en la vida real.

Experto en: planificación semanal, time-blocking, MITs (Most Important Tasks), rutinas de mañana/noche, sistemas en Notion/Calendar/Reminders y automatizaciones con iOS Shortcuts.

Solo interviene cuando el input pide ayuda con organización, planificación, sistemas o productividad. En inputs de entrenamiento o nutrición rutinarios: NO_APORTACION

Sistemas simples sobreviven. Una herramienta por función. Calendario es la verdad.
Un cambio de sistema cada vez. No reformas globales.

Responde en español. Usa el formato:
📋 Productividad
[recomendación de sistema o planificación concreta]"""
```

### Paso 5.8 — Crear `agents/identity.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\identity.py`:

```python
from coach_bot.agents.base import BaseAgent

class IdentityCoach(BaseAgent):
    EMOJI = "🌟"
    LABEL = "Identidad"
    MODEL_FULL = "claude-opus-4-7"
    MEMORY_FILES = ["personal-profile.md", "goals-roadmap.md", "decision-log.md"]

    def is_relevant(self, input_type: str) -> bool:
        return input_type == "text"

    def get_system_prompt(self) -> str:
        return """Eres el Identity & Life Design Coach del usuario. Trabajas la capa más profunda: quién es, qué quiere, hacia dónde va.

Experto en: propósito vital, identidad personal, valores, diseño de vida y dirección a 1/3/5 años.

Solo interviene cuando el input toca propósito, valores, identidad, dirección vital o decisiones de vida importantes. En inputs del día a día (sueño, entreno, menú): NO_APORTACION

Trabaja con preguntas, no con respuestas. Detecta incoherencias entre valores declarados y tiempo/dinero invertido.
No hagas terapia. Deriva si aparece trauma o depresión.

Responde en español. Usa el formato:
🌟 Perspectiva
[una observación o pregunta potente que aporte perspectiva real]"""
```

### Paso 5.9 — Crear `agents/memory_curator.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\memory_curator.py`:

```python
from coach_bot.agents.base import BaseAgent

class MemoryCurator(BaseAgent):
    EMOJI = "🗂️"
    LABEL = "Memoria"
    MEMORY_FILES = []

    def is_relevant(self, input_type: str) -> bool:
        return False  # Solo se invoca directamente, nunca como secundario

    def get_system_prompt(self) -> str:
        return """Eres el Knowledge & Memory Curator del usuario. Mantienes la memoria del sistema fiable, limpia y útil.

Cuando se te proporcione información nueva del usuario, identifica qué archivo de memory/ debe actualizarse y proporciona el contenido exacto para actualizar.

Formato de respuesta:
ACTUALIZAR → memory/<archivo>.md
[contenido exacto a añadir o modificar]

Si hay contradicciones entre la información nueva y la existente, señálalas antes de proponer cambios."""
```

### Paso 5.10 — Crear `agents/life_coworker.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\agents\life_coworker.py`:

```python
from coach_bot.agents.base import BaseAgent

class LifeCoworker(BaseAgent):
    EMOJI = "🧠"
    LABEL = "Coach"
    MODEL_FULL = "claude-opus-4-7"
    MEMORY_FILES = [
        "personal-profile.md",
        "goals-roadmap.md",
        "habits-tracker.md",
        "weekly-review.md",
    ]

    def is_relevant(self, input_type: str) -> bool:
        return True

    def get_system_prompt(self) -> str:
        return """Eres el Personal Life Co-Worker del usuario: su compañero senior de alto rendimiento.

Coordinas cuerpo, mente, trabajo, tiempo, energía y objetivos. Execution-first: diagnostica, detecta el objetivo real, propón acción concreta.

Para inputs de texto libre (dudas, planificación del día, revisiones, peticiones generales): responde tú directamente.
Para imágenes de AutoSleep: coordina el análisis general.
Para imágenes de entreno: coordina el diagnóstico.

Lee siempre la memoria del usuario antes de responder. Sé honesto si el usuario se está autoengañando.

Tono: directo, exigente, realista, práctico, sereno. Tuteo. Sin frases huecas.
Responde en español. Sin preambles. Directo al diagnóstico y la acción."""
```

### Paso 5.11 — Escribir test de agentes (unit, sin API)

- [ ] Crear `Z:\appdaemon\apps\tests\test_agents.py`:

```python
import pytest
from unittest.mock import MagicMock, patch
from coach_bot.agents.sleep import SleepCoach
from coach_bot.agents.strength import StrengthCoach
from coach_bot.agents.meditation import MeditationGuide
from coach_bot.agents.decisions import DecisionAdvisor

@pytest.fixture
def tmp_repo(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "personal-profile.md").write_text("# Perfil\n- Nombre: Jesús")
    (memory_dir / "sleep-energy-log.md").write_text("# Sueño\n- HRV: 42")
    (memory_dir / "body-training-profile.md").write_text("# Entreno\n- Objetivo: hipertrofia")
    return str(tmp_path)

def test_sleep_coach_relevant_for_sleep(tmp_repo):
    agent = SleepCoach(tmp_repo, "fake_key")
    assert agent.is_relevant("sleep") is True

def test_sleep_coach_relevant_for_strength(tmp_repo):
    agent = SleepCoach(tmp_repo, "fake_key")
    assert agent.is_relevant("strength") is True

def test_meditation_not_relevant_for_strength(tmp_repo):
    agent = MeditationGuide(tmp_repo, "fake_key")
    assert agent.is_relevant("strength") is False

def test_decisions_not_relevant_for_sleep(tmp_repo):
    agent = DecisionAdvisor(tmp_repo, "fake_key")
    assert agent.is_relevant("sleep") is False

def test_strength_relevant_for_cardio(tmp_repo):
    agent = StrengthCoach(tmp_repo, "fake_key")
    assert agent.is_relevant("cardio") is True

def test_sleep_coach_has_system_prompt(tmp_repo):
    agent = SleepCoach(tmp_repo, "fake_key")
    prompt = agent.get_system_prompt()
    assert len(prompt) > 50
    assert "sueño" in prompt.lower() or "sleep" in prompt.lower() or "hrv" in prompt.lower()

def test_memory_files_configured(tmp_repo):
    agent = SleepCoach(tmp_repo, "fake_key")
    assert "sleep-energy-log.md" in agent.MEMORY_FILES
    assert "personal-profile.md" in agent.MEMORY_FILES
```

### Paso 5.12 — Ejecutar tests de agentes

- [ ] `python -m pytest appdaemon/apps/tests/test_agents.py -v`
- [ ] Esperado: 7 tests en verde.

### Paso 5.13 — Commit

```bash
git add appdaemon/apps/coach_bot/agents/ appdaemon/apps/tests/test_agents.py
git commit -m "feat: add all 9 agent modules"
```

---

## Task 6: Bot handlers y AppDaemon app

**Files:**
- Create: `/config/appdaemon/apps/coach_bot/bot_handlers.py`
- Create: `/config/appdaemon/apps/coach_bot/app.py`

### Paso 6.1 — Crear `bot_handlers.py`

- [ ] Crear `Z:\appdaemon\apps\coach_bot\bot_handlers.py`:

```python
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
        self._pending_memory: dict[int, dict] = {}  # chat_id → {file, content}

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
```

### Paso 6.2 — Crear `app.py` (entrada AppDaemon)

- [ ] Crear `Z:\appdaemon\apps\coach_bot\app.py`:

```python
import asyncio
import logging
import threading
import appdaemon.plugins.hass.hassapi as hass
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from coach_bot.bot_handlers import BotHandlers

logger = logging.getLogger(__name__)


class CoachBotApp(hass.Hass):
    def initialize(self):
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
            await asyncio.Event().wait()  # bloquea indefinidamente
```

### Paso 6.3 — Reiniciar AppDaemon y verificar logs

- [ ] En HA → AppDaemon add-on → Log.
- [ ] Esperado: `CoachBot: bot iniciado, escuchando Telegram...`
- [ ] Si hay error de token: verificar `apps.yaml` con el token correcto de `telegram_bot_orig.py`.

### Paso 6.4 — Test manual en Telegram

- [ ] Abre el bot en Telegram → envía `/start` → debe responder con el menú.
- [ ] Envía un texto libre: `"hoy he dormido mal"` → debe responder con análisis multi-agente.
- [ ] Envía `/agentes` → debe listar los 10 agentes.

### Paso 6.5 — Commit

```bash
git add appdaemon/apps/coach_bot/app.py appdaemon/apps/coach_bot/bot_handlers.py
git commit -m "feat: wire AppDaemon app and Telegram bot handlers"
```

---

## Task 7: Sync de memoria — HA Automation

**Files:**
- Modify: HA automation (vía UI de HA)

### Paso 7.1 — Crear automation en HA

- [ ] En HA → Ajustes → Automatizaciones → Nueva automatización → Editor YAML → pegar:

```yaml
alias: "Coach Bot — Sync memoria GitHub"
description: "git pull del repo cada hora para mantener memory/ fresca"
trigger:
  - platform: time_pattern
    hours: "/1"
action:
  - service: shell_command.coach_git_pull
```

### Paso 7.2 — Añadir shell_command a `configuration.yaml`

- [ ] Editar `Z:\configuration.yaml`, añadir:

```yaml
shell_command:
  coach_git_pull: "git -C /config/personal-coach-system pull origin main"
```

### Paso 7.3 — Reiniciar HA y verificar

- [ ] En HA → Herramientas del desarrollador → Servicios → `shell_command.coach_git_pull` → Llamar.
- [ ] Esperado: sin error. En el terminal SSH: `git -C /config/personal-coach-system log --oneline -1` muestra el último commit de main.

### Paso 7.4 — Commit

```bash
git commit -m "docs: add HA git sync automation instructions"
```

---

## Task 8: Test de integración manual end-to-end

### Paso 8.1 — Prueba: foto AutoSleep sin caption

- [ ] Abre el bot → adjunta captura de AutoSleep → envía sin texto.
- [ ] Esperado: respuesta con secciones 💤 Descanso + al menos uno de [🏋️ Entreno, 🥗 Nutrición, 🧘 Meditación].

### Paso 8.2 — Prueba: foto AutoSleep con caption "autosleep"

- [ ] Envía la misma foto con caption `"autosleep"`.
- [ ] Esperado: mismo flujo, correctamente clasificado como SLEEP_IMAGE.

### Paso 8.3 — Prueba: texto con petición de entreno

- [ ] Envía: `"no quiero entrenar hoy, llevo 2 días sin dormir bien"`
- [ ] Esperado: respuesta de 🧠 Coach o 🔥 Disciplina como primario + 💤 Descanso como secundario.

### Paso 8.4 — Prueba: /actualizar

- [ ] Envía `/actualizar` → debe responder `✅ Memoria sincronizada.`

### Paso 8.5 — Verificar autorización

- [ ] Desde otro chat o cuenta: envía cualquier mensaje al bot.
- [ ] Esperado: sin respuesta (chat_id no autorizado).

### Paso 8.6 — Commit final del plan A

```bash
git add -A
git commit -m "feat: Telegram Coach Bot v1 — bot core + 9 agentes desplegados"
git push origin main
```

---

---

## Task 9: Flujo de propuesta y confirmación de memoria

**Files:**
- Modify: `/config/appdaemon/apps/coach_bot/bot_handlers.py`

Cuando un agente detecta información nueva relevante (nuevo peso, lesión, objetivo cambiado), el bot la propone al usuario antes de escribirla en `memory/`.

### Paso 9.1 — Añadir detección de propuestas en `handle_message`

- [ ] En `bot_handlers.py`, después de generar `response`, añadir al final de `handle_message`:

```python
        # Detectar si algún agente propone actualizar memoria
        memory_proposal = self._extract_memory_proposal(primary_result)
        if memory_proposal:
            self._pending_memory[message.chat_id] = memory_proposal
            proposal_text = (
                f"\n\n📝 *Propuesta de memoria*\n"
                f"`{memory_proposal['file']}`\n"
                f"```\n{memory_proposal['content'][:400]}\n```\n"
                f"¿Confirmas? Responde *sí* o *no*"
            )
            await message.reply_text(proposal_text, parse_mode=ParseMode.MARKDOWN)
```

### Paso 9.2 — Añadir método `_extract_memory_proposal`

- [ ] En la clase `BotHandlers`, añadir:

```python
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
```

### Paso 9.3 — Añadir handler de confirmación

- [ ] En `handle_message`, antes de llamar al orquestador, añadir al inicio:

```python
        # Si hay propuesta pendiente, gestionar confirmación
        text_lower = (message.text or "").lower().strip()
        if message.chat_id in self._pending_memory and text_lower in ("sí", "si", "yes", "s", "y"):
            await self._apply_memory_update(message, self._pending_memory.pop(message.chat_id))
            return
        if message.chat_id in self._pending_memory and text_lower in ("no", "n"):
            self._pending_memory.pop(message.chat_id)
            await message.reply_text("❌ Propuesta descartada.")
            return
```

### Paso 9.4 — Añadir método `_apply_memory_update`

- [ ] En la clase `BotHandlers`, añadir:

```python
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
            await message.reply_text(f"✅ Memoria actualizada: `{proposal['file']}`", parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await message.reply_text(f"⚠️ Error al actualizar memoria: {e}")
```

### Paso 9.5 — Test manual del flujo

- [ ] Envía al bot: `"peso 79kg hoy tras pesarme en ayunas"`
- [ ] El bot debe responder con el análisis + propuesta de actualizar `memory/body-training-profile.md` o `memory/nutrition-progress.md`.
- [ ] Responde `sí` → debe confirmar `✅ Memoria actualizada`.
- [ ] En GitHub, verificar que el commit aparece.

### Paso 9.6 — Commit

```bash
git add appdaemon/apps/coach_bot/bot_handlers.py
git commit -m "feat: memory update proposal and confirmation flow"
git push origin main
```

---

## Notas para Plan B (Reportes PDF) y Plan C (OneDrive)

- **Plan B** comienza cuando el bot esté desplegado y funcionando (Task 8 completado).
- Ficheros a añadir: `coach_bot/reports/` (generator, charts, weekly, training, sleep, progress).
- El handler de `/reporte X` en `bot_handlers.py` ya responde "próximamente" — se conectará en Plan B.
- **Plan C** (rclone + OneDrive): instalación de rclone via SSH en el RPi, configuración OAuth con cuenta Microsoft del usuario, y `coach_bot/onedrive.py` como wrapper de subprocess.
