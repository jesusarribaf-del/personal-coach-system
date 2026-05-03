---
description: Diseña un plan de cardio (Z2, HIIT o mixto) compatible con hipertrofia.
argument-hint: [objetivo: salud cardiovascular, definición, rendimiento; tiempo disponible]
---

Delega en `strength-conditioning-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/body-training-profile.md` y plan de fuerza vigente.
2. Confirmar: objetivo (salud / definición / rendimiento), tiempo semanal disponible para cardio, modalidades preferidas, FC en reposo si la hay.
3. Devolver:

```
PLAN DE CARDIO — objetivo [...]

DISTRIBUCIÓN SEMANAL
- Z2: X sesiones × Y min
- HIIT: X sesiones × Y min
- Total: Z min/semana

MODALIDADES
- [bici, cinta, remo, elíptica, correr, saltar cuerda, etc.]

INTEGRACIÓN CON FUERZA
- [día y hora respecto a sesiones de pierna y empuje]

PROGRESIÓN
- [cómo subir volumen/intensidad cada 2-4 semanas]

SEÑALES DE EXCESO
- [fatiga, marcas que bajan, sueño deteriorado]
```
