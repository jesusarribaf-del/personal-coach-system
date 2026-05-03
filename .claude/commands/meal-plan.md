---
description: Genera el menú semanal con recetas, macros aproximados y batch cooking.
argument-hint: [contexto: presupuesto, días fuera de casa, preferencias semanales]
---

Delega en `muscle-cooking-nutrition-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer `memory/personal-profile.md`, `memory/nutrition-profile.md`, `memory/nutrition-progress.md`.
2. Confirmar: kcal y proteína objetivo, presupuesto semanal aproximado en comida, días en/fuera de casa, electrodomésticos disponibles, aversiones.
3. Generar menú semanal usando el formato estándar del agente: cada día con desayuno, comida, cena, snacks, macros aprox por comida.
4. Incluir bloque de batch cooking del domingo (60-90 min, paso a paso).
5. Indicar cuántas porciones y qué congelar.
6. Recordar al final: usar `/shopping-list` para generar la lista derivada.
