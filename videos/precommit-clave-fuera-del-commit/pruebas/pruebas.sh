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
IMAGEN="repro-precommit-clave-fuera-del-commit:local"
CTX="${DOCKER_CONTEXT:-default}"
ESPERADO='VERIFICADO: dos controles paran el commit · la clave no entra · el YAML y el binario se arreglan · hook propio de 20 líneas · --no-verify lo salta'

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker --context "$CTX" build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
SALIDA="$(docker --context "$CTX" run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh' 2>&1)"

echo "[3/3] Comprobando la salida esperada ..."
if ! grep -Fq "$ESPERADO" <<<"$SALIDA"; then
  echo "❌ La salida no contiene la línea esperada:"
  echo "   $ESPERADO"
  echo "--- últimos 40 renglones de la demo ---"
  tail -40 <<<"$SALIDA"
  exit 1
fi

echo
echo "✔ Prueba terminada sin errores: el material se reproduce en limpio."
