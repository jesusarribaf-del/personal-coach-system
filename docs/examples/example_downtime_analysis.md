# Ejemplo — Downtime analysis (output esperado)

> Petición: *"Analiza el downtime de la línea TBA-3 de abril."*

## Resumen ejecutivo
- Downtime total **42.6 h** (8.1% del tiempo planificado), +18% vs marzo.
- **MTBF 27 h · MTTR 1.4 h**.
- Pareto: **3 causas** = 71% del downtime → atascos film, fallos sealing, sensor jam.

## KPIs
| Equipo | Eventos | Downtime (h) | MTBF (h) | MTTR (h) |
|--------|---------|--------------|----------|----------|
| TBA-3  | 31      | 42.6         | 27       | 1.4      |

## Pareto causas
1. Atasco film de aluminio — 14.2 h (33%)
2. Fallo en sealing horizontal — 9.8 h (23%)
3. Falsa detección sensor jam — 6.3 h (15%)
4. Cambio formato — 5.1 h
5. Otros — 7.2 h

## Hipótesis priorizadas
- **H1** Tensado film fuera de rango — verificar set-point vs spec proveedor.
  Evidencia: 9 de 14 atascos en lotes con bobinas de proveedor B.
- **H2** Desgaste de mordazas sealing — última sustitución hace 18 meses (vida típica 12).
- **H3** Sensor jam mal calibrado tras intervención del 02-abr.

## Próxima acción
- Abrir RCA sobre H1 (líder: técnico senior packaging).
- Inspección mordazas (24 h).
- Recalibración sensor (turno noche, sin parar línea).

[DATO PENDIENTE: coste/h de la línea TBA-3 para cuantificar impacto €.]

⚠ Si alguno de los lotes implicados está bajo desviación, requiere revisión QA.
