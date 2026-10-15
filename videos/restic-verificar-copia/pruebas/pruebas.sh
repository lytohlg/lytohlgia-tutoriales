#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba que la demo dice lo que tiene que decir
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-restic-verificar-copia:local"
CTX="${REPO_DOCKER_CONTEXT:-default}"
ESPERADO="VERIFICACION FINAL: OK (detecta la copia incompleta y restaura identica)"
SALIDA="$(mktemp -t salida-restic-verificar-copia.XXXXXX.txt)"

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker --context "$CTX" build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
set +e
docker --context "$CTX" run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro && cd /tmp/repro && bash demo.sh' \
  2>&1 | tee "$SALIDA"
rc=${PIPESTATUS[0]}
set -e

echo "[3/3] Comprobando la salida esperada ..."
if [ "$rc" -ne 0 ]; then
  echo "✘ La demo terminó con código $rc (se esperaba 0)."
  exit 1
fi
if ! grep -qF "$ESPERADO" "$SALIDA"; then
  echo "✘ La salida no contiene lo esperado:"
  echo "   $ESPERADO"
  exit 1
fi
if ! grep -qE '^resultado +: +FALLO' "$SALIDA"; then
  echo "✘ La demo no llegó a detectar la copia incompleta (no hay ningún FALLO en la salida)."
  exit 1
fi

echo
echo "✔ Prueba terminada sin errores: la copia se restaura idéntica y el verificador detecta una copia incompleta."
