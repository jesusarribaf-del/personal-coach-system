# 🧠 PERSONAL COACH SYSTEM
### Manual operativo · Jesús Arriba · Nine Fitness Cañaveral · Mayo 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> Un co-trabajador de vida que vive en tu Telegram.  
> Lee `memory/` antes de cada respuesta. **No empieza desde cero.**

| | |
|---|---|
| **Acceso** | Telegram → tu bot |
| **Arquitectura** | 11 agentes especializados + 13 archivos de memoria |
| **Coordinador** | `life_coworker` — gestiona todo lo que no sea imagen o reporte |
| **Memoria** | Persistente en GitHub, sincronización cada hora vía HA |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🤖 LOS 11 AGENTES

> No eliges el agente — el sistema lo decide automáticamente según tu mensaje.  
> Saber qué hay detrás te ayuda a formular mejor la pregunta.

| Agente | Emoji | Cuándo entra | Ejemplo de activación |
|--------|-------|--------------|----------------------|
| **Life Coworker** | 🧠 | Cualquier texto general | Coordinador principal |
| **Strength Coach** | 🏋️ | Entreno, progresión, lesiones | `"Sentadilla me chirría la rodilla, ¿qué hago?"` |
| **Nutrition Coach** | 🥗 | Comida, batch cooking, proteína | `"Desayuno con 40g proteína en 5 min"` |
| **Sleep & Recovery** | 💤 | Sueño, VFC, fatiga, decisión de entreno | `"VFC 38ms, toca piernas, ¿voy?"` |
| **Meditation Guide** | 🧘 | Ansiedad, calma, presencia | `"3 días sin dormir bien desde que dejé el cannabis"` |
| **Decision Advisor** | 🎯 | Decisiones con incertidumbre real | `"¿Boxeo en junio o espero a julio?"` |
| **Motivation Coach** | 🔥 | Sin ganas, hábitos, bloqueos | `"Son las 6pm y me da igual todo"` |
| **Productivity Builder** | 📋 | Rutinas, organización, planificación | `"Estructúrame la semana con Rovi a las 7h"` |
| **Identity Coach** | 🌟 | Propósito, valores, patrones repetitivos | `"¿Por qué sigo cayendo en el mismo patrón?"` |
| **Memory Curator** | 🗂️ | Actualizaciones de memoria | `"Añade que pesé 81.2 kg hoy"` |
| **Report Designer** | 📊 | Reportes, balances, análisis de datos | `/reporte` o `"dame un informe semanal"` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⌨️ COMANDOS DEL BOT

