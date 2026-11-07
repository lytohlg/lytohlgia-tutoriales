#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba que la salida trae las cifras del vídeo
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-founder-skill:local"

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
SALIDA="$(docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh')"
printf '%s\n' "$SALIDA"

echo "[3/3] Comprobando el resultado ..."
fallos=0
for esperado in "Break-even: 186 cups a day" "Break-even: 289 bandejas a day" "-66%" "Verdict: Not yet" "0 answered"; do
  if printf '%s' "$SALIDA" | grep -qF -- "$esperado"; then
    echo "  ok     $esperado"
  else
    echo "  FALTA  $esperado"
    fallos=$((fallos + 1))
  fi
done

if [ "$fallos" -ne 0 ]; then
  echo "✘ La demo no produjo $fallos de las cifras esperadas."
  exit 1
fi

echo
echo "✔ Prueba terminada sin errores."
