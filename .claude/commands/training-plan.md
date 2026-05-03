---
description: Diseña o ajusta el plan de entrenamiento (fuerza, cardio, boxeo, movilidad).
argument-hint: [objetivo o contexto del bloque]
---

Delega en el subagente `strength-conditioning-coach`.

Contexto del usuario: $ARGUMENTS

Indica al subagente:
1. Leer `memory/personal-profile.md`, `memory/body-training-profile.md`, `memory/training-progress.md`, `memory/sleep-energy-log.md`.
2. Confirmar: objetivo principal vigente, frecuencia disponible, material, lesiones activas, tiempo por sesión.
3. Diseñar un plan semanal completo en el formato estándar del agente (LUNES → DOMINGO con calentamiento, bloque principal, accesorios, cierre, RIR/RPE, descansos).
4. Incluir cómo progresa semana a semana y señales para ajustar.
5. Indicar qué registrar en `memory/training-progress.md`.

Si el usuario ya tiene un plan vigente y solo pide ajuste, leer el plan actual antes de modificar.
