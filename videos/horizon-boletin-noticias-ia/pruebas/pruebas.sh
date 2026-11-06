#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba que la salida trae lo que esperamos
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-horizon-boletin-noticias-ia:local"
ESPERADO="seleccionadas: 5"

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
SALIDA="$(docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh')"
echo "$SALIDA"

echo "[3/3] Comprobando la salida esperada ..."
if printf '%s' "$SALIDA" | grep -qF "$ESPERADO"; then
  echo
  echo "✔ Prueba terminada sin errores. Salida esperada encontrada: $ESPERADO"
else
  echo
  echo "✘ La demo corrió, pero no aparece «$ESPERADO» en la salida."
  exit 1
fi
