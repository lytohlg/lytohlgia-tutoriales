#!/bin/bash
# Prepara el almacén de ejemplo desde cero, sin ninguna copia previa:
# esquema → usuario admin → servidor → token de API → datos por la API REST → copia de la base.
#
# Uso: ./scripts/preparar_almacen.sh [_snap/00_inicial.sqlite3]
#
# Se ejecuta sola la primera vez que `arrancar.sh` recibe una copia que no existe. Tarda
# 2-3 minutos (las migraciones de InvenTree son lo que más tarda); después, arrancar la demo
# con la copia ya hecha es cuestión de segundos.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1
BASE="$PWD"
DESTINO="${1:-_snap/00_inicial.sqlite3}"

# Rutas y variables de InvenTree, todas dentro de la carpeta (ver scripts/env.sh)
. scripts/env.sh

echo "1/5 · esquema sobre una base vacía (tarda un poco)"
rm -f database.sqlite3 database.sqlite3-wal database.sqlite3-shm
if ! ( cd "$INVENTREE_BACKEND_DIR/InvenTree" && python3 manage.py migrate --noinput > /tmp/migrate.log 2>&1 ); then
    tail -8 /tmp/migrate.log
    exit 1
fi
tail -1 /tmp/migrate.log

echo "2/5 · usuario admin"
( cd "$INVENTREE_BACKEND_DIR/InvenTree" && \
  DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=inventree \
  DJANGO_SUPERUSER_EMAIL=admin@example.com \
  python3 manage.py createsuperuser --noinput > /tmp/admin.log 2>&1 ) || true
tail -1 /tmp/admin.log

echo "3/5 · servidor en marcha"
bash scripts/arrancar.sh

echo "4/5 · token de API y datos de ejemplo, por la API REST"
( cd "$INVENTREE_BACKEND_DIR/InvenTree" && python3 "$BASE/scripts/_token.py" )
export INVENTREE_TOKEN="$(cat "$BASE/.token")"
export INVENTREE_URL=http://127.0.0.1:8000
python3 scripts/sembrar.py

echo "5/5 · copia de la base ya sembrada"
python3 scripts/_guardar.py "$DESTINO"

# El servidor de este paso no hace falta para nada más: se para para no ocupar el puerto.
pkill -f "gunicorn" 2>/dev/null || true
sleep 1
echo "almacén preparado: $DESTINO"
