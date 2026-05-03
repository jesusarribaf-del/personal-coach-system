---
description: Revisión global de progreso por áreas (cuerpo, mente, hábitos, sueño).
argument-hint: [opcional: área específica o periodo]
---

Coordinación general por `personal-life-co-worker`.

Contexto: $ARGUMENTS

Pasos:
1. Leer todos los archivos de progreso en `memory/`: `training-progress.md`, `nutrition-progress.md`, `sleep-energy-log.md`, `habits-tracker.md`, `meditation-journal.md`, `decision-log.md`.
2. Si la pregunta es sobre un área concreta, consultar al subagente correspondiente.
3. Si es global, integrar:

```
PROGRESS REVIEW — [periodo]

PUNTUACIÓN GLOBAL POR ÁREA (1-5)
- Físico: X
- Nutrición: X
- Mental: X
- Sueño: X
- Hábitos: X
- Identidad / vida: X

QUÉ HA CAMBIADO REALMENTE
- [vs hace 1 mes / 3 meses / 6 meses]

PATRONES POSITIVOS
- [...]

PATRONES NEGATIVOS
- [...]

DESVÍOS RESPECTO AL ROADMAP
- [...]

PRÓXIMA PALANCA (una sola)
- [el cambio que más mueve la aguja en el próximo mes]
```

4. Si detecta contradicciones en `memory/`, derivar a `knowledge-memory-curator`.
