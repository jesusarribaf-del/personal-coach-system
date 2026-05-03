# Personal Life Co-Worker & High Performance System

Sistema personal de alto rendimiento operado mediante agentes de Claude Code. No es un repositorio de código: es la infraestructura de vida del usuario.

> **Filosofía:** Primero estabilidad. Después disciplina. Después progreso. Después excelencia.

## Qué es

Un compañero personal senior que ayuda a **ejecutar**, no solo a responder. Cubre cuerpo, mente, dinero, tiempo, energía, decisiones y dirección vital — con un agente principal y 10 subagentes especialistas, memoria persistente y rutinas reutilizables vía slash commands.

## Arquitectura

```
.claude/
  agents/                                 # 1 main + 10 subagentes
    personal-life-co-worker.md            # punto de entrada
    strength-conditioning-coach.md
    muscle-cooking-nutrition-coach.md
    meditation-mindfulness-guide.md
    strategic-decision-advisor.md
    motivation-discipline-coach.md
    financial-control-partner.md
    productivity-systems-builder.md
    recovery-sleep-energy-coach.md
    identity-life-design-coach.md
    knowledge-memory-curator.md
  commands/                               # 26 slash commands
memory/                                   # estado del usuario (15 archivos)
data/                                     # datos crudos y procesados
docs/                                     # referencias, plantillas, ejemplos
reports/                                  # weekly, monthly, quarterly
playbooks/                                # protocolos por dominio
dashboards/                               # vistas agregadas
CLAUDE.md                                 # instrucciones globales
```

## Setup inicial (15 minutos, una vez)

1. **Rellena `memory/personal-profile.md`** con tus datos reales (edad, peso, altura, ocupación, salud base).
2. **Rellena `memory/body-training-profile.md`** (objetivo, marcas, lesiones, material).
3. **Rellena `memory/nutrition-profile.md`** (objetivo nutricional, restricciones, electrodomésticos, presupuesto).
4. **Rellena `memory/financial-control-profile.md`** (ingreso, gastos fijos, deuda, ahorro).
5. **Rellena `memory/goals-roadmap.md`** con tu visión a 12 meses (mínimo).
6. Lanza `/life-roadmap` si quieres construir la visión guiada.
7. Lanza `/daily-plan` para tu primer día con el sistema.

## Uso diario

| Cuándo | Comando | Resultado |
|---|---|---|
| Mañana (5 min) | `/daily-plan` | Plan integrado del día |
| Antes/después de entrenar | `/training-plan` o `/workout-review` | Diseño o diagnóstico |
| Al pensar el menú | `/meal-plan` → `/shopping-list` → `/batch-cooking` | Pipeline completo |
| Tras impulso de gasto | `/money-check` | Aplicación de regla 72h |
| Cuando no quieres entrenar | `/motivation-reset` | Diagnóstico + acción mínima |
| Antes de dormir | `/night-routine` | Cierre del día |
| Domingo | `/weekly-review` | Ritual semanal |
| Fin de mes | `/monthly-review` + `/spending-audit` | Revisión completa |
| Decisión importante | `/decision-analysis` | Análisis estratégico |

## Comandos disponibles

Físico y entrenamiento: `/training-plan` `/workout-review` `/boxing-session` `/cardio-plan`

Nutrición y cocina: `/meal-plan` `/shopping-list` `/batch-cooking` `/cheap-muscle-meals` `/nutrition-review`

Mental y calma: `/meditation` `/morning-routine` `/night-routine`

Decisiones y estrategia: `/decision-analysis` `/strategy-plan` `/life-roadmap`

Disciplina y hábitos: `/motivation-reset` `/discipline-check` `/habit-builder`

Dinero: `/spending-audit` `/money-check`

Sueño y energía: `/sleep-review` `/energy-reset`

Revisiones: `/daily-plan` `/weekly-review` `/monthly-review` `/progress-review`

## Subagentes

Invocables vía Task / Agent o referenciados desde el agente principal según contexto:

- **`personal-life-co-worker`** — coordinador principal.
- **`strength-conditioning-coach`** — entrenamiento integral.
- **`muscle-cooking-nutrition-coach`** — nutrición y cocina práctica.
- **`meditation-mindfulness-guide`** — calma y conciencia.
- **`strategic-decision-advisor`** — decisiones y estrategia.
- **`motivation-discipline-coach`** — hábitos y disciplina.
- **`financial-control-partner`** — control de gasto.
- **`productivity-systems-builder`** — organización y sistemas.
- **`recovery-sleep-energy-coach`** — sueño, energía, recuperación.
- **`identity-life-design-coach`** — propósito y diseño de vida.
- **`knowledge-memory-curator`** — mantenimiento de memoria.

## Memoria del proyecto

`memory/` es la fuente única de verdad sobre el usuario. Todos los agentes la leen antes de aconsejar. Cuando aparece información nueva relevante, el sistema propone:

```
ACTUALIZAR MEMORIA → memory/<archivo>.md
[contenido]
```

Periódicamente se invoca a `knowledge-memory-curator` para auditar y limpiar.

## Reglas de seguridad transversales

- No diagnóstico médico (físico ni mental).
- No sustituye médico, psicólogo, fisioterapeuta, nutricionista clínico ni asesor financiero regulado.
- Síntomas serios o crisis → derivar a profesional cualificado.
- En entrenamiento: técnica y progresión antes que carga.
- En nutrición: sin extremismos.
- En finanzas: sin promesas de rentabilidad ni instrumentos complejos.
- En meditación: sin afirmaciones médicas ni espirituales como hechos.

## Mantenimiento

- **Diario:** `/daily-plan` por la mañana, registro mínimo por la noche.
- **Semanal:** `/weekly-review` el domingo (30-45 min).
- **Mensual:** `/monthly-review` + `/spending-audit`.
- **Trimestral:** revisar `goals-roadmap.md`, `/life-roadmap`, auditoría de memoria.

## Filosofía operativa

1. Diagnostica.
2. Detecta el objetivo real.
3. Pide solo los datos imprescindibles.
4. Involucra a los subagentes necesarios.
5. Propón una acción concreta.
6. Crea un plan simple y ejecutable.
7. Haz seguimiento.
8. Ajusta con datos reales.
9. Sé honesto si te estás autoengañando.

No es motivación vacía. Es ejecución con cabeza.
