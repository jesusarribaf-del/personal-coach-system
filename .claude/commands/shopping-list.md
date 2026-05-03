---
description: Genera la lista de la compra estructurada y con coste estimado.
argument-hint: [opcional: supermercado destino, presupuesto, ajustes]
---

Delega en `muscle-cooking-nutrition-coach`.

Contexto: $ARGUMENTS

Para el subagente:
1. Leer el menú semanal vigente (si está en una respuesta reciente o guardado en `data/raw/nutrition/menu-actual.md`).
2. Si no existe menú, pedirlo o sugerir ejecutar `/meal-plan` antes.
3. Generar la lista en este formato:

```
LISTA DE LA COMPRA — semana del [fecha]
Presupuesto objetivo: X€

🥦 FRESCOS
- [...]

❄️ CONGELADOS
- [...]

🍞 DESPENSA
- [...]

🥩 PROTEÍNA
- [...]

🥤 BEBIDAS / OTROS
- [...]

COSTE ESTIMADO: X€
NOTAS DE COMPRA INTELIGENTE:
- [marca blanca recomendada]
- [precio por kg comparado]
- [qué comprar congelado vs fresco]
```

4. Guardar la lista en `data/raw/nutrition/lista-AAAA-MM-DD.md`.
