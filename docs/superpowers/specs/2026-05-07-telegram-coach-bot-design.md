# Telegram Coach Bot — Especificación de diseño

**Fecha:** 2026-05-07  
**Proyecto:** personal-coach-system  
**Estado:** Aprobado — pendiente de implementación

---

## 1. Objetivo

Bot de Telegram que actúa como consejo de expertos personal disponible 24/7 desde el móvil, independiente del PC. Recibe imágenes de sueño y entreno, responde con análisis multi-agente coordinado, y genera reportes PDF premium entregados por Telegram y guardados en OneDrive.

---

## 2. Arquitectura general

```
iPhone (Telegram)
      │
      ▼
Telegram Bot
(AppDaemon · RPi · 192.168.13.3)
      │
      ▼
Orquestador
├── Clasifica input (foto sueño / foto entreno / texto / reporte)
├── Lee memory/ del repo clonado en RPi
└── Lanza llamadas paralelas a Claude API
          │
          ├── Agente primario (análisis completo)
          └── Agentes secundarios (solo los relevantes)
                    │
                    ▼
             Sintetizador
             (une respuestas, elimina redundancias)
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
   Respuesta Telegram    Generador PDF
                         (si es reporte)
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             Telegram (envío)      OneDrive (rclone)
```

### Stack técnico

| Componente | Tecnología |
|------------|------------|
| Bot runtime | AppDaemon add-on (HA) |
| Librería Telegram | `python-telegram-bot` |
| Modelo agentes | Claude Haiku (respuestas) · Claude Sonnet (reportes) |
| Generación PDF | WeasyPrint + matplotlib + Jinja2 |
| Sincronización OneDrive | rclone (desde RPi, directo) |
| Memoria | Git repo clonado en `/config/personal-coach-system/` |

---

## 3. Orquestación de agentes

### Tabla de routing

| Input | Agente primario | Agentes secundarios posibles |
|-------|----------------|------------------------------|
| Foto AutoSleep | `recovery-sleep-energy-coach` | entreno, nutrición, meditación |
| Foto Jefit | `strength-conditioning-coach` | nutrición, sueño, disciplina |
| Foto Strava / cardio | `strength-conditioning-coach` | nutrición, sueño |
| Texto libre | `personal-life-co-worker` | los que procedan |
| Solicitud reporte | orquestador directo | todos los relevantes |

### Lógica de activación de agentes secundarios

Un agente secundario responde únicamente si su aportación cambia alguna acción concreta del día. Ejemplos de activación:

- HRV bajo → `strength-conditioning-coach` reduce carga
- Sueño < 6h → `muscle-cooking-nutrition-coach` ajusta calorías y carbohidratos
- Entreno muy intenso → `recovery-sleep-energy-coach` da pautas de recuperación
- Serie de mal sueño (3+ días) → `meditation-mindfulness-guide` propone práctica

Si un agente no tiene nada que cambie la acción del día, no aparece en la respuesta.

### Formato de respuesta — secciones etiquetadas

Cada agente firma su aportación con emoji y nombre de dominio. Ejemplo para foto AutoSleep:

```
📊 Análisis · 7 mayo

💤 Descanso
HRV 42 (↓ respecto a tu media 58). Sueño fragmentado,
2 despertares. Calidad real: 5.8h efectivas.
Hoy es día de carga reducida.

🏋️ Entreno
Con ese HRV no toques máximos. Sesión técnica:
70% del peso habitual, foco en movilidad y ejecución.

🥗 Nutrición
Sueño malo sube cortisol. Desayuno rico en carbohidratos
complejos (avena, fruta). Evita cafeína antes de las 9h.

🧘 Meditación
10 min body scan al levantarte. Te dejo la secuencia.
```

---

## 4. Reportes PDF

### Tipos disponibles

| Comando Telegram | Contenido | Frecuencia recomendada |
|-----------------|-----------|----------------------|
| `reporte semanal` | Sueño, entrenos, nutrición, hábitos | Domingo |
| `reporte entreno` | Progresión de marcas, volumen, tendencias | Mensual |
| `reporte sueño` | HRV, calidad media, patrones, correlaciones | Mensual |
| `reporte progreso` | Peso, composición, adherencia global | Mensual |
| `reporte decisiones` | Decisiones tomadas, resultados, aprendizajes | Trimestral |
| `reporte completo` | Todo lo anterior unificado | Mensual / trimestral |

### Estructura de cada reporte

```
1. Portada          — Nombre · Periodo · Fecha
2. Resumen ejecutivo — 3 métricas clave · semáforo · tendencia
3. Secciones por dominio — Gráfica + análisis del agente relevante
4. Conclusiones     — Top 3 prioridades del periodo siguiente
```

