# Patrones multi-agente — Maintenance Intelligence System

El agente principal `maintenance-co-worker` orquesta. Los subagentes pueden trabajar **solos**, **en paralelo**, **en cadena** o **en panel**. Esta guía estandariza cuándo usar cada patrón.

## Patrón 1 — Paralelo (independientes)
Cuándo: las tareas no dependen una de otra y las puedes integrar tú al final.
Beneficio: tiempo.

Ejemplos:
- **Weekly review**: `data-analyst-maintenance` (KPIs) ‖ `safety-risk-reviewer` (incidentes) ‖ `gmp-maintenance-advisor` (desviaciones) ‖ `team-leadership-partner` (notas equipo).
- **Brief de auditoría inminente**: `gmp-maintenance-advisor` (CAPA abiertas) ‖ `data-analyst-maintenance` (PM compliance) ‖ `knowledge-base-curator` (SOPs vigentes).

## Patrón 2 — Cadena (pipeline)
Cuándo: cada paso necesita el output del anterior.
Beneficio: profundidad y rigor.

Cadenas frecuentes:
- **Fallo crítico → comunicación**:
  `data-analyst-maintenance` → `reliability-engineer` (RCA) → `gmp-maintenance-advisor` (impacto GMP/CAPA) → `executive-communication-editor` (email HQ) → `visual-report-designer` (one-pager).
- **Mejora continua**:
  `data-analyst-maintenance` (bad actors) → `lean-maintenance-engineer` (A3) → `automation-productivity-engineer` (tracker Excel) → `knowledge-base-curator` (lección aprendida).
- **Cambio de equipo**:
  `safety-risk-reviewer` (JSA/LOTO) → `gmp-maintenance-advisor` (change control) → `reliability-engineer` (FMEA actualizado) → `executive-communication-editor` (notificación).

## Patrón 3 — Panel (revisión cruzada)
Cuándo: el entregable es de alto riesgo (GMP, seguridad, RRHH, comunicación HQ).
Beneficio: detectar huecos y validar.

Ejemplos:
- A3 producido por `lean-maintenance-engineer` → revisado por `safety-risk-reviewer` + `gmp-maintenance-advisor`.
- Email de escalado por `executive-communication-editor` → revisado por `team-leadership-partner` (tono) + `gmp-maintenance-advisor` (compliance).
- CAPA por `gmp-maintenance-advisor` → revisada por `reliability-engineer` (eficacia técnica).

## Reglas de orquestación (obligatorias para el agente principal)
1. **Declarar el plan** antes de ejecutar: *“Voy a lanzar A en paralelo con B y luego C en cadena con su output”*.
2. **Paralelizar** llamadas independientes en el mismo turno.
3. **Integrar** todo en **un único entregable** (estructura ejecutiva de 10 puntos).
4. **Trazabilidad**: cuando ayude, marcar `[subagente]` la fuente de cada bloque.
5. **Conflicto entre subagentes**: presentar ambas posturas + decisión propuesta + dato que la cerraría.
6. **Panel obligatorio** para outputs con: impacto GMP serio, escalado a HQ, cambio de equipo crítico, comunicación a auditor/cliente.

## Cómo invocar manualmente colaboración
- Llamada al principal con instrucción explícita: *“Usa data-analyst + reliability + gmp en cadena para…”*.
- Comandos slash que ya activan multi-agente: `/weekly-maintenance-review`, `/rca`, `/kpi-dashboard-brief`, `/visual-report`, `/meeting-prep`.
- Petición de revisión cruzada: *“Revisa este A3 con safety y gmp en panel”*.

## Anti-patrones
- Llamar a 5 subagentes para una pregunta simple.
- Encadenar sin pasarse el contexto necesario.
- Entregar la respuesta como un collage sin integrar (el usuario debe leer una pieza, no cuatro).
