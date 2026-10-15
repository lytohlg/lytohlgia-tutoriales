# Entorno de pruebas del vídeo «restic: restaurar y comparar para saber si tu copia sirve» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-restic-verificar-copia:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Dependencias del sistema: lo mínimo para descargar y descomprimir el binario.
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      bzip2 \
    && rm -rf /var/lib/apt/lists/*

# restic FIJADO por versión + hash: se descarga el binario oficial de la release y
# se comprueba su sha256 contra el valor publicado (el mismo que se ve en el vídeo).
# Si el binario no coincide con el hash, la construcción FALLA: no se instala nada.
ARG RESTIC_VERSION=0.19.1
ARG RESTIC_SHA256=f415415624dcc452f2a02b8c33641791a8c6d6d3b65bbb3543fcf9a25151585c
RUN FICHERO="restic_${RESTIC_VERSION}_linux_amd64.bz2" \
 && curl -fsSL -o /tmp/restic.bz2 \
        "https://github.com/restic/restic/releases/download/v${RESTIC_VERSION}/${FICHERO}" \
 && echo "${RESTIC_SHA256}  /tmp/restic.bz2" | sha256sum -c - \
 && bunzip2 /tmp/restic.bz2 \
 && install -m 0755 /tmp/restic /usr/local/bin/restic \
 && rm -f /tmp/restic \
 && restic version

WORKDIR /trabajo
