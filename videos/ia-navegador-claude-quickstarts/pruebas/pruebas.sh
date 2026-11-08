#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, con la carpeta montada en
#      SOLO LECTURA (el script no puede tocar el original) y una copia de trabajo
#      en /tmp. Se ejecuta como root porque Chromium no arranca su sandbox como
#      root y el driver añade --no-sandbox en ese caso (ver cdp_browser.py).
#   3) comprueba las cuatro cosas que el vídeo afirma: 6 llamadas (4 respondidas
#      y 2 rechazadas), los ref_N del formulario, el bloqueo por política y la
#      negativa a usar una herramienta que el driver no implementa
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-ia-navegador-claude-quickstarts:local"

echo "[1/2] Construyendo el entorno desde entorno/Dockerfile ..."
docker build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/2] Ejecutando la demo en un contenedor limpio ..."
docker run --rm --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -eu
    mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro
    bash demo.sh
    echo
    echo "--- comprobaciones de lo que afirma el video ---"
    python3 exercise.py > /tmp/ej.txt 2>&1
    test "$(grep -c " -> answered" /tmp/ej.txt)" -eq 4
    test "$(grep -c " -> refused" /tmp/ej.txt)" -eq 2
    grep -q "is outside this exercise's page" /tmp/ej.txt
    grep -q "must be between 0 and 30 seconds" /tmp/ej.txt
    python3 mipagina.py > /tmp/mi.txt 2>&1
    grep -q "el enlace del listado es ref_" /tmp/mi.txt
    grep -q "F-101" /tmp/mi.txt
    grep -q "blocked: https://example.com" /tmp/mi.txt
    python3 fuera_del_driver.py > /tmp/fd.txt 2>&1
    grep -q "unknown browser toolset member" /tmp/fd.txt
    echo "OK: 6 llamadas (4 respondidas, 2 rechazadas), refs del formulario, bloqueo por politica"'

echo
echo "✔ Prueba terminada sin errores."
