---
description: Analiza una sesión de entrenamiento ya hecha y devuelve diagnóstico y ajuste.
argument-hint: [resumen de la sesión: ejercicios, series, reps, RIR, sensaciones]
---

Delega en `strength-conditioning-coach`.

Sesión a revisar: $ARGUMENTS

Pasos para el subagente:
1. Leer `memory/body-training-profile.md` y la última entrada de `memory/training-progress.md`.
2. Diagnosticar la sesión en formato:

```
✅ BIEN
- [...]

🔧 AJUSTA
- [técnica, volumen, intensidad, descanso, selección de ejercicios]

📈 PRÓXIMA SESIÓN
- [carga / reps / RIR / orden]

🧘 RECUPERACIÓN RECOMENDADA HOY
- [...]
```

3. Proponer entrada para `memory/training-progress.md`.
