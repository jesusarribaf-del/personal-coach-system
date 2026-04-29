---
description: Genera el reporte diario de mantenimiento con KPIs del día, incidencias, acciones y próximos pasos.
argument-hint: [fecha YYYY-MM-DD] [línea/área opcional]
---

Genera el **reporte diario de mantenimiento** para `$ARGUMENTS`.

1. Invoca `data-analyst-maintenance` para calcular KPIs del día (downtime, paradas, PM ejecutados vs plan, backlog delta).
2. Estructura el output con la **plantilla ejecutiva** (Contexto · Mensaje clave · Datos · Insight · Impacto · Acciones · Riesgos).
3. Si faltan datos → marcar `[DATO PENDIENTE]` y listar fuente.
4. Guarda en `reports/drafts/YYYY-MM-DD_daily_report.md`.
5. Cierra con: 3 acciones para mañana + qué necesitas del usuario.

**Tono**: ejecutivo, conciso, ≤1 página A4.
