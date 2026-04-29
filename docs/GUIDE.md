# Guía de uso — Maintenance Intelligence System

Guía maestra para sacar el máximo partido al sistema. Léela una vez. Después, usa los comandos slash o llama al agente principal.

## 1. ¿Qué es este sistema?
Un **compañero de trabajo senior**, no un coach: un agente principal `maintenance-co-worker` y 10 subagentes especialistas que producen entregables ejecutables (reportes, RCA, A3, CAPA, emails, dashboards, automatizaciones).

Pensado para tu rol: **Site Manager / Responsable de Mantenimiento Industrial** en farma / Tetra Pak.

## 2. Capacidades que ganas
- **Reportes ejecutivos** diarios, semanales y mensuales con calidad consultora.
- **Análisis de datos** de CMMS (SAP PM, Maximo, Infor) sin tener que limpiar tú.
- **RCA, FMEA, A3, 5 Why** estructurados en minutos.
- **GMP**: borradores de desviación, CAPA, change control, GMP impact assessment (todos marcados para revisión QA).
- **Liderazgo**: feedback SBI, 1:1, agendas de reunión, evaluaciones, planes de desarrollo.
- **Automatización**: Excel avanzado, Power Query, Power Automate, Python.
- **Comunicación ES/EN**: emails y memos profesionales BLUF.
- **Seguridad**: LOTO, JSA, ATEX, permisos.
- **Diseño visual premium**: Canva, PPT, PDF, Excel y Power BI con estándar consultora top.
- **Base de conocimiento**: lecciones aprendidas, OPL, glosario.

## 3. Estructura del proyecto
```
.claude/
  agents/                  # 1 principal + 10 subagentes
  commands/                # 15 comandos slash
docs/
  references/              # Glosario, reglas calidad, design system, patrones multi-agente
  templates/               # A3, RCA, CAPA, FMEA, daily, weekly, etc.
  examples/                # Ejemplos resueltos
  GUIDE.md                 # Este documento
data/
  raw/                     # Pones aquí CSV/Excel originales
  processed/               # El sistema deja aquí los datasets limpios
reports/
  drafts/                  # Borradores generados por el sistema
  final/                   # Mueves aquí cuando esté aprobado
playbooks/                 # Procedimientos y lecciones aprendidas
  maintenance/ lean/ gmp/ leadership/ automation/
CLAUDE.md                  # Instrucciones del proyecto (las lee Claude)
README.md
```

### ¿Dónde añado yo cosas? — Regla rápida
| Quiero añadir… | Va en… |
|---|---|
| CSV/Excel del CMMS, exports, históricos | `data/raw/` |
| Datasets limpios (lo hace el sistema) | `data/processed/` |
| Manuales OEM, fichas técnicas, especificaciones de equipo | `docs/references/` |
| SOPs, procedimientos internos, normativas | `docs/references/` |
| Plantillas corporativas (logos, paletas, fuentes) | `docs/references/branding/` (créala) |
| Ejemplos de reportes que te gustan (referencia visual) | `docs/examples/` |
| Reportes pasados ya finales (histórico) | `reports/final/` |
| Lecciones aprendidas, OPLs, mejores prácticas | `playbooks/{area}/` |
| Capturas, fotos de planta, diagramas | `docs/references/assets/` (créala) |

> Cualquier cosa que pongas en `docs/` o `playbooks/` el sistema la podrá leer y citar como fuente.

## 4. Cómo usar el sistema (3 modos)
### Modo A — Comando slash directo (recomendado)
Escribes `/<comando>` con un argumento corto. El comando lanza al/los subagente(s) correctos con la plantilla adecuada.

Ejemplos:
- `/daily-report 2026-04-29 línea TBA-3`
- `/downtime-analysis data/raw/2026-04_downtime.csv abril`
- `/rca llenadora L3, evento 27-abr 14:32, 2 lotes afectados`
- `/a3 paradas no programadas en línea TBA-3`
- `/gmp-impact-assessment sustitución sensor presión autoclave AC-02`
- `/capa-draft DEV-2026-041 fallo sealing horizontal`
- `/stakeholder-email HQ, retraso PM crítico 2 semanas, EN`
- `/team-feedback técnico Juan, llegadas tarde, correctivo`
- `/weekly-maintenance-review semana 17`
- `/visual-report monthly board pack, audiencia HQ, 16:9`
- `/automation-idea consolidar exports SAP semanales`
- `/executive-summary reports/drafts/2026-04-29_rca_TBA3.md EN`

