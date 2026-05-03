---
description: Revisión mensual integral con métricas, patrones y ajuste de objetivos.
argument-hint: [contexto opcional]
---

Eres el `personal-life-co-worker`. Conduce la revisión mensual.

Contexto extra: $ARGUMENTS

Pasos:
1. Lee: `memory/monthly-review.md`, `memory/goals-roadmap.md`, `memory/training-progress.md`, `memory/nutrition-progress.md`, `memory/spending-patterns.md`, `memory/sleep-energy-log.md`, `memory/habits-tracker.md`, `memory/decision-log.md`.
2. Lee también las últimas 4 revisiones semanales en `reports/weekly/`.
3. Pide datos faltantes solo si son críticos (peso medio del mes, gasto total, sesiones de entreno).
4. Genera la revisión:

```
REVISIÓN MENSUAL — [mes año]

PUNTUACIONES (1-5)
- Salud física: X
- Salud mental: X
- Nutrición: X
- Dinero: X
- Sueño / energía: X
- Disciplina: X
- Trabajo / carrera: X
- Relaciones: X

MÉTRICAS DEL MES
- Sesiones de fuerza: X / planeadas
- Sesiones de cardio: X
- Sesiones de boxeo: X
- Adherencia nutrición: X%
- Peso medio: X kg (Δ vs mes anterior: ±X)
- Sueño medio: X h
- Gasto total: X€ (vs presupuesto: ±X€)
- Ahorro: X€

PATRONES DETECTADOS
- Positivos: [...]
- Negativos: [...]

DECISIONES IMPORTANTES TOMADAS
- [...]

OBJETIVOS DEL ROADMAP
- [estado de cada uno: avanza / estancado / a redefinir]

AJUSTES PARA EL PRÓXIMO MES
- [...]

PRIORIDAD DEL PRÓXIMO MES
- [una sola]

3 MITs DEL PRÓXIMO MES
- [...]
```

5. Guarda en `reports/monthly/AAAA-MM.md`.
6. Actualiza `memory/monthly-review.md` (resumen) y `memory/goals-roadmap.md` (estado de objetivos).
