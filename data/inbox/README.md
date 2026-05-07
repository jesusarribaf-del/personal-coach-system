# inbox/

Zona de entrada de documentación. Suelta aquí los archivos y pide análisis.
Los datos procesados se mueven a `data/raw/` o se vuelcan en `memory/`.

```
inbox/
  01-perfil-inicial/    # setup único: exports, analíticas, texto con tus datos
  02-complementaria/    # docs de apoyo: PDFs, planes previos, informes
  03-descanso/          # capturas diarias de AutoSleep (screenshot o export)
  04-entrenos/          # capturas de Jefit (fuerza) y Strava/Entreno (cardio)
```

## Cómo usar

1. Sube el archivo a la carpeta correspondiente.
2. Di: *"analiza lo nuevo en inbox/03-descanso"* (o la carpeta que sea).
3. Yo extraigo los datos, actualizo `memory/` y muevo o archivo el fichero.

## Nombrado recomendado

- Capturas: `AAAA-MM-DD.png` (ej. `2026-05-07.png`)
- Exports: `jefit-AAAA-MM-DD.csv`, `strava-AAAA-MM-DD.gpx`
- Docs: nombre descriptivo + fecha

## Privacidad

Este directorio contiene datos personales y de salud.
Asegúrate de que el repositorio es **privado** en GitHub.
