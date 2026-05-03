---
description: Plan de batch cooking dominical paso a paso (60-90 minutos).
argument-hint: [tiempo disponible, electrodomésticos, días a cubrir]
---

Delega en `muscle-cooking-nutrition-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/nutrition-profile.md` y menú semanal si existe.
2. Confirmar: tiempo disponible (60 / 90 / 120 min), electrodomésticos, raciones objetivo, tuppers/recipientes.
3. Generar plan paralelizado:

```
BATCH COOKING — duración total [X min]

PREPARACIÓN PREVIA (5 min)
- Sacar ingredientes
- Encender horno a Xº
- Poner agua a hervir

LÍNEA 1 — HORNO ([X min])
1. [preparar y meter X]
2. [...]

LÍNEA 2 — VITRO / SARTÉN ([X min en paralelo])
1. [...]

LÍNEA 3 — FREIDORA DE AIRE ([X min en paralelo])
1. [...]

ENSAMBLAJE Y RACIONADO (15 min)
- [tuppers para cada día]

QUÉ QUEDA HECHO
- [proteína para X días]
- [carbo para X días]
- [verdura para X días]
- [salsas]

QUÉ CONGELAR
- [...]
```
