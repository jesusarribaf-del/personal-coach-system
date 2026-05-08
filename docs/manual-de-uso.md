# Manual de uso — Personal Coach System
### Jesús Arriba · Nine Fitness Cañaveral · Mayo 2026

---

## ¿Qué es este sistema?

Un co-trabajador de vida personal que vive en tu Telegram. No es una app de fitness. No es un chatbot genérico. Es un sistema con **memoria de ti** — sabe tu historial de entrenamiento, tus marcas, tu VFC, tu protocolo Allen Carr, tu déficit proteico, y que el hombro derecho tiene historial.

Cada vez que hablas con él, lee tu `memory/` antes de responder. No empieza desde cero.

**Coordinador central:** `personal-life-co-worker`
**Acceso:** Telegram → [@tu_bot]

---

## Los 9 agentes y cuándo usarlos

> No tienes que elegir el agente — el sistema lo hace. Pero saber qué hay detrás te ayuda a formular mejor la pregunta.

| Agente | Para qué sirve | Ejemplo real |
|--------|---------------|--------------|
| **Strength Coach** | Entreno, progresión, técnica, lesiones | "Hoy sentadilla me chirría la rodilla, ¿qué hago?" |
| **Nutrition Coach** | Qué comer, batch cooking, proteína | "Dame un desayuno con 40g de proteína que prepare en 5 min" |
| **Sleep & Recovery** | Sueño, fatiga, VFC, si entrenar hoy | "VFC hoy 38ms, tengo piernas programado, ¿voy?" |
| **Meditation & Mindfulness** | Calma, presencia, gestión ansiedad | "Llevo 3 días sin dormir bien desde que dejé el cannabis" |
| **Decision Advisor** | Decisiones con incertidumbre | "¿Empiezo a hacer boxeo antes o después de que baje el % grasa?" |
| **Motivation & Discipline** | Cuando no tienes ganas, hábitos | "No me apetece nada entrenar hoy y son las 5pm" |
| **Productivity Builder** | Rutinas, organización, planificación semanal | "Ayúdame a estructurar la semana con el horario de Rovi" |
| **Identity & Life Design** | Propósito, valores, quién quieres ser | "¿Por qué sigo cayendo en el mismo patrón con el cannabis?" |
| **Memory Curator** | Actualizar o consultar tu memoria | "Añade que hoy pesé 81.2 kg en ayunas" |

---

## Comandos del bot

| Comando | Qué hace |
|---------|----------|
| `/start` | Saludo + estado del sistema |
| `/agentes` | Lista todos los agentes disponibles |
| `/memoria` | Muestra el estado actual de tu memoria |
| `/actualizar` | Fuerza un `git pull` — sincroniza cambios desde GitHub |

---

## Flujos de trabajo del día a día

---

### 🌅 MAÑANA — antes de salir de casa

**Qué mandarle:**
```
VFC hoy: [X] ms · sueño: [Xh] · energía (1-10): [X]
```

**Ejemplo real:**
```
VFC hoy: 42ms · sueño: 6.5h · energía: 6
Hoy toca Push. ¿Voy normal o ajusto algo?
```

**Qué esperar:** El agente de sleep/recovery cruza tu VFC con el histórico (media 44ms) y te da luz verde, ajuste de intensidad, o te dice que sustituyas por Z2 suave si hay señal de fatiga.

**Regla del sistema:** Si VFC < 38ms o sueño < 6h → cardio duro se convierte en Z1, entrenamiento de fuerza se hace pero bajando RPE objetivo en 1 punto.

---

### 💪 PRE-ENTRENO — en el vestuario o de camino

**Qué mandarle:**
```
A punto de hacer [día de rutina]. Peso de trabajo previo en [ejercicio]: [X kg].
¿Subo o mantengo hoy?
```

**Ejemplo real:**
```
A punto de hacer Push. Última banca: 65kg x8 (4ª serie, 05/05).
Dormí 7h, VFC 49ms. ¿Intento 67.5kg hoy o consolido?
```

**Qué esperar:** El strength coach aplica la regla de doble progresión: si completaste todas las series en el rango alto con el RIR objetivo → sube. Si no → consolida.

---

### 📊 POST-ENTRENO — nada más terminar

**Qué mandarle (formato Jefit resumido):**
```
Sesión completada: [día]
Banca: 65x8 / 65x8 / 65x7 / 65x6 · RIR s1:3 s2:2 s3:1 s4:0
[otros ejercicios clave]
Sensación general: [X/10]
```

**Ejemplo real:**
```
Sesión Push completada.
Banca: 65x8/65x8/65x7 · RIR 3/2/1
Incline DB: 22x10/22x8/24x6
Hombro: sin molestias. Energía al final: 7/10.
```

