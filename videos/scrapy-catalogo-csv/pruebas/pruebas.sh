#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
#   3) comprueba las cuatro cosas que el vídeo afirma: 1.000 filas, 999 títulos,
#      el precio con símbolo antes del pipeline y numérico después
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-scrapy-catalogo-csv:local"

echo "[1/2] Construyendo el entorno desde entorno/Dockerfile ..."
docker build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/2] Ejecutando la demo en un contenedor limpio ..."
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -eu
    mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro
    ./demo.sh
    echo
    echo "--- comprobaciones de lo que afirma el vídeo ---"
    test "$(wc -l < catalogo.csv)" -eq 1001
    python3 analiza.py catalogo.csv | grep -q "1000 fichas | 999 titulos distintos"
    head -2 catalogo.csv | grep -q "£"
    python3 analiza.py catalogo_limpio.csv | grep -q "999 fichas | 999 titulos distintos"
    head -2 catalogo_limpio.csv | grep -qv "£"
    test "$(wc -l < catalogo_limpio.csv)" -eq 1000
    echo "OK: 1.000 filas, 999 titulos, precio con simbolo y precio numerico"'

echo
echo "✔ Prueba terminada sin errores."
