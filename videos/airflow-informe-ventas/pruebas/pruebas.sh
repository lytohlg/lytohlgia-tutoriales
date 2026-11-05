#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba que la salida contiene lo prometido
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-airflow-informe-ventas:local"
CTX="${DOCKER_CONTEXT:-default}"
# Lo que la demo promete dejar en pantalla (subcadenas literales):
ESPERADO=("leidas 8 filas" "limpias 8 de 8 filas" "clientes con ventas: 4" "ACME,2110.50" "upstream_failed" "sigue intacto")

echo "[1/3] Construyendo el entorno desde entorno/Dockerfile ..."
docker --context "$CTX" build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/3] Ejecutando la demo en un contenedor limpio ..."
SALIDA="$(docker --context "$CTX" run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh')"
printf '%s\n' "$SALIDA"

echo "[3/3] Comprobando la salida ..."
FALLO=0
for trozo in "${ESPERADO[@]}"; do
  if printf '%s' "$SALIDA" | grep -qF -- "$trozo"; then
    echo "  ok   $trozo"
  else
    echo "  FALTA  $trozo"
    FALLO=1
  fi
done
[ "$FALLO" -eq 0 ] || { echo "✘ La salida no es la esperada."; exit 1; }

echo
echo "✔ Prueba terminada sin errores."
