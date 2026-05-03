# memory/

Estado persistente del usuario. Fuente única de verdad para todos los agentes.

## Convenciones

- Cada archivo `.md` lleva una sección `## Última actualización: AAAA-MM-DD`.
- **Perfiles** (personal, body-training, nutrition): estado actual, se sobrescriben.
- **Roadmap y reviews**: estado actual + sección "histórico".
- **Logs** (training-progress, nutrition-progress, sleep-energy-log, decision-log, meditation-journal): append-only con fechas.
- **Tracker**: `habits-tracker.md` con adherencia semanal.
- **Risks**: `assumptions-and-risks.md` lista viva.

## Archivado

Cuando un log supere ~1500 líneas o un trimestre, mover lo antiguo a:

```
memory/archive/AAAA-Qn/<archivo>.md
```

Lo gestiona `knowledge-memory-curator`.

## Privacidad

Estos archivos contienen datos personales sensibles. Consideraciones:

- Si el repo es público, **no** hagas push de `memory/` con datos reales — gitignóralo.
- Para uso privado en remoto, mantén el repo privado.
- Considera cifrado en reposo si trabajas con datos médicos o financieros sensibles.
