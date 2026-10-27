#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba que la salida contiene lo que promete el material
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-mlflow-experimentos-que-no-se-pierden:local"

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker --context "${DOCKER_CONTEXT:-default}" build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
SALIDA="$(docker --context "${DOCKER_CONTEXT:-default}" run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh')"
printf '%s\n' "$SALIDA"

echo "[3/3] Comprobando la salida esperada ..."
for TROZO in "VERIFICADO: 3 pruebas registradas" "ridge-alpha-0.1" "rmse 53.010" "progresion-diabetes"; do
  if ! printf '%s' "$SALIDA" | grep -qF "$TROZO"; then
    echo "✘ falta en la salida: $TROZO"
    exit 1
  fi
done

echo
echo "✔ Prueba terminada sin errores."
