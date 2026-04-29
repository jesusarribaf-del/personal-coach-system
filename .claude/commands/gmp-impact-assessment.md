---
description: Evaluación de impacto GMP de una intervención o cambio.
argument-hint: [descripción intervención/cambio]
---

Realiza un **GMP Impact Assessment** sobre: `$ARGUMENTS`

Subagente líder: `gmp-maintenance-advisor`.

Salida estructurada:
1. **Descripción de la intervención/cambio**.
2. **Sistema/equipo y criticidad GMP** (directo / indirecto / no-GMP).
3. **Evaluación de impacto en**:
   - Producto (calidad, identidad, pureza, potencia)
   - Proceso (parámetros críticos, CPP)
   - Equipo (función, performance, contacto producto)
   - Sistema computarizado y datos (ALCOA+)
   - Validación / calificación (¿requiere requalificación?)
4. **Lotes potencialmente afectados** (ventana temporal).
5. **Acciones requeridas**: change control, desviación, CAPA, requalificación, update SOP.
6. **Recomendación** y nivel de riesgo (bajo/medio/alto).

⚠ Marcar siempre: *"Borrador. Requiere revisión y aprobación QA antes de uso."*
Guardar en `reports/drafts/YYYY-MM-DD_gmp_impact_<asunto>.md`.
