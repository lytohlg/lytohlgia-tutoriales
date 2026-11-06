# Entorno de pruebas del vídeo «El agente dice que está hecho» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material: Python 3.12 y git, nada más.
# El repositorio público NO se mete en la imagen: lo trae `demo.sh` con `traer_repo.sh`,
# así que se puede leer antes de ejecutarlo.
#
#   docker build -t repro-hardware-in-the-loop-gates:local entorno
#
# Reglas: imagen base fijada y ningún dato personal dentro.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
