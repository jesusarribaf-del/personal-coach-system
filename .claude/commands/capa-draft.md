---
description: Borrador de CAPA (Corrective + Preventive Action) para revisión QA.
argument-hint: [evento / desviación / hallazgo]
---

Genera un **borrador de CAPA** para: `$ARGUMENTS`

Subagente líder: `gmp-maintenance-advisor`. Soporte: `reliability-engineer` (causa raíz).

Estructura:
1. **Referencia** (desviación/auditoría/queja/incidente).
2. **Descripción del problema** (factual, ALCOA+).
3. **Análisis de causa raíz** (resumen del RCA).
4. **Corrección** (acción inmediata sobre el evento).
5. **Acción Correctiva** (sobre la causa raíz, evita recurrencia).
6. **Acción Preventiva** (sistémica, evita ocurrencia en otros sitios/equipos similares).
7. **Owner + fecha + recursos** por acción.
8. **Verificación de eficacia**: métrica, plazo, criterio.
9. **Documentos a actualizar** (SOP, plan PM, training).

⚠ *"Borrador. Requiere revisión y aprobación QA. No usar como CAPA oficial."*
Guardar en `reports/drafts/YYYY-MM-DD_capa_<id>.md`.
