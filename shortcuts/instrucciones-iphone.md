# Shortcuts iPhone — flujo definitivo

## Check-in matinal — sin Shortcut (más fiable)

La acción "Preguntar a Claude" en iOS no permite seleccionar Project. Usar el Project directamente es la única opción fiable.

**3 pasos, ~30 segundos**:
1. Abre **Claude** → Project **"Coach Personal"** → **Nuevo chat**.
2. Adjunta 2-3 capturas de **AutoSleep** (botón + → Foto).
3. Escribe `Check-in matinal` → enviar.

**Acceso rápido**: añade Claude al Dock (barra inferior del iPhone) para tenerla a 1 tap siempre.

---

## Shortcut útil: "Diagnóstico entreno"

Este sí vale como Shortcut porque se lanza desde el **Share Sheet** de Workouts/Jefit.

### Crear el Shortcut

1. Atajos → **"+"** → nombre: `Diagnóstico entreno`.
2. **Acción 1** — busca `recibir`: selecciona **"Recibir entrada de Compartir"** → tipo Imágenes.
3. **Acción 2** — busca `texto`: añade acción **"Texto"** y escribe:
   ```
   Diagnóstico de entreno. Adjunto captura de la sesión.
   Sensaciones (edita antes de enviar si quieres):
   - RIR percibido:
   - Técnica (1-10):
   - Dolor/molestia:
   - Energía:
   Aplica el protocolo de diagnóstico de entreno.
   ```
4. **Acción 3** — busca `portapapeles`: **"Copiar al portapapeles"** → conectado al Texto.
5. **Acción 4** — busca `abrir app`: **"Abrir app"** → selecciona Claude.

**Uso**: en Workouts o Jefit → compartir captura → Share Sheet → toca "Diagnóstico entreno" → se abre Claude → ve al Project → nuevo chat → adjunta la foto → pega el prompt → envía.

---

## Recordatorios diarios (Automations simples)

No necesitan Shortcut. Solo crean una notificación a una hora fija.

**Crear uno** (ejemplo: recordatorio check-in):
1. Atajos → pestaña **"Automatización"** → **"+"**.
2. **"Crear automatización personal"** → **"Hora del día"** → pon 07:30 (o tu hora habitual).
3. Añadir acción: busca `notificación` → **"Mostrar notificación"**.
4. Título: `Coach` → Cuerpo: `Abre Claude → check-in matinal`.
5. Desactiva "Preguntar antes de ejecutar" si iOS lo permite → **"Hecho"**.

Repite para:
- 23:00 → `Cierra el día en Claude`
- Domingo 21:00 → `Revisión semanal en Claude`

---

## Automatización completa vía API (futuro, ~1.50€/mes)

Cuando quieras cero-taps: el Shortcut llamaría directamente a la API de Anthropic con el system-prompt y skills embebidos, sin necesidad de abrir la app. Instrucciones disponibles bajo petición.
