---
description: Plan de limpieza y normalización de un dataset de mantenimiento.
argument-hint: [archivo o esquema columnas]
---

Plan de limpieza para: `$ARGUMENTS`

Subagente líder: `data-analyst-maintenance`. Soporte: `automation-productivity-engineer` (Power Query / pandas).

Salida:
1. **Auditoría inicial**: filas, columnas, tipos, % nulos por columna, duplicados, outliers groseros.
2. **Reglas de limpieza** por columna (parseo fechas, normalización texto, mapeo causas, unidades).
3. **Joins/lookups** necesarios (ej. equipo→línea→área).
4. **Validaciones**: integridad referencial, rangos plausibles, fechas coherentes (start<end).
5. **Pipeline reproducible** en Power Query M o pandas.
6. **Salida**: dataset limpio en `data/processed/` + log de transformaciones.
7. **Riesgos** de calidad de dato y cómo monitorizar.
