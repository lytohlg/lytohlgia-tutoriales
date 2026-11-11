# Entorno de pruebas del vídeo «Photon: lo que tu web expone sin que lo sepas» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-photon-audita-tu-web:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# git: para traer el repo en una revisión EXACTA (reproducible, no "master").
RUN apt-get update && apt-get install -y --no-install-recommends git curl \
    && rm -rf /var/lib/apt/lists/*

# Repo clonado en el commit medido y comprobado (2026-10-18). Versión del CLI: 1.3.2.
# Va en /opt: /trabajo lo ocupa (solo lectura) el paquete al reproducir.
RUN git clone -q https://github.com/s0md3v/Photon.git /opt/photon \
    && cd /opt/photon \
    && git checkout -q c8d2566841d69a268b244609921143d84b72b0c6

# Dependencias de Python con versión fijada.
RUN pip install --no-cache-dir \
      requests==2.34.2 \
      urllib3==2.8.0 \
      tld==0.13.2

# Material del vídeo: los scripts que generan el sitio de prueba y verifican el informe.
COPY material/ /opt/material/

# El revisor ejecuta como usuario 1000: git apply y el informe necesitan escribir.
RUN chown -R 1000:1000 /opt

WORKDIR /opt
