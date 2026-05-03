# data/

Datos crudos y procesados del usuario.

```
data/
  raw/
    training/    # exports de Jefit, capturas, logs en bruto
    nutrition/   # menús semanales, listas de la compra, recetas
    finance/     # extractos bancarios, exports de apps de gasto
    sleep/       # exports de AutoSleep, Apple Health, Garmin, etc.
    habits/      # logs de hábitos en bruto
    medical/     # analíticas, informes (privados)
  processed/     # datos limpios para análisis
```

## Convenciones

- Nombres de archivo: `dominio-AAAA-MM-DD.ext` (ej. `peso-2026-05-01.csv`, `extracto-2026-04.pdf`).
- En `processed/` se generan agregados por mes/trimestre.

## Privacidad

`data/raw/medical/` y `data/raw/finance/` contienen información especialmente sensible. Considerar:
- Repo privado obligatorio.
- Gitignorar si se hace push.
- No subir a servicios de terceros sin cifrado.
