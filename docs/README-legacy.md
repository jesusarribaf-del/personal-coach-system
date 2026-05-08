# Personal Coach System

Sistema de coach personal multi-dominio (entrenamiento, nutrición, deshabituación, motivación) basado en Claude Pro Projects + iOS Shortcuts. Diseñado como **plantilla reutilizable**: para crear futuros coaches (finanzas, idiomas, etc.) basta clonar la estructura y cambiar `system-prompt.md` y `skills/`.

## Cómo está estructurado

```
personal-coach-system/
├── system-prompt.md          → instrucciones de sistema del coach (pegar en Claude Project)
├── skills/                   → conocimiento experto por dominio
│   ├── allen-carr-15-dias.md
│   ├── entrenamiento.md
│   ├── nutricion.md
│   ├── biomecanica.md
│   └── motivacion.md
├── memoria/                  → estado persistente del usuario
│   ├── perfil.md             → quién eres (rellenar al inicio)
│   ├── historico-chatgpt.md  → resumen del hilo previo
│   └── logs/                 → logs diarios autogenerados
├── plantillas/               → prompts reutilizables
│   ├── check-in-matinal.md
│   ├── diagnostico-entreno.md
│   ├── cierre-dia.md
│   └── revision-semanal.md
└── shortcuts/                → configuración iOS Shortcuts
    └── instrucciones-iphone.md
```

## Flujo diario (resumen)

| Cuándo | Qué pasa | Tu acción |
|---|---|---|
| 07:00 | Shortcut "Check-in mañana" se dispara solo | 1 tap: abrir el resumen |
| Tras entrenar | Compartes captura Jefit/Workouts a Claude | 2 taps: Share → Claude |
| 23:00 | Shortcut "Cierre del día" se dispara solo | 1 tap confirmar guardado |
| Domingo 21:00 | Shortcut "Revisión semanal" | 2 taps: subir log al Project |

## Setup inicial (15 minutos, una vez)

1. **Crea un Project en Claude.ai**: nombre "Coach Personal".
2. **Copia el contenido de `system-prompt.md`** en las instrucciones del Project.
3. **Sube como archivos del Project**: todos los `.md` de `skills/` + `memoria/perfil.md` + `memoria/historico-chatgpt.md`.
4. **Rellena `memoria/perfil.md`** con tus datos reales (peso, edad, historial, objetivos, lesiones).
5. **Pega tu export de ChatGPT en `memoria/historico-chatgpt.md`** — luego pide a Claude en una primera sesión: "léelo y reescríbelo en formato estructurado siguiendo la plantilla del archivo". Reemplazas el archivo en el Project.
6. **Configura Shortcuts en iPhone** siguiendo `shortcuts/instrucciones-iphone.md`.

## Mantenimiento

- **Diario**: el sistema se mantiene solo vía Shortcuts.
- **Semanal**: 1 minuto el domingo para sincronizar el log de la semana al Project.
- **Mensual**: revisión + ajuste del `system-prompt.md` si detectas desvíos.

## Replicar para otro coach

1. `cp -r personal-coach-system coach-finanzas`
2. Reescribe `system-prompt.md` y `skills/` para el dominio nuevo.
3. Crea un nuevo Project en Claude.ai.
4. El resto (memoria, plantillas, shortcuts) es estructuralmente idéntico.
