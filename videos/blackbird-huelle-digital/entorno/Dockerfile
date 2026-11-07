# Entorno de pruebas del vídeo «Blackbird: en qué 653 webs existe tu nombre de usuario (y cuáles no eres tú)» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-blackbird-huelle-digital:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.13-slim

# git: la herramienta se usa clonando su repositorio público.
RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /trabajo
