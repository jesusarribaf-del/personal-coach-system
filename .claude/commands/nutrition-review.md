---
description: Revisión nutricional: adherencia, peso, proteína, gasto y ajustes.
argument-hint: [periodo: semana/mes; datos: peso, adherencia, gasto]
---

Delega en `muscle-cooking-nutrition-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/nutrition-progress.md`, `memory/nutrition-profile.md`, `memory/spending-patterns.md`.
2. Pedir datos faltantes (peso medio, adherencia estimada %, gasto en comida del periodo).
3. Devolver:

```
REVISIÓN NUTRICIONAL — [periodo]

ESTADO
- Peso medio: X kg (Δ: ±X)
- Adherencia: X%
- Proteína estimada/día: Xg (objetivo: Y)
- Gasto en comida: X€ (objetivo: Y)

ANÁLISIS
- Qué funciona: [...]
- Qué falla: [...]
- Causas: [...]

AJUSTES PROPUESTOS
- Kcal: [mantener / +X / -X]
- Proteína: [...]
- Estructura del menú: [...]
- Coste: [...]

PRÓXIMOS PASOS
1. [...]
2. [...]
```

4. Proponer entrada en `memory/nutrition-progress.md`.
