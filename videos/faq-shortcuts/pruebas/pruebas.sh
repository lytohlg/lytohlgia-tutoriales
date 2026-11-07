#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba que la salida contiene lo que el vídeo promete
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-faq-shortcuts:local"
SALIDA="$(mktemp)"
trap 'rm -f "$SALIDA"' EXIT

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker --context default build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh' \
  2>&1 | tee "$SALIDA"

echo
echo "[3/3] Comprobando la salida esperada ..."
FALLOS=0
while IFS= read -r esperado; do
  [ -z "$esperado" ] && continue
  if grep -qF -- "$esperado" "$SALIDA"; then
    echo "  ok   $esperado"
  else
    echo "  FALTA $esperado"
    FALLOS=$((FALLOS + 1))
  fi
done <<'ESPERADO'
33 prompts from claude
8 prompts from codex
6 prompts from cursor
[REDACTED]
13  revisar el CSV de facturas
peticiones clasificadas
passed
ESPERADO

if [ "$FALLOS" -gt 0 ]; then
  echo
  echo "✘ La salida no coincide: $FALLOS comprobaciones fallidas (ver arriba)."
  exit 1
fi
echo
echo "✔ Prueba terminada sin errores: la salida contiene lo que el vídeo promete."
