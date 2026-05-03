---
description: Revisión del patrón de sueño y propuesta de intervención mínima.
argument-hint: [datos: horas, hora acostarse/levantarse, despertares, cafeína]
---

Delega en `recovery-sleep-energy-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/sleep-energy-log.md` (últimos 7-14 días si existen).
2. Si no hay log, pedir datos concretos.
3. Generar diagnóstico en el formato estándar del agente:

```
PATRÓN DETECTADO
CAUSAS PROBABLES (en orden)
INTERVENCIÓN MÍNIMA (1-2 cambios)
CHECKLIST NOCTURNA
REVISIÓN: en 7 días
```

4. Si detecta señales rojas (sueño <6h reiterado, fatiga crónica, despertares con ahogo), recomendar evaluación médica.
5. Proponer entrada/actualización en `memory/sleep-energy-log.md`.
