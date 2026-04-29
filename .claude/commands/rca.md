---
description: Root Cause Analysis estructurado de un evento de fallo.
argument-hint: [equipo / evento / fecha]
---

Lanza un **RCA** sobre `$ARGUMENTS`.

Subagentes: `reliability-engineer` (líder), `lean-maintenance-engineer` (5Why/Ishikawa), `gmp-maintenance-advisor` (si farma), `safety-risk-reviewer` (si hay riesgo HSE).

Salida obligatoria:
1. **Evento** (qué/cuándo/dónde, secuencia).
2. **Evidencia** recogida (datos, fotos, logs).
3. **5 Why** (cada Why verificable).
4. **Ishikawa 6M**.
5. **Causa física + causa humana + causa latente (sistémica)**.
6. **Contramedidas**: contención (24-72h) + solución (raíz) + preventiva (sistémica).
7. **Plan**: owner, fecha, métrica de eficacia.
8. **Cierre**: criterio de verificación, próximo follow-up.

Si toca GMP → marcar `⚠ Requiere QA review` + sugerir abrir desviación si no existe.
Guardar en `reports/drafts/YYYY-MM-DD_rca_<equipo>.md`.
