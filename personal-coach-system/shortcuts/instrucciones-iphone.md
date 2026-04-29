# Shortcuts iPhone — instrucciones de configuración

> Cuatro Shortcuts más una Automation diaria. Configurarlos te lleva ~20 minutos una vez. Después, fricción mínima diaria.

## Pre-requisitos

1. **App Atajos** (iOS, viene preinstalada).
2. **App Claude** (iOS) instalada y logueada con tu cuenta Pro.
3. **App Working Copy** (gratis para uso básico) o **a-Shell** — para sincronizar memoria con GitHub desde el móvil. Alternativa más simple: usar la app de **GitHub** + edición de archivos vía web.
4. Una carpeta en **iCloud Drive**: `Atajos/CoachPersonal/` con subcarpetas `logs/` y `temp/`.

## Acción base: "Preguntar a Claude"

iOS Shortcuts incluye desde finales de 2024 la acción **"Ask Claude"** del app oficial (requiere Pro). Si no aparece en tu lista de acciones, actualiza la app de Claude.

Esta acción acepta:
- Texto del prompt
- Archivos adjuntos (imágenes, PDF, .md)
- Devuelve el texto de la respuesta

Si tu versión de Claude iOS aún no expone la acción, alternativa: el Shortcut **abre la app Claude con el prompt ya escrito en el portapapeles** (1 tap pegar + enviar). No es 100% automatizado pero es 5 segundos.

---

## Shortcut 1 — "Check-in mañana"

**Cuándo se ejecuta**: automáticamente cada día a las 07:00 (ajusta a tu hora real de despertar) vía Personal Automation.

**Pasos**:
1. *Show Alert*: "Check-in matinal — ¿listo?" (botones: Sí / Más tarde).
2. Si Sí: *Get File* desde iCloud `CoachPersonal/plantillas/check-in-matinal.md`.
3. *Ask for Input* (Texto): "Sueño anoche (horas + calidad 1–10)".
4. *Ask for Input*: "Energía y ánimo (1–10 cada uno)".
5. *Ask for Input*: "Día Allen Carr y estado".
6. *Ask for Input*: "Plan tentativo de entreno hoy".
7. *Combine Text*: monta el prompt con la plantilla + las inputs.
8. *Ask Claude* con el texto resultante. Project: "Coach Personal".
9. *Show Result* en notificación rica.
10. *Save to Files*: guarda la respuesta en `CoachPersonal/temp/checkin-{fecha}.md` (luego se consolidará en el cierre).

---

## Shortcut 2 — "Diagnóstico entreno"

**Cuándo**: tú lo lanzas tras entrenar, desde el Share Sheet de la captura de Jefit/Workouts (2 taps: Compartir → Diagnóstico entreno).

**Pasos**:
1. *Receive Image* (input desde Share Sheet).
2. *Get File* `plantillas/diagnostico-entreno.md`.
3. *Ask for Input*: "Sensaciones (RIR, técnica, dolor, energía)".
4. *Combine Text*: plantilla + sensaciones.
5. *Ask Claude* (texto + imagen adjunta) en Project Coach Personal.
6. *Show Result*.
7. *Append to File* `CoachPersonal/temp/entrenos-{fecha}.md`.

---

## Shortcut 3 — "Cierre del día"

**Cuándo**: automáticamente a las 23:00 vía Personal Automation. iOS pedirá una confirmación de 1 segundo (limitación de la plataforma).

**Pasos**:
1. *Get File* `plantillas/cierre-dia.md`.
2. *Ask Claude* (sólo el texto de la plantilla — Claude tiene en su Project la conversación del día).
3. *Get text from*: extraer JSON de la respuesta (acción "Match Text" con regex `\{[\s\S]*\}`).
4. *Get Current Date* → formato `YYYY-MM-DD`.
5. *Save to Files*: `CoachPersonal/logs/log-{fecha}.md` con contenido = plantilla de log + JSON dentro.
6. *Show Notification*: "✅ Día cerrado — log guardado".
7. *(Opcional avanzado)*: si tienes Working Copy configurada con repo `personal-coach-system`, ejecuta acción de Working Copy "Commit + Push" sobre la carpeta `memoria/logs/`.

> ⚠️ **Limitación honesta**: iOS exige una confirmación humana para que un Shortcut con acciones que envían datos a un servicio externo se ejecute desde Automation. Es 1 tap. No es evitable sin jailbreak.

---

## Shortcut 4 — "Revisión semanal"

**Cuándo**: domingo 21:00, Personal Automation.

**Pasos**:
1. *Get Files* de los últimos 7 archivos en `CoachPersonal/logs/` (filtrar por fecha de los últimos 7 días).
2. *Combine Text* concatenando todos.
3. *Get File* `plantillas/revision-semanal.md`.
4. *Combine*: plantilla + logs.
5. *Ask Claude* en Project Coach Personal.
6. *Show Result* (largo, lectura completa).
7. *Save* la respuesta en `CoachPersonal/logs/resumen-semana-{fecha}.md`.
8. *Show Alert*: "Sube `resumen-semana-{fecha}.md` al Project Coach Personal y elimina los 7 logs diarios". (Hasta aquí llega la automatización; subir archivos al Project requiere acción manual.)

---

## Personal Automations a crear (en app Atajos → Automatización → +)

| Automation | Trigger | Shortcut |
|---|---|---|
| Check-in mañana | Hora del día 07:00 | Check-in mañana |
| Cierre del día | Hora del día 23:00 | Cierre del día |
| Revisión semanal | Hora del día 21:00, domingos | Revisión semanal |

Para todas: deshabilita "Pedir antes de ejecutar" cuando iOS lo permita; donde no, será 1 tap.

---

## Sincronización con el Project de Claude

El Project de Claude no se actualiza solo. Pero el flujo natural es:

- **Diario**: el log se guarda en iCloud (no en el Project). El coach lo lee desde la conversación porque tú compartiste los datos en el chat del día.
- **Semanal (domingo)**: subes manualmente el `resumen-semana-{fecha}.md` al Project y eliminas los 7 logs diarios sueltos del Project si los habías subido. El Project siempre tiene como máximo: skills + perfil + histórico + 4–6 resúmenes semanales recientes.
- **Mensual**: el coach genera (a tu petición) un `resumen-mes-{YYYY-MM}.md` que reemplaza los resúmenes semanales del mes anterior.

Esto mantiene el Project ligero, fresco y con memoria útil sin cargarlo de ruido diario.

---

## Migración futura a "cero toques" (si abres la puerta a API)

Cuando quieras eliminar incluso el tap de confirmación diaria:

1. Repo en GitHub con los archivos de `memoria/`.
2. GitHub Action programada (cron) llama a la API de Anthropic con el log del día y devuelve el resumen.
3. Commit automático al repo.
4. Push notification al iPhone (vía Pushover/ntfy gratis).

Coste estimado: <1€/mes con Sonnet 4.6. Lo dejo apuntado pero no lo construyo hasta que lo decidas.
