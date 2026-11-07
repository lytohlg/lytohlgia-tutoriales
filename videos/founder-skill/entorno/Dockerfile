# Entorno de pruebas del vídeo «Pon los números de tu negocio en un JSON y el script te dice si pierdes dinero» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material (la misma que se ve en pantalla):
# Python 3.13 y git, nada más. Se construye con:
#     docker build -t repro-founder-skill:local entorno
# El repositorio público NO se mete en la imagen: lo trae `traer_repo.sh`
# (o `demo.sh` si no lo encuentra), así que se puede leer antes de ejecutarlo.
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Este material no usa NINGUNA dependencia de Python: unit_economics.py,
# van_westendorp.py, panel.py y compile.py son biblioteca estándar pura.
# Por eso no hay ningún `pip install` aquí, y esa es justo una de las cosas
# que el vídeo demuestra: ni pip, ni entorno virtual, ni claves de API.

WORKDIR /trabajo
