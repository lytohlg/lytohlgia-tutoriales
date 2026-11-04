#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
#   1) construye el entorno de entorno/Dockerfile
#   2) ejecuta la demo en un contenedor limpio, sin privilegios, con la carpeta
#      montada en SOLO LECTURA y una copia de trabajo en /tmp
#   3) comprueba que la salida contiene lo que promete el material
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-llmux-gateway-observabilidad:local"
CTX="${DOCKER_CONTEXT:-default}"

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker --context "$CTX" build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
SALIDA="$(docker --context "$CTX" run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh')"
printf '%s\n' "$SALIDA"

echo "[3/3] Comprobando la salida esperada ..."
for TROZO in "gateway en :8095" "sin clave: HTTP 401" "con clave: HTTP 200" \
             "modelo que devuelve el gateway: gpt-4o-mini" "VERIFICADO:"; do
  if ! printf '%s' "$SALIDA" | grep -qF "$TROZO"; then
    echo "FALLO: la salida no contiene: $TROZO"
    exit 1
  fi
done
echo "OK: el material hace lo que promete"
