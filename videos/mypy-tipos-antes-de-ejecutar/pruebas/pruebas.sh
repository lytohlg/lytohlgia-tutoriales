#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-mypy-tipos:local"
# Motor de Docker a usar. Por defecto, el de tu máquina. Si tienes varios
# contextos: DOCKER="docker --context mi-contexto" bash pruebas/pruebas.sh
DOCKER="${DOCKER:-docker}"

echo "[1/2] Construyendo el entorno desde entorno/Dockerfile ..."
$DOCKER build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/2] Ejecutando la demo en un contenedor limpio ..."
$DOCKER run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -a /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'

echo
echo "✔ Prueba terminada sin errores."
