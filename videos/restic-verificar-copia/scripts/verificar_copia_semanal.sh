#!/usr/bin/env bash
# Verificación semanal de la copia: restaura la última copia, compara fichero a
# fichero por sha256 y deja el informe del día en $TRABAJO/informes. El código de
# salida lo mira el cron: 0 = copia buena, 1 = hay que restaurar de verdad.
#
# En el vídeo esa carpeta es la del contenedor de la demo (work, en su raíz). Aquí se pasa en
# la variable TRABAJO para que la pongas donde quieras; en el cron, con tu ruta absoluta.
set -uo pipefail

: "${TRABAJO:?Falta TRABAJO: la carpeta donde estan datos/ y copias/ (p. ej. la ruta de tu carpeta de trabajo)}"
PYTHON="${PYTHON:-python3}"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export RESTIC_PASSWORD_FILE="$TRABAJO/.restic-pass"
mkdir -p "$TRABAJO/informes"
"$PYTHON" "$AQUI/verificar_copia.py" \
    --repo "$TRABAJO/copias/repo" \
    --datos "$TRABAJO/datos" \
    --destino "$TRABAJO/verificacion" \
    --informe "$TRABAJO/informes/$(date -u +%F).json"
