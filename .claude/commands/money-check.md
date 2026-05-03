---
description: Chequeo financiero rápido (semanal o ad-hoc) — estado, riesgos, próxima acción.
argument-hint: [datos del periodo o pregunta concreta]
---

Delega en `financial-control-partner`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/financial-control-profile.md` y `memory/spending-patterns.md`.
2. Pedir solo lo imprescindible (gasto últimos 7 días, próximas obligaciones, ahorro automatizado pendiente).
3. Devolver chequeo breve:

```
MONEY CHECK — [fecha]

ESTADO RÁPIDO
- Gasto últimos 7 días: X€ (vs presupuesto semanal: ±X€)
- Ahorro este mes: X€ (objetivo: Y€)
- Colchón actual: X meses de gastos esenciales

RIESGOS A CORTO
- [vencimientos, suscripciones que cargan, compras pendientes]

ACCIONES ESTA SEMANA
1. [...]
2. [...]

REGLA ANTI-IMPULSO ACTIVA
- [...]
```

4. Si hay impulso de compra concreto, aplicar regla de 72h.
