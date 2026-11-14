# Entorno de pruebas del vídeo «Textual: ve qué falla en un proceso largo sin leer 240 líneas» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-textual-proceso-largo:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

# Dependencias de Python, con la versión EXACTA que se usó en el vídeo:
RUN pip install --no-cache-dir -q textual==8.2.8

WORKDIR /trabajo
