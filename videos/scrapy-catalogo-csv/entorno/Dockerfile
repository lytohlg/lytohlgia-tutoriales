# Entorno de pruebas del vídeo «Scrapy: reunir un catalogo entero en un CSV sin escribir un bucle» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-scrapy-catalogo-csv:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Dependencias de Python, con la versión fijada (las mismas que se usaron en el vídeo):
RUN pip install --no-cache-dir \
      "scrapy==2.20.0" \
      "requests==2.34.2" \
      "beautifulsoup4==4.15.0"

WORKDIR /trabajo
