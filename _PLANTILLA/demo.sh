#!/usr/bin/env bash
# Plantilla de demo — @lytohlgIA
# Reglas: rutas RELATIVAS, valores en variables de entorno, NADA hardcodeado.
set -euo pipefail

# Si hace falta una clave, se lee del entorno y se avisa claro si falta:
# : "${MI_CLAVE:?Falta MI_CLAVE en el entorno (copia .env.example a .env y rellénalo)}"

echo "== TÍTULO DEL VÍDEO =="
# Aquí van los comandos REALES del vídeo, en el mismo orden en que se ven en el vídeo.
