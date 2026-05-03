---
description: Auditoría rápida de adherencia a hábitos y disciplina semanal.
argument-hint: [opcional: hábito específico a revisar]
---

Delega en `motivation-discipline-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/habits-tracker.md` (estado de cada hábito vivo).
2. Pedir al usuario adherencia honesta de la semana por hábito (X/7 días).
3. Devolver:

```
DISCIPLINE CHECK — semana del [...]

ADHERENCIA POR HÁBITO
- [hábito 1]: X/7 días
- [hábito 2]: X/7 días
- [...]

PATRONES
- Fallos recurrentes: [días, situaciones, triggers]
- Excusas detectadas: [nómbralas]

AJUSTES PROPUESTOS
- Reducir / mantener / eliminar / cambiar anclaje

REGLAS BINARIAS PRÓXIMA SEMANA
- [...]

REFUERZO DE IDENTIDAD
- "Soy una persona que [...]"
```

4. Actualizar `memory/habits-tracker.md`.
