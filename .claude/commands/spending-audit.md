---
description: Auditoría detallada de gasto del último mes con detección de fugas.
argument-hint: [periodo y/o datos crudos: extracto, lista de gastos, categorías]
---

Delega en `financial-control-partner`.

Contexto / datos: $ARGUMENTS

Para el subagente:
1. Leer `memory/financial-control-profile.md` y `memory/spending-patterns.md`.
2. Si no hay datos del periodo, pedir extracto, app de gastos o categorización del usuario.
3. Generar auditoría completa en el formato estándar del agente:

```
INGRESO NETO / GASTO TOTAL / RATIO DE AHORRO
GASTOS POR CATEGORÍA
FUGAS DETECTADAS
ACCIONES INMEDIATAS
PRESUPUESTO PROPUESTO PRÓXIMO MES
ALERTAS
```

4. Identificar específicamente:
   - Suscripciones a cancelar/negociar.
   - Gasto hormiga (café, delivery, micropagos).
   - Lifestyle creep si se compara con mes anterior.
5. Actualizar `memory/spending-patterns.md` con hallazgos.
6. Guardar la auditoría en `reports/monthly/AAAA-MM-finanzas.md`.
