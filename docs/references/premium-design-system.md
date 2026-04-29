# Premium Design System — Maintenance Intelligence System

Estándar visual obligatorio para cualquier output entregable a dirección, HQ, auditores o cliente. Inspirado en McKinsey/BCG decks, *The Economist*, *FT*, IBM Carbon y Material Design.

## Principios
1. **Claridad > densidad.** El aire blanco es información.
2. **Una idea hero por vista.** El resto la soporta.
3. **Data-ink ratio máximo (Tufte).** Cada píxel debe servir al dato.
4. **Restricción cromática.** 60% neutro · 30% primario · 10% acento.
5. **Tipografía editorial.** 2 familias máximo. 3 tamaños por vista.
6. **Accesibilidad por defecto.** Contraste AA (4.5:1). Color nunca como única señal.
7. **Coherencia entre piezas.** Mismo grid, paleta y tipografía en todos los reportes.

## Grid
- A4 vertical: 12 columnas · gutter 4 mm · margen 15–18 mm.
- 16:9 slide (1920×1080): 12 columnas · gutter 24 px · margen 64 px.
- Vertical rhythm: línea base 8 px (o 4 mm).

## Tipografía
**Recomendadas (gratuitas, instaladas o Google Fonts):**
- Sans serif UI/datos: **Inter**, **IBM Plex Sans**, **Source Sans 3**.
- Serif titulares (opcional, editorial): **Source Serif Pro**, **Tinos**, **IBM Plex Serif**.
- Monospace código/números: **JetBrains Mono**, **IBM Plex Mono**.

**Escala modular (ratio 1.25):**
| Rol | Tamaño A4 | Tamaño 16:9 | Peso |
|---|---|---|---|
| Display (hero KPI) | 48–56 pt | 72–96 pt | 700 |
| H1 título | 22 pt | 36 pt | 700 |
| H2 subtítulo | 16 pt | 24 pt | 600 |
| H3 sección | 12 pt | 18 pt | 600 |
| Body | 10 pt | 16 pt | 400 |
| Caption / footnote | 8 pt | 12 pt | 400 |

**Reglas tipográficas:**
- Tracking ligero en titulares (-1%), normal en body.
- Line-height 1.3 (titular) / 1.5 (body).
- Números siempre con *tabular figures* (`font-variant-numeric: tabular-nums`).
- No mayúsculas continuas salvo etiquetas ≤4 palabras.

## Paletas oficiales del sistema
Elige **una** y mantenla en toda la pieza.

### 1. Executive Blue (default ejecutivo)
```
Primary       #0B2545
Primary-2     #13315C
Primary-light #8DA9C4
Neutral-900   #1F2937
Neutral-500   #64748B
Neutral-300   #CBD5E1
Neutral-100   #F5F7FA
Accent        #E0A458
Success       #15803D
Warning       #B45309
Danger        #B91C1C
```

### 2. Pharma Clean (farma/GMP)
```
Primary       #0F766E
Primary-2     #134E4A
Neutral-900   #0F172A
Neutral-500   #64748B
Neutral-300   #CBD5E1
Neutral-100   #F8FAFC
Accent        #D97706
Success       #15803D · Warning #B45309 · Danger #B91C1C
```

### 3. Industrial Graphite (operativo/planta)
```
Primary       #111827
Primary-2     #374151
Neutral-500   #9CA3AF
Neutral-100   #F3F4F6
Accent        #2563EB
Success #15803D · Warning #B45309 · Danger #B91C1C
```

## Iconografía
- Sets coherentes: **Lucide**, **Phosphor**, **Material Symbols Outlined**.
- Stroke 1.5–2 px. Tamaño en cuadrícula 24/16 px.
- Mismo set en toda la pieza. Nunca mezclar emoji con icon set profesional.

