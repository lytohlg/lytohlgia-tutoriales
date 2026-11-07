# Entorno de pruebas del vídeo «Encuentra lo que repites en tu historial de IA y tapa tus claves» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-faq-shortcuts:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
# El repositorio público NO se mete en la imagen: lo trae `traer_repo.sh`
# (o `demo.sh` si no lo encuentra), así que se puede leer antes de ejecutarlo.
FROM python:3.13-slim

# git: necesario para traer el repositorio original en la revisión fijada.
# pytest: el runner de los tests del propio repositorio, con versión fijada.
RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pytest==9.2.0

WORKDIR /trabajo
