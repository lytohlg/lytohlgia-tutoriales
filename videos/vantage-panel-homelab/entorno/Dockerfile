# Entorno de pruebas del vídeo «Vantage: un panel para tu red y tus servidores» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-vantage-panel-homelab:local entorno
# Reglas: versiones FIJADAS (commit exacto) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Commit exacto con el que se grabó el vídeo (no una rama que cambie mañana).
ARG VANTAGE_COMMIT=803b47f65089329fbf369df2a0c931d770a87da3
RUN git clone https://github.com/levi-xy/vantage /opt/vantage \
 && cd /opt/vantage && git checkout ${VANTAGE_COMMIT}

RUN pip install --no-cache-dir /opt/vantage/backend

WORKDIR /trabajo
