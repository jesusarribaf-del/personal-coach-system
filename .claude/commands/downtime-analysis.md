---
description: Análisis de downtime con Pareto, MTBF/MTTR e hipótesis priorizadas.
argument-hint: [archivo CSV/Excel o ruta data/raw] [periodo]
---

Análisis de downtime de `$ARGUMENTS`.

1. `data-analyst-maintenance` carga, limpia y valida el dataset.
2. Calcula: total downtime (h y %), MTBF, MTTR por equipo, Pareto por causa, top 10 eventos.
3. `reliability-engineer` propone 3-5 **hipótesis** priorizadas y siguiente paso (RCA/FMEA/PdM).
4. Output:
   - Tabla resumen
   - Pareto (descrito en texto + spec visual)
   - Top eventos
   - Hipótesis con evidencia
   - Plan de profundización (qué dato buscar)
5. Guardar dataset limpio en `data/processed/` y reporte en `reports/drafts/`.
