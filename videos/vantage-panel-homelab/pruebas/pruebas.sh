#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile (commit fijado)
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios y con la
#      carpeta montada en SOLO LECTURA (el script trabaja sobre una copia en /tmp)
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-vantage-panel-homelab:local"

echo "[1/2] Construyendo el entorno desde entorno/Dockerfile ..."
docker build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/2] Ejecutando la demo en un contenedor limpio ..."
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/origen:ro" "$IMAGEN" \
  bash -c 'cp -r /origen /tmp/paquete && cd /tmp/paquete && bash demo.sh'