### Estilo visual

- Paleta oscura premium: fondo `#0F1117`, acentos `#6C63FF` y `#00D9FF`
- Tipografía Inter
- Gráficas limpias, sin ruido visual
- *Nota: paleta y layout se ajustarán en fase de implementación*

### Entrega

1. PDF enviado por Telegram al chat
2. Copia guardada en `C:\Users\jesus\OneDrive\Mis Documentos\40-Reports\personal-coach-system\`
   vía rclone directo desde RPi (sin pasar por el PC)

**Nombrado:** `AAAA-MM-DD-tipo.pdf`  
Ejemplo: `2026-05-07-semanal.pdf`

---

## 5. Interfaz Telegram

### Comandos

```
/start          — Presentación y ayuda
/agentes        — Lista agentes activos

/descanso       — Análisis manual sin foto (usa último log)
/entreno        — Resumen del último entreno registrado
/plan           — Plan del día basado en estado actual

/reporte semanal
/reporte entreno
/reporte sueño
/reporte progreso
/reporte decisiones
/reporte completo

/memoria        — Resumen del perfil actual
/actualizar     — Fuerza sync de memory/ desde GitHub
```

### Lenguaje natural

El bot entiende mensajes sin comandos. Ejemplos:

- `"no me apetece entrenar hoy"` → `motivation-discipline-coach`
- `"¿qué como antes de entrenar?"` → `muscle-cooking-nutrition-coach`
- `"llevo 3 días durmiendo mal"` → análisis multi-agente
- `"tengo que tomar una decisión importante"` → `strategic-decision-advisor`

### Envío de imágenes

Sin comando previo. El bot detecta el tipo automáticamente:
- Pantalla AutoSleep → flujo sueño
- Resumen Jefit → flujo fuerza
- Mapa / resumen Strava → flujo cardio

### Memoria de conversación

Cada sesión mantiene contexto durante la conversación. Preguntas de seguimiento (`"¿y si duermo una siesta?"`) se resuelven sin repetir contexto.

---

## 6. Sincronización de memoria

### GitHub → RPi (cada hora)

```
GitHub repo (personal-coach-system)
        │  git pull · HA automation · cada hora
        ▼
RPi /config/personal-coach-system/memory/
        │  leído antes de cada respuesta del bot
        ▼
Claude API (contexto siempre actualizado)
```

### PC → GitHub → RPi

1. Editas `memory/` en `C:\Users\jesus\personal-coach-system\`
2. `git push` (manual o asistido)
3. RPi lo recibe en la siguiente hora
4. `/actualizar` en Telegram fuerza sync inmediata

### Bot → GitHub (actualizaciones propuestas)

Cuando el bot detecta información nueva relevante en conversación:

```
📝 PROPUESTA DE MEMORIA
→ memory/body-training-profile.md
Peso actual: 78kg (actualizado desde 80kg)
¿Confirmas? Sí / No
```

Si confirmas: commit automático al repo, PC lo recibe en el siguiente `git pull`.

---

## 7. Estructura de archivos en RPi

```
/config/
  appdaemon/
    apps/
      coach-bot.py          # bot principal (AppDaemon app)
      orchestrator.py       # clasificación y routing
      agents/               # un módulo por agente
        sleep_coach.py
        strength_coach.py
        nutrition_coach.py
        meditation_coach.py
        decision_advisor.py
        motivation_coach.py
        productivity_coach.py
        identity_coach.py
        memory_curator.py
      report_generator.py   # generación de PDFs
      memory_reader.py      # lectura de archivos memory/
      onedrive_uploader.py  # rclone wrapper
    apps.yaml               # config AppDaemon
  personal-coach-system/    # clon del repo GitHub
    memory/
    data/
    ...
```

---

## 8. Dependencias y requisitos previos

- AppDaemon add-on instalado en HA
- `python-telegram-bot`, `anthropic`, `WeasyPrint`, `matplotlib`, `Jinja2`, `Pillow` instalados en el entorno AppDaemon
- Token de Telegram Bot (ya existe — `telegram_bot_orig.py`)
- API key de Anthropic
- rclone configurado con cuenta OneDrive del usuario
- Repo clonado en `/config/personal-coach-system/`
- HA automation de sync git cada hora

---

## 9. Fuera de alcance (esta fase)

- Integración directa con APIs de Jefit o Strava (el usuario envía capturas manualmente)
- Notificaciones proactivas sin input del usuario (p.ej. alertas automáticas de sueño)
- Interfaz web o dashboard
- Ajuste fino del estilo visual de reportes (se hará en implementación)
