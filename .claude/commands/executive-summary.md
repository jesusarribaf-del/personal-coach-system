---
description: Resumen ejecutivo de un tema, reporte o evento, en formato BLUF + estructura de 10 puntos.
argument-hint: [tema o ruta de reporte]
---

Genera un **executive summary** sobre: `$ARGUMENTS`

Subagentes: `executive-communication-editor` (estilo) + `data-analyst-maintenance` (datos si los hay).

Estructura obligatoria (estructura ejecutiva del sistema):
1. Contexto
2. Mensaje clave (1 frase, BLUF)
3. Datos (3-5 bullets cuantificados)
4. Insight
5. Impacto (Seguridad/Calidad/OEE/Coste)
6. Causa probable
7. Acción
8. Responsable
9. Fecha
10. Riesgos

Reglas:
- ≤ 1 página A4.
- Sin jerga innecesaria.
- ES o EN según pedido.
- Si faltan datos → marcar `[DATO PENDIENTE]`.