```
/start          →  Estado del sistema + resumen de comandos
/agentes        →  Lista de los 11 agentes activos
/memoria        →  Muestra perfil + objetivos (personal-profile.md + goals-roadmap.md)
/actualizar     →  Fuerza git pull desde GitHub (sync inmediata)
/reporte        →  Reporte completo integrado
/reporte semanal    →  Balance de la semana con veredicto
/reporte mensual    →  Análisis de 4 semanas con evolución de marcas
/reporte entreno    →  Progresión de fuerza + estado mesociclo
/reporte nutricion  →  Adherencia proteica + TDEE real vs consumo
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📅 FLUJOS DEL DÍA A DÍA

---

### 🌅 MAÑANA — antes de salir de casa

**Mensaje tipo:**
```
VFC hoy: 42ms · sueño: 6.5h · energía: 6
Hoy toca Push. ¿Voy normal o ajusto algo?
```

**Qué recibe:**  
Sleep/Recovery cruza tu VFC con el baseline (`44ms`) → luz verde, ajuste de RPE, o sustitución por Z1 si hay fatiga.

**Regla dura del sistema:**
| Señal | Acción automática |
|-------|-----------------|
| `VFC < 38ms` ó `sueño < 6h` | Cardio duro → Z1 · Fuerza → bajar RPE 1 punto |
| `VFC 38-44ms` | Entreno normal, vigilar fatiga acumulada |
| `VFC > 44ms` | Verde completo |

---

### 💪 PRE-ENTRENO — en el vestuario o de camino

**Mensaje tipo:**
```
A punto de hacer Push. Última banca: 65kg x8 (4ª serie, 05/05).
Dormí 7h, VFC 49ms. ¿Intento 67.5kg o consolido?
```

**Regla de doble progresión aplicada automáticamente:**  
✅ Todas las series en rango alto con RIR objetivo → **sube `+2.5 kg`**  
⚠️ Alguna serie sin completar → **consolida mismo peso**  
❌ Fallo o dolor → **ajuste o revisión técnica**

---

### 📊 POST-ENTRENO — nada más terminar

**Mensaje tipo:**
```
Sesión Push completada.
Banca: 65x8 / 65x8 / 65x7 · RIR 3/2/1
Incline DB: 22x10 / 22x8 / 24x6
Hombro: sin molestias · Energía final: 7/10
```

**Qué recibe:**  
Registro en `training-progress.md`, análisis de progresión, alerta si hay señal a vigilar (hombro derecho, fatiga acumulada, semana de descarga próxima).

---

### 🏃 POST-CARDIO — después de cinta

**Mensaje tipo:**
```
Z2 completado: 42min · FC media: 137lpm · km: 5.2
Empecé corriendo pero a los 25min bajé ritmo para no salirme de zona.
```

**Objetivo en progreso:** `→ 40min continuos en Z2 (130-145 lpm)` · Julio 2026  
El sistema trackea sesión a sesión cuánto te falta.

---

### 🍳 BATCH COOKING — antes de cocinar

**Mensaje tipo:**
```
Batch cooking hoy. Tengo: pollo, huevos, arroz, pasta, tomates, queso.
Dame 4 recetas para preparar en freidora de aire con proteína en cada comida.
Sin brócoli ni coliflor.
```

**Qué recibe:**  
Menú con cantidades, tiempo real de prep y distribución proteica del día. El sistema sabe: tienes freidora de aire, presupuesto `60€/semana`, y el desayuno es tu agujero proteico principal.

---

### 😤 CUANDO NO TIENES GANAS

**Mensaje tipo:**
```
Son las 6pm, llevo en casa todo el día, no tengo energía para nada.
Toca Upper+ pero me da igual todo. ¿Voy o no voy?
```

**Qué NO recibe:** "¡Tú puedes!" — diagnóstico real: ¿fatiga acumulada (VFC, sueño) o resistencia mental?  
**Qué SÍ recibe:** Versión mínima viable de la sesión — o razón concreta para descansar.

---

### 🎯 DECISIONES DIFÍCILES

**Mensaje tipo:**
```
Estoy pensando en empezar boxeo en junio pero la base cardio aún no está consolidada.
¿Tiene sentido o espero a julio como tenía planeado?
```

**Estructura de respuesta:** `deseo / miedo / evidencia / estrategia` — escenarios con pros/contras basados en TU situación, no genéricos.

---

### 📸 CAPTURAS DE APPS

El bot acepta fotos directamente. Sin escribir nada.

| Captura | Qué hace el sistema |
|---------|-------------------|
| AutoSleep (VFC + sueño) | Análisis de recuperación sin teclear nada |
| Jefit post-sesión | Extrae datos de entrenamiento automáticamente |
| Apple Health tendencias | Seguimiento de composición y actividad |
| Foto de comida | Estimación nutricional rápida |
| Ticket de supermercado | Análisis de compra y balance proteico |

**Ejemplo mínimo viable:**  
> `[foto AutoSleep]` + `"¿Entreno fuerte hoy o ajusto?"` → respuesta en ~15 segundos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🗂️ QUÉ RECUERDA EL SISTEMA

| ✅ Sabe siempre | ❌ No sabe (a menos que lo registres) |
|----------------|--------------------------------------|
| Tus marcas de fuerza y su evolución | Lo que comiste ayer |
| Tu VFC media `44ms` · pico histórico `99ms` | Tu estado de ánimo hoy |
| Protocolo Allen Carr · cese previsto `11/05` | Si entrenaste ayer |
| Zonas cardio · Z2 `130-145 lpm` · FC máx `178 lpm` | El contenido exacto de conversaciones anteriores |
| Objetivo julio: banca `67-70kg` · squat `90-95kg` · jalón `110kg` | |
| Hombro derecho con historial · face pull inamovible | |
| Déficit proteico · objetivo `164-180g/día` · actual `~120g` | |
| Aversiones: brócoli, coliflor, bacalao | |
| Patrón de riesgo: disciplina alta en rachas | |
| Rovi `14/05` como punto de ruptura potencial | |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📝 CUÁNDO ACTUALIZAR MEMORIA MANUALMENTE

Dile directamente en Telegram. El Memory Curator lo gestiona.

| Evento | Qué escribir |
|--------|-------------|
| Nuevo récord | `"Banca hoy: 67.5 kg x8 — nuevo récord"` |
| Cambio de peso `> 1 kg` | `"Peso hoy: 80.4 kg en ayunas"` |
| Lesión o molestia nueva | `"Dolor en rodilla derecha al agacharme desde hoy"` |
| Día 1 sin cannabis | `"Hoy es el día 1 oficial sin cannabis"` |
| Cambio de horario | `"Desde el 14/05 entreno a las 16:30 después de Rovi"` |
| Inicio del boxeo | `"Empecé boxeo en [gimnasio], 2 días/semana"` |
| Fin de mesociclo | `"Semana de descarga completada. Mesociclo 2 empieza el lunes"` |

**Dos vías de actualización:**

```
VÍA TELEGRAM (inmediato)
  Escribe al bot → Memory Curator propone el cambio → confirmas con "sí"

