# Maintenance Co-Worker & Maintenance Intelligence System

Sistema profesional de agentes Claude Code para Site Manager / Responsable de Mantenimiento Industrial (farma / Tetra Pak).

> Este repo contiene **dos sistemas** independientes:
> - `personal-coach-system/` — sistema previo de coach personal (entrenamiento, nutrición, hábitos).
> - **Maintenance Intelligence System** — el nuevo sistema profesional documentado en este README y en `CLAUDE.md`.

## Arquitectura
```
.claude/
  agents/        # 1 principal + 10 subagentes
  commands/      # 15 comandos slash
docs/
  references/    # glosario, reglas de calidad
  templates/     # A3, RCA, CAPA, FMEA, daily, weekly, ES, email
  examples/
data/
  raw/  processed/
reports/
  drafts/  final/
playbooks/
  maintenance/  lean/  gmp/  leadership/  automation/
CLAUDE.md
```

## Agente principal
`maintenance-co-worker` — orquestador execution-first. Reformula la tarea, elige subagente(s), entrega el output ejecutable.

## Subagentes
1. `data-analyst-maintenance` — KPIs, limpieza, Pareto.
2. `visual-report-designer` — layouts, storytelling visual.
3. `lean-maintenance-engineer` — A3, 5Why, Kaizen, 5S, VSM.
4. `reliability-engineer` — RCM, FMEA, RCA, Weibull, OEE.
5. `gmp-maintenance-advisor` — ALCOA+, desviaciones, CAPA, change control.
6. `team-leadership-partner` — feedback, 1:1, conflictos, PDI.
7. `automation-productivity-engineer` — Excel/Power Query/Power Automate/Python.
8. `executive-communication-editor` — emails, memos, ES/EN.
9. `safety-risk-reviewer` — LOTO, ATEX, PTW, JSA.
10. `knowledge-base-curator` — lecciones aprendidas, OPL, índice.

## Comandos slash
`/daily-report` `/weekly-maintenance-review` `/downtime-analysis` `/rca` `/a3`
`/gmp-impact-assessment` `/capa-draft` `/kpi-dashboard-brief` `/meeting-prep`
`/stakeholder-email` `/team-feedback` `/automation-idea` `/visual-report`
`/data-cleaning-plan` `/executive-summary`

## Cómo usarlo
1. Abre Claude Code en la raíz de este repo.
2. Llama al agente principal: *"actúa como maintenance-co-worker"* o invoca un comando slash.
3. Pasa contexto/datos (CSV en `data/raw/`, descripción del problema, audiencia).
4. Recibe el entregable en `reports/drafts/` o inline.
5. Itera. Cuando esté aprobado, mueve a `reports/final/`.

## Reglas críticas (resumen)
- Nunca inventar datos. Marcar `[DATO PENDIENTE]`.
- Separar Hechos / Hipótesis / Suposiciones.
- Priorización: **Seguridad > Calidad/GMP > Producción > Coste**.
- GMP → siempre `⚠ Requiere revisión QA`.
- Output ejecutivo en 10 puntos (ver `CLAUDE.md`).

## Convenciones de archivos
- Reportes: `reports/{drafts|final}/YYYY-MM-DD_tipo_asunto.md`
- Datos: `data/raw/YYYY-MM-DD_origen_descripcion.csv`
- Playbooks: `playbooks/{area}/NN_titulo.md`
- Sufijo `_EN` para archivos en inglés.

Detalles completos en `CLAUDE.md` y `docs/references/quality-rules.md`.
