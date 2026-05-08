# Plantilla — Cierre del día

> Prompt que envía el Shortcut "Cierre del día" automáticamente a las 23:00.

---

Cierre del día. Genera el log estructurado de hoy basándote en TODA nuestra conversación de hoy en este Project.

Datos a sintetizar:
- Sueño (si lo compartí esta mañana)
- Entreno(s) hechos hoy y diagnóstico
- Adherencia nutricional aproximada
- Estado Allen Carr: día actual del protocolo, consumo si aplica, gatillos del día, estado mental
- Energía y ánimo a lo largo del día
- Un ajuste para mañana

**Devuelve EXCLUSIVAMENTE el JSON con el formato siguiente, sin texto adicional antes ni después**:

```json
{
  "fecha": "YYYY-MM-DD",
  "sueno": {"horas": 0.0, "calidad": "", "notas": ""},
  "entreno": {"tipo": "", "carga": "", "calidad": "", "notas": ""},
  "nutricion": {"adherencia": "", "notas": ""},
  "allen_carr": {"dia": 0, "consumo_tabaco": 0, "consumo_cannabis": 0, "estado_mental": "", "gatillos": []},
  "energia_animo": "",
  "ajuste_manana": ""
}
```

Sustituye la fecha por la de hoy. Si te falta dato porque no se compartió, déjalo vacío ("") o en 0, no inventes.