VÍA CLAUDE CODE / GITHUB (revisiones grandes)
  Edita memory/*.md → commit + push → bot lo lee en el próximo mensaje
  Forzar sync: /actualizar
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚡ TIPS — CÓMO SACARLE MÁS

**① Empieza con datos, no con preguntas:**
```
❌  "Dame una rutina de hoy"
✅  "VFC 45ms · sueño 7h · toca Pull. Pesos de la semana pasada ajustados si procede."
```

**② Los números cambian la respuesta:**
```
❌  "Estoy cansado"
✅  "VFC hoy 36ms, ayer 42ms. 3 noches con menos de 6.5h desde que dejé el cannabis."
```

**③ Las fotos son más rápidas que escribir:**  
`[AutoSleep] + "¿voy?"` → el sistema lee la imagen y decide

**④ Usa el tiempo real como contexto:**
```
"Son las 6pm, acabo de llegar de Rovi, cena en 2h.
Dame algo proteico que tarde 15 min y tengo huevos + arroz."
```

**⑤ Para batch cooking — dile lo que tienes, no lo que quieres:**
```
"Tengo: pollo, huevos, arroz, tomates, queso.
Batch cooking de 90 min. Hazme algo con lo que hay."
```

**⑥ Si quieres respuesta corta:**
```
"Dame solo la conclusión y el plan en 3 pasos."
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚫 LO QUE EL SISTEMA NO HACE

| Límite | Qué hacer en su lugar |
|--------|-----------------------|
| No diagnóstico médico | Dolor agudo, lesión, síntomas graves → **médico o fisio** |
| No sustituye a profesionales | Nutricionista clínico, psicólogo, endocrino → **profesional** |
| No inventa datos | Si no está registrado, te lo pregunta o indica que falta |
| No da motivación vacía | Si algo no tiene sentido, lo dice directamente |
| No hace planes imposibles | Todo propuesto considera horario, presupuesto y contexto real |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📆 SEMANA TIPO — EJEMPLO COMPLETO

```
LUNES  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  07:30  "VFC: 46ms · sueño: 7h · Push hoy. ¿Subo banca?"
  17:00  Entreno Push — Nine Fitness
  19:30  "Push: banca 67.5x8/8/7 · incline 24x10/9/8 · hombro bien"

MARTES  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  07:30  "VFC: 44ms · sueño: 6.5h · Pull hoy. Normal."
  17:00  Entreno Pull
  19:30  "Pull: jalón 102.5kg ✅ · curl inclinado subí a 14kg"

MIÉRCOLES  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  09:00  [foto AutoSleep] "Z2 en cinta. ¿A qué ritmo para quedarme en 130-145?"
  10:00  Cinta 45 min Z2
  19:00  Batch cooking → "Dame menú 4 días con lo que tengo"

JUEVES  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  08:00  "VFC: 41ms · sueño: 6h · Toca piernas. ¿Bajo volumen?"
  17:00  Entreno Legs

VIERNES  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  09:30  HIIT 25 min cinta
  21:00  "No he comido bien hoy. ¿Qué ceno para compensar proteína?"

SÁBADO  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  10:00  Entreno Upper+
  resto  Descanso / vida personal

DOMINGO  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  09:00  Z2 45 min (o descanso si VFC < 40ms)
  18:00  Batch cooking
  19:00  "/reporte semanal" → balance completo de la semana
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 HITOS CRÍTICOS

| Fecha | Evento | Acción |
|-------|--------|--------|
| **11/05 lun** | 🚭 Cese cannabis (previsto Allen Carr) | Avisar al sistema ese mismo día: `"Hoy es día 1 sin cannabis"` |
| **14/05 jue** | 🏢 Inicio Rovi `7:00-15:00h` | Confirmar horario real + actualizar memoria |
| **~09/06 lun** | 🔄 Deload — semana 6 | Reducir volumen `40%` · mantener pesos · 1 semana |
| **Jul 2026** | 📊 Revisión de marcas objetivo | Banca `67-70kg` · Squat `90-95kg` · Jalón `110kg` · Z2 `40min` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Última actualización: 08/05/2026 · Personal Coach System v2*
