#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba que la salida esperada (AVISO) aparece
# Si esto termina sin errores, tu copia funciona.
#
# Uso:  bash pruebas/pruebas.sh [--context NOMBRE]
#       (el contexto es opcional: solo hace falta si tienes más de un motor
#        Docker configurado; nosotros lo usamos para forzar el local)
# ---------------------------------------------------------------------------
set -euo pipefail

CTX=""
if [ "${1:-}" = "--context" ] && [ -n "${2:-}" ]; then
  CTX="--context $2"
fi

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-stock-ssm:local"
SALIDA="$(mktemp)"

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker $CTX build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
docker $CTX run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh' \
  | tee "$SALIDA"

echo
echo "[3/3] Comprobando la salida esperada ..."
if grep -q "AVISO" "$SALIDA"; then
  echo "✔ Prueba terminada sin errores: la salida contiene AVISO."
else
  echo "✘ La demo terminó pero no aparece AVISO: revisa la salida de arriba." >&2
  exit 1
fi
