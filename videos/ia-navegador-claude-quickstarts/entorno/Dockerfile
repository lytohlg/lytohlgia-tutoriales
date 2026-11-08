# Entorno de pruebas del vídeo «Tu IA no puede navegar: 6 llamadas de Claude Quickstarts, una por una» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-ia-navegador-claude-quickstarts:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Chromium es el navegador que el driver controla: sin él no hay nada que demostrar.
RUN apt-get update && apt-get install -y --no-install-recommends \
      chromium fonts-liberation ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python, SIEMPRE con la versión fijada:
RUN pip install --no-cache-dir \
      "anthropic==2.6.0" \
      "websockets==17.4"

WORKDIR /trabajo
