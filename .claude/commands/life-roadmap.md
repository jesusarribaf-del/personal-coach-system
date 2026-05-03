---
description: Define o actualiza la visión de vida a 1, 3 y 5 años por áreas.
argument-hint: [opcional: área a profundizar o cambio reciente]
---

Delega en `identity-life-design-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/personal-profile.md`, `memory/goals-roadmap.md`, `memory/decision-log.md`, `memory/monthly-review.md`.
2. Si no existe roadmap previo, conducir el diseño desde cero (estado actual por área, valores declarados vs observados, visión por horizonte).
3. Si existe, revisarlo y actualizar lo que ha cambiado.
4. Devolver en el formato estándar del agente:

```
ESTADO ACTUAL POR ÁREA (1-10)
VALORES DECLARADOS
VALORES OBSERVADOS
INCOHERENCIAS

VISIÓN A 12 MESES (por área)
VISIÓN A 3 AÑOS
VISIÓN A 5 AÑOS

PRÓXIMAS 3 ACCIONES (este mes)
PREGUNTA PARA REFLEXIONAR
```

5. Guardar en `memory/goals-roadmap.md` (estado actual + sección "histórico de cambios" con fecha).