**Qué esperar:** Registro en memoria de entrenamiento, feedback sobre progresión, y alerta si hay algo a vigilar (p.ej. hombro).

---

### 🏃 POST-CARDIO — después de cinta

**Qué mandarle:**
```
Z2 completado: [X] min · FC media: [X] lpm · km: [X]
```

**Ejemplo real:**
```
Z2 completado: 42min · FC media: 137lpm · km: 5.2
Empecé corriendo pero a los 25min tuve que bajar ritmo para no salirme de zona.
```

**Qué esperar:** Tracking de progresión hacia objetivo julio (40min continuos). El sistema te irá diciendo cuánto te falta.

---

### 🍳 COCINA — antes del batch cooking

**Qué mandarle:**
```
Batch cooking domingo. Tengo: [ingredientes].
Presupuesto: ~30€. Dame menú para 3-4 días con foco en proteína.
```

**Ejemplo real:**
```
Batch cooking hoy. Tengo pollo, huevos, arroz, pasta, tomates, queso.
Dame 4 recetas para preparar hoy que me den proteína en cada comida.
Sin brócoli ni coliflor.
```

**Qué esperar:** Menú concreto con cantidades, tiempo estimado de prep, y la distribución proteica del día resultante. El sistema sabe que tienes freidora de aire y que el desayuno es tu agujero proteico.

---

### 😤 CUANDO NO TIENES GANAS

**Qué mandarle — sin filtros:**
```
No me apetece nada entrenar hoy. [contexto real de por qué]
```

**Ejemplo real:**
```
Son las 6pm, llevo en casa todo el día, no tengo energía para nada.
Toca Upper+ pero me da igual todo. ¿Voy o no voy?
```

**Qué esperar:** El agente de motivación NO te va a decir "¡tú puedes!". Va a diagnosticar si es fatiga real (VFC, sueño) o resistencia mental, y darte la versión mínima viable de la sesión. A veces la respuesta es: ve y haz solo los compuestos. A veces es: descansa. Siempre con razón concreta.

---

### 🧠 DECISIONES DIFÍCILES

**Qué mandarle:**
```
Tengo que decidir sobre [tema]. Contexto: [situación real].
```

**Ejemplo real:**
```
Estoy pensando en empezar boxeo en junio pero la base cardio aún no está consolidada.
¿Tiene sentido o espero a julio como tenía planeado?
```

**Qué esperar:** El agente de decisiones separa deseo / miedo / evidencia / estrategia. Te da escenarios con pros y contras reales basados en TU situación, no genéricos.

---

### 📸 MANDAR CAPTURAS DE APPS

El bot acepta fotos directamente. Úsalo para:

| Qué mandar | Por qué |
|------------|---------|
| Captura AutoSleep con VFC y sueño | Registro sin escribir nada |
| Captura Jefit post-sesión | El sistema extrae los datos |
| Captura Apple Health tendencias | Seguimiento de composición |
| Foto de comida o ticket de supermercado | Análisis nutricional rápido |

**Ejemplo:**
> [foto de la pantalla de AutoSleep]
> "¿Entreno fuerte hoy o ajusto?"

---

## Cómo se actualiza la memoria

La memoria en `memory/` es lo que el sistema lee en cada conversación. Hay dos formas de actualizarla:

**Vía Telegram (inmediato):**
```
Añade a mi memoria que hoy pesé 80.8 kg en ayunas.
```
```
Actualiza que mi sentadilla ahora es 85kg x6.
```

**Vía Claude Code / GitHub (sesiones de onboarding o revisiones grandes):**
Los archivos `.md` en `memory/` se editan directamente, se hace commit y push, y el bot los lee en el próximo mensaje.

**El bot se sincroniza con GitHub cada hora** (automation en HA). Si necesitas forzar la sync: `/actualizar`

---

## Qué recuerda el sistema

| ✅ Recuerda | ❌ No recuerda (todavía) |
|------------|------------------------|
| Tus marcas de fuerza y su evolución | El contenido exacto de cada conversación anterior |
| Tu protocolo Allen Carr y fecha de cese | Lo que comiste ayer (a menos que lo registres) |
| Tu VFC media y pico histórico | Tu estado de ánimo si no lo dices |
| Tus zonas cardio y objetivo julio | Si entrenaste ayer si no lo registras |
| Tu hombro derecho y el face pull como inamovible | |
| Tu déficit proteico y objetivo 150-165g/día | |
| Que no te gustan brócoli, coliflor ni bacalao | |
| Que el cannabis fue tu factor más diferenciador | |
| Que el patrón de riesgo es disciplina alta en rachas | |
| Que Rovi empieza el 14/05 como punto de ruptura potencial | |

