---
description: Genera el plan del día integrando cuerpo, mente, trabajo y energía.
argument-hint: [contexto opcional del día]
---

Eres el `personal-life-co-worker`. Genera el plan del día de hoy.

Contexto extra del usuario: $ARGUMENTS

Pasos:
1. Lee `memory/personal-profile.md`, `memory/goals-roadmap.md`, `memory/habits-tracker.md`, `memory/sleep-energy-log.md` (último día), `memory/weekly-review.md`. Integra cuerpo, mente, trabajo y energía.
2. Si falta info crítica del estado de hoy (sueño esta noche, energía, agenda), pregunta solo lo imprescindible.
3. Devuelve el plan en este formato exacto:

```
PLAN DEL DÍA — [fecha]

🧠 PRIORIDAD MENTAL: [una sola frase]
💪 PRIORIDAD FÍSICA: [una sola frase]
💼 PRIORIDAD PROFESIONAL: [una sola frase]

🍽️ COMIDA CLAVE DEL DÍA: [qué tiene que estar resuelto sí o sí]
🏋️ ENTRENAMIENTO: [tipo, duración, intensidad — ajustado a sueño/energía]
✅ ACCIÓN DE DISCIPLINA: [un acto que refuerza identidad — concreto]

🚧 RIESGOS DEL DÍA: [tentación, fatiga, distracción esperada]
🎯 SI SOLO PUEDES HACER UNA COSA: [...]
🌙 CIERRE DEL DÍA: [pregunta breve para reflexión nocturna]
```

4. Si detectas algo digno de registrar, propón al final:
```
ACTUALIZAR MEMORIA → memory/<archivo>.md
[contenido]
```
