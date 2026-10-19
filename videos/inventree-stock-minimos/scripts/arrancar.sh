#!/bin/bash
# Arranca InvenTree dentro de este contenedor y espera a que la API conteste.
#
# Uso:
#   ./scripts/arrancar.sh                          -> arranca sobre la base que ya haya
#   ./scripts/arrancar.sh _snap/00_inicial.sqlite3 -> restaura esa copia antes de arrancar
#
# La primera vez no existe ninguna copia: en vez de fallar, se prepara el almacén de ejemplo
# desde cero (esquema, usuario, token y datos) con scripts/preparar_almacen.sh, que deja la
# copia pedida lista. Así la secuencia del vídeo se puede repetir tal cual, empezando de cero.
cd "$(dirname "$0")/.." || exit 1
BASE="$PWD"

# Rutas y variables de InvenTree, todas dentro de la carpeta (ver scripts/env.sh)
. scripts/env.sh

if [ -n "${1:-}" ] && [ ! -f "$1" ]; then
    echo "todavía no existe $1: preparo el almacén de ejemplo (2-3 min la primera vez)"
    bash scripts/preparar_almacen.sh "$1" || exit 1
fi

if [ -n "${1:-}" ]; then
    python3 scripts/_restore.py "$1" || exit 1
fi

cd "$INVENTREE_HOME" || exit 1
nohup python3 -m gunicorn -c ./gunicorn.conf.py InvenTree.wsgi \
    -b 0.0.0.0:8000 --chdir "$INVENTREE_BACKEND_DIR/InvenTree" \
    > /tmp/gunicorn.log 2>&1 &

for _ in $(seq 1 40); do
    sleep 1
    if python3 "$BASE/scripts/_ping.py" > /dev/null 2>&1; then
        echo "InvenTree listo · API en http://127.0.0.1:8000/api/"
        exit 0
    fi
done
echo "InvenTree NO arrancó"
tail -3 /tmp/gunicorn.log
exit 1
