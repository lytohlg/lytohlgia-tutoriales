# Entorno de pruebas del vídeo «El validador dijo OK y guardó una fecha que no existe: pydantic» — @lytohlgIA
# ---------------------------------------------------------------------------
# Se construye con:  docker build -t repro-pydantic-csv:local entorno
# Versiones FIJADAS (reproducible). Ningún dato personal dentro de la imagen: el CSV del
# vídeo se genera aquí, en el repositorio, con datos inventados.
FROM python:3.12-slim

RUN pip install --no-cache-dir pydantic==2.12.3 email-validator==2.3.0

WORKDIR /trabajo
