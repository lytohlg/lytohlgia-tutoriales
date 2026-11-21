# Entorno donde se grabó «Automatiza 300 fotos de producto con Pillow en minutos» — @lytohlgIA
# ---------------------------------------------------------------------------
# Se construye con:  docker build -t repro-pillow-300-fotos:local entorno
# Versiones FIJADAS (reproducible). Ningún dato personal dentro de la imagen: las 300 fotos
# se generan aquí, en el momento, con semilla fija.
FROM python:3.11-slim

RUN pip install --no-cache-dir pillow==13.0.0

WORKDIR /trabajo