### Modo B — Llamada libre al agente principal
Escribes en lenguaje natural. El principal reformula, elige subagentes y entrega.

Ejemplos:
- *"Tengo un downtime alto en la TBA-3 este mes. Analízalo y dame plan."*
- *"Prepárame el 1:1 con el supervisor de turno noche, hay tensión con producción."*
- *"Necesito un email firme pero diplomático al proveedor X por retraso de repuesto."*

### Modo C — Multi-agente explícito
Pides expresamente colaboración:
- *"Lanza data-analyst + reliability en paralelo y luego pasa a gmp."*
- *"Revisa este A3 con safety y gmp en panel."*

Ver `docs/references/multi-agent-patterns.md`.

## 5. Flujo recomendado para una tarea típica
1. **Pones los datos crudos** en `data/raw/YYYY-MM-DD_origen_descripcion.csv`.
2. **Lanzas un comando slash** (ej. `/downtime-analysis`).
3. El sistema **calcula KPIs**, deja dataset limpio en `data/processed/` y borrador en `reports/drafts/`.
4. **Iteras** con feedback corto (*"resalta más el riesgo de seguridad"*, *"versión EN para HQ"*).
5. Cuando esté aprobado, **mueves** a `reports/final/`.
6. **Pides al curador**: *"Captura la lección aprendida en playbooks/maintenance"*.

## 6. Diseño visual premium (estándar)
Cada output gráfico sigue `docs/references/premium-design-system.md`:
- Paletas profesionales (Executive Blue / Pharma Clean / Industrial Graphite).
- Tipografía editorial (Inter + Source Serif Pro).
- Grid 12 columnas, jerarquía clara, whitespace generoso.
- Data viz a la Tufte (sin 3D, etiqueta directa, paleta limitada).
- Recetas de construcción para Canva, PowerPoint, Excel, PDF y Power BI.

Si tu empresa tiene **branding corporativo**, créame `docs/references/branding/` con:
- `palette.md` (hex de colores corporativos),
- `fonts.md` (tipografías oficiales),
- `logos/` (PNG/SVG),
- `examples/` (1-2 reportes corporativos previos como referencia).

El sistema los respetará automáticamente.

## 7. Reglas críticas que ya están integradas
- Nunca inventa datos. Marca `[DATO PENDIENTE]` con la fuente sugerida.
- Separa Hechos / Hipótesis / Suposiciones cuando hay incertidumbre.
- Priorización: **Seguridad > Calidad/GMP > Producción > Coste**.
- Cualquier output con impacto regulatorio lleva `⚠ Requiere QA review`.
- Estructura ejecutiva de 10 puntos (Contexto → Riesgos).
- ES por defecto, EN profesional B2-C1 cuando se pida.

## 8. Cómo darle el máximo partido (tips)
- **Alimenta el contexto**: cuanto más sepa el sistema de tu planta (líneas, equipos críticos, KPIs target, organigrama), mejor. Crea `docs/references/site-context.md` con esa info.
- **Branding**: súbele tu paleta y tipografía corporativa una vez; las usará siempre.
- **Histórico**: guarda reportes pasados en `reports/final/`. El curador puede usarlos para detectar tendencias.
- **Lecciones**: tras cada incidente serio, pídele *"capturar lección aprendida"*. Estás construyendo tu propia knowledge base.
- **Itera corto**: en lugar de pedir el documento perfecto, pide un borrador 80% y refina con 2-3 iteraciones cortas.
- **Usa multi-agente**: en temas complejos pide explícitamente *"panel de revisión"* o *"cadena completa"*.
- **Feedback continuo**: si un output no tiene el tono que quieres, dilo. El sistema lo recordará si lo capturas en `CLAUDE.md`.

## 9. Qué pedir cuando no sabes qué pedir
Cuatro arranques útiles:
1. *"Hazme el reporte semanal con los datos de `data/raw/...`."*
2. *"Tengo este problema: [1 frase]. ¿Cómo lo abordamos?"*
3. *"Prepara mi 1:1 / mi reunión con dirección sobre [tema]."*
4. *"Convierte este análisis en un one-pager premium para HQ."*

## 10. Próximos pasos sugeridos
- [ ] Subir 1 export real del CMMS a `data/raw/` y lanzar `/downtime-analysis`.
- [ ] Crear `docs/references/site-context.md` con líneas, equipos críticos, KPI targets.
- [ ] Crear `docs/references/branding/` con paleta y tipografía corporativas (si aplica).
- [ ] Probar `/weekly-maintenance-review` con la semana en curso.
- [ ] Probar `/visual-report` para un one-pager mensual a HQ.
