# Skill: Entrenamiento — Fuerza + Cardio

Base de conocimiento aplicado para programación, diagnóstico y ajuste de entrenamientos. Stack del usuario: **Jefit (fuerza)** + **app Workouts iPhone (cardio)**.

## Marco general

### Principios de programación (evidencia 2024–2026)

1. **Volumen efectivo > volumen total**. Series cerca del fallo (RIR 0–3) son las que cuentan. 10–20 series semanales por grupo muscular para hipertrofia, 5–10 para fuerza pura.
2. **Frecuencia ≥ 2 por grupo/semana** para hipertrofia. Para fuerza máxima en patrones específicos, hasta 3–4.
3. **Progresión**: micro-cargas (1.25–2.5 kg) > saltos grandes. Doble progresión (reps→peso) supera a progresión lineal en fase intermedia.
4. **Periodización ondulante** o **bloques** > lineal pura tras los primeros 6 meses.
5. **Fatiga acumulada**: cada 4–6 semanas, deload 40–60% volumen (no descanso total).
6. **Ratio empuje:tracción ≈ 1:1** mínimo, idealmente 1:1.2 favoreciendo tracción para salud postural.

### Cardio — modelo polarizado

- **80% baja intensidad** (zona 2: respira por nariz, conversación posible). Construye base mitocondrial, oxidación grasa, recuperación.
- **20% alta intensidad** (zona 4–5: VO2max, intervalos). Eleva techo aeróbico.
- **Evita zona 3 ("gris")** en exceso: alto coste de fatiga, bajo retorno adaptativo.
- Mínimo eficaz: 150 min/semana zona 2 + 1 sesión HIIT (4×4 min o 30/30) para mejoras cardiovasculares notables.

## Biomecánica aplicada (resumen operativo)

### Patrones fundamentales y errores frecuentes

| Patrón | Errores típicos | Señal de buena ejecución |
|---|---|---|
| **Sentadilla** | Rodillas colapsando hacia dentro, pelvis báscula al fondo (butt wink), pérdida de torso erguido | Pies activos (tripode), rodillas alineadas con dedos medio/segundo, columna neutra, profundidad sin perder lumbar |
| **Peso muerto** | Lumbar flexionada, barra alejada del cuerpo, hiperextensión final | Barra pegada, cadera y rodilla extienden coordinadas, glúteo termina el movimiento, no hiperextensión |
| **Press banca** | Codos 90° (estrés hombro), arco lumbar excesivo sin escapulas fijadas | Escápulas retraídas + deprimidas, codos 45–60°, barra al mid-pec, contacto pies-tres puntos |
| **Press militar** | Lumbar hiperextendida compensando, cuello adelantado | Glúteos contraídos, costillas abajo, barra sobre mediopié al final |
| **Dominada** | Solo brazos, rango parcial, hombros adelantados | Activa dorsal antes de tirar, escápula deprime, esternón al barra, ROM completo |
| **Remo** | Tirón con torso en lugar de brazos, escápula no se mueve | Codo viaja atrás, escápula retrae al final, torso estable |

### Lesiones — banderas rojas vs molestias normales
- **Dolor agudo punzante en articulación**: parar, no enmascarar.
- **Dolor referido en cuello/lumbar tras sesión**: revisar técnica, probable error postural.
- **DOMS (agujetas) 24–72h en vientre muscular**: normal y esperable.
- **Tendinopatías** (codo, hombro, rótula): no descansar — *cargar* progresivamente con isométricos y excéntricos lentos. La inmovilización empeora.

## Protocolo de diagnóstico de entreno

Cuando el usuario comparte un entreno:

1. **Datos bruto**: ejercicios, series×reps×peso, RIR percibido, tiempo total.
2. **Análisis volumen**: ¿está dentro del rango efectivo para el grupo trabajado esta semana?
3. **Análisis intensidad**: ¿RIR coherente con su fase? Fuerza: 1–3 RIR. Hipertrofia: 0–2 RIR la última serie. Mantenimiento: 3–5 RIR.
4. **Progresión vs sesión anterior** (consultar log): ¿se ha movido peso, reps o RIR? Si no hay progresión 2 sesiones seguidas → analizar (técnica, recuperación, programa).
5. **Selección de ejercicios**: ¿hay redundancia? ¿falta algún patrón? ¿ratio empuje/tracción?
6. **Recuperación inferida**: cruzar con sueño y carga de los últimos 3 días.
7. **Devolución**: formato `✅ Bien / 🔧 Ajusta / 📈 Próxima sesión`.

## Ajuste según métricas de sueño (AutoSleep)

| Sueño noche anterior | Recomendación entreno del día |
|---|---|
| <5h o calidad mala | Movilidad + cardio zona 2 30 min, NO fuerza intensa |
| 5–6h aceptable | Sesión planificada al 80% intensidad, reducir 1 serie por ejercicio |
| 6.5–8h calidad buena | Sesión completa según plan |
| >8h, HRV alto | Día ideal para sesión clave (PR, intensidad alta) |

## Estructura semanal recomendada (a personalizar tras conocer el perfil)

Modelo **Upper/Lower 4 días + 2 cardio**:
- L: Upper (push priority)
- M: Cardio Z2 45 min
- X: Lower (squat priority)
- J: Descanso o movilidad
- V: Upper (pull priority)
- S: Lower (hinge priority) + cardio HIIT 15 min final
- D: Cardio Z2 60 min outdoor

Variantes según objetivo del usuario (a definir en `perfil.md`).

## Suplementación con evidencia para entreno

- **Creatina monohidrato 5g/día**: la única con evidencia overwhelming. Tomar siempre, momento irrelevante.
- **Cafeína 3–6 mg/kg pre-entreno**: rendimiento +5–10% en alta intensidad. Cuidado interacción con cese de nicotina (puede amplificar ansiedad).
- **Proteína whey/aislado**: solo herramienta para alcanzar 1.6–2.2 g/kg/día totales. No mágica.
- **Omega-3 EPA/DHA 2–3g**: anti-inflamatorio, recuperación.
- **Vitamina D3** si déficit (analítica): 2000–4000 UI.
- Lo demás (BCAAs, glutamina, pre-workouts comerciales): irrelevante o estafa.

## Reglas para el coach

1. **No prescribas sin conocer**: si falta info en `perfil.md` (lesiones, experiencia, objetivos), pregunta antes de programar.
2. **Cuestiona la rutina actual del usuario** al revisarla por primera vez: ¿está optimizada o es herencia? Listar puntos a mejorar.
3. **No copies plantillas de internet**: cada propuesta justificada en su contexto específico.
4. **Si el usuario tiene 3+ días seguidos de sueño <6h**: insiste en deload, no programes intensidad.
5. **Durante Allen Carr días 7–15**: prioriza cardio Z2 (regula dopamina sin estresar) sobre fuerza pesada.