---

## Lo que el sistema NO hace

- **No diagnostica médicamente** — dolor agudo, lesión, síntomas físicos o mentales graves → médico o fisio
- **No sustituye a profesionales** — nutricionista clínico, psicólogo, endocrino
- **No inventa datos** — si no tienes registrado algo, te lo pregunta
- **No te da motivación vacía** — si algo no tiene sentido, te lo dice
- **No hace planes imposibles** — todo lo que proponga tiene en cuenta tu horario, presupuesto y contexto real

---

## Tips para sacarle más partido

**1. Empieza el mensaje con contexto:**
> ❌ "Dame una rutina"
> ✅ "Hoy VFC 45ms, dormí 7h, toca Pull. Dame la rutina con los pesos de la semana pasada ajustados si procede."

**2. Sé específico con los números:**
> ❌ "Estoy cansado"
> ✅ "VFC hoy 36ms, ayer 42ms. Llevo 3 noches durmiendo menos de 6.5h desde que dejé el cannabis el lunes."

**3. Las fotos son más rápidas que escribir:**
Captura de AutoSleep + "¿voy?" → respuesta en 15 segundos.

**4. Usa el contexto de tiempo real:**
> "Son las 6pm, acabo de llegar de Rovi, cena en 2h. Dame algo proteico que tarde 15 min."

**5. Para batch cooking — dile lo que tienes, no lo que quieres:**
> "Tengo estos ingredientes: [lista]. Haz algo con lo que hay."

**6. Si la respuesta es larga y no la quieres:**
> "Dame solo la conclusión y el plan en 3 pasos."

---

## Cuándo actualizar manualmente la memoria

Hay momentos donde vale la pena decirle al sistema que actualice algo importante:

| Evento | Qué decirle |
|--------|-------------|
| Nuevo récord en un ejercicio | "Actualiza mi marca de banca: 67.5 kg x8 hoy" |
| Cambio de peso (+/- 1.5 kg) | "Peso hoy: 80.4 kg en ayunas" |
| Lesión o molestia nueva | "Tengo dolor en rodilla derecha al agacharme desde hoy" |
| Cese del cannabis completado | "Hoy es el día 1 oficial sin cannabis" |
| Cambio de horario o rutina | "Desde el 14/05 entreno a las 16:30 después de Rovi" |
| Inicio del boxeo | "Empecé boxeo en [gimnasio], 2 días/semana" |

---

## Flujo semanal completo — ejemplo tipo

```
LUNES
  07:30 → WhatsApp: "VFC: 46ms · sueño: 7h · Push hoy. ¿Subo banca?"
  17:00 → Entreno Push en Nine Fitness
  19:30 → "Push completado: banca 67.5x8/8/7, incline 24x10/9/8. Hombro bien."

MARTES
  07:30 → "VFC: 44ms · sueño: 6.5h · Pull hoy. Normal."
  17:00 → Entreno Pull
  19:30 → "Pull completado. Jalón 102.5 kg completado. Curl inclinado subí a 14kg."

MIÉRCOLES
  09:00 → [foto AutoSleep] "Z2 en cinta hoy. ¿A qué ritmo para quedarme en 130-145?"
  10:00 → Cinta 45 min
  19:00 → Batch cooking · "Dame menú para 4 días con lo que tengo"

JUEVES
  08:00 → "VFC: 41ms · sueño: 6h. Toca piernas. ¿Bajo el volumen?"
  17:00 → Entreno Legs

VIERNES
  09:30 → HIIT 25 min cinta
  21:00 → "No he comido bien hoy, ¿qué ceno para compensar proteína?"

SÁBADO
  10:00 → Entreno Upper+
  Resto → Descanso / vida personal

DOMINGO
  09:00 → Z2 45 min (o descanso si VFC baja)
  18:00 → Batch cooking
  19:00 → Revisión semanal: "¿Cómo fue la semana? ¿Qué ajusto?"
```

---

## Hitos críticos próximos

| Fecha | Evento | Qué hacer |
|-------|--------|-----------|
| **11/05 (lun)** | Cese cannabis (previsto) | Avisarle al sistema ese mismo día |
| **14/05 (jue)** | Inicio Rovi (7:00-15:00h) | Confirmar horario real y actualizar memoria |
| **~09/06 (lun)** | Deload semana 6 de rutina | Reducir 40% volumen, mismos pesos |
| **Jul 2026** | Revisión de marcas objetivo | Banca 67-70 · Squat 90-95 · Jalón 110 · Z2 40min |

---

*Última actualización: 08/05/2026 — onboarding completado*