## Data Visualization
**Selección de gráfico:**
| Pregunta | Gráfico |
|---|---|
| ¿Cómo evoluciona X? | Línea |
| ¿Qué compone X? (≤5 partes) | Donut delgado / barra apilada 100% |
| ¿Quién es mayor? | Barra horizontal ordenada |
| ¿Cómo se distribuye X? | Histograma / boxplot |
| 80/20 causas | Pareto (barra + línea acumulada) |
| KPI vs target | Bullet chart |
| Relación X-Y | Scatter |

**Reglas:**
- Eje Y desde 0 (salvo justificación; marcar la ruptura).
- 1 color por serie. Resaltar máximo 1 serie con primary, resto neutro.
- Etiqueta directa > leyenda.
- Decimales mínimos (1 decimal en %, 0 en horas si >10).
- Sin gridlines pesadas: solo horizontales sutiles `#E5E7EB`.
- Sin 3D, sin sombras decorativas, sin texturas.

## Tablas premium
- Sin bordes verticales. Fila header con barra primary y texto blanco.
- Filas alternas en `Neutral-100` (zebra suave) o sin zebra.
- Números alineados a la derecha, *tabular figures*.
- Padding generoso (8–12 px vertical).
- Totales en negrita con barra superior 1 px.

## Excel premium (recetas)
1. Quitar gridlines (View → uncheck Gridlines).
2. Cabeceras: fondo `Primary`, texto blanco, negrita, alto 28.
3. Body: fuente Inter o Calibri 10–11 pt, alto 22, alineación dato (números derecha).
4. Bordes: solo línea horizontal 0,5 pt color `#CBD5E1` bajo cada fila.
5. Números: formato `#,##0` o `0.0%`. Para KPIs: condicional formatting con barras (sin gradiente arcoiris).
6. Sparklines en columna lateral para tendencia.
7. Hoja "README" con leyenda, fuente, fecha, owner.
8. Pestañas con color: gris para datos crudos, primary para resumen, ámbar para inputs.

## Canva premium (recetas)
- Crear **Brand Kit** con la paleta oficial y subir tipografías.
- Usar plantillas **"Corporate / Annual report"** y simplificar (eliminar adornos).
- Reemplazar pictogramas por iconos Lucide/Phosphor importados como SVG.
- Imágenes: solo si añaden información. Preferir ilustraciones planas o foto B/N con overlay primary 80%.
- Exportar PDF print-ready 300 dpi con marcas de corte si es para imprenta.

## PowerPoint premium (recetas)
- Slide master con guías a 64 px del borde, grid 12 col.
- Theme colors = paleta oficial.
- Fuentes en theme: Heading = Inter Bold, Body = Inter Regular.
- Layout obligatorios: Title slide · Section divider · Content 1-col · Content 2-col · KPI dashboard · Closing.
- Footer fijo: `Confidential · Site X · YYYY-MM-DD · Page n`.

## PDF editorial
- Márgenes ≥18 mm.
- Cuerpo en 10 pt, line-height 1.5.
- Pull quotes en serif tamaño +4 pt, color primary.
- Numeración: `Section.Page` (`2.4`).
- Footer con autor, versión, clasificación.

## Power BI tema (extracto JSON)
```json
{
  "name": "MaintenanceExecutiveBlue",
  "dataColors": ["#0B2545","#13315C","#8DA9C4","#E0A458","#64748B","#15803D","#B45309","#B91C1C"],
  "background":"#FFFFFF","foreground":"#1F2937",
  "tableAccent":"#0B2545"
}
```
Guardar como `.json` y aplicar en View → Themes → Browse for themes.

## Checklist de revisión visual
- [ ] 1 mensaje hero por vista.
- [ ] Máx. 2 familias tipográficas, 3 tamaños.
- [ ] Paleta limitada (60/30/10).
- [ ] Sin 3D, sin sombras decorativas.
- [ ] Etiqueta directa en gráficos donde sea posible.
- [ ] Contraste AA verificado.
- [ ] Color nunca como única señal.
- [ ] Números tabulares y decimales mínimos.
- [ ] Whitespace generoso.
- [ ] Footer con confidencialidad / fecha / autor.
