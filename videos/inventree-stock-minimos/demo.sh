#!/usr/bin/env bash
# Demo del vídeo «InvenTree: controla el stock de tus componentes con Python» — @lytohlgIA
# Hace, en este orden, lo mismo que se ve en pantalla:
#   arrancar InvenTree → estado del almacén → qué falta → dónde está →
#   registrar un consumo → volver a preguntar → parte de reposición en CSV
#
#   bash demo.sh        -> la secuencia completa
#   bash demo.sh 4      -> solo el paso 4
#
# La primera vez prepara el almacén de ejemplo desde cero (2-3 minutos: crea el esquema,
# el usuario, el token y siembra los datos por la API). Después arranca en segundos,
# porque reutiliza la copia de la base en _snap/.
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$RAIZ"
[ -f .env ] || cp .env.example .env
set -a; . ./.env; set +a

paso() { printf '\n### %s\n' "$1"; }
QUIERE="${1:-todos}"
toca() { [ "$QUIERE" = "todos" ] || [ "$QUIERE" = "$1" ]; }

if [ ! -f _snap/00_inicial.sqlite3 ]; then
  paso "0 · primera vez: preparar el almacén de ejemplo"
  bash scripts/preparar_almacen.sh _snap/00_inicial.sqlite3
fi

if [ ! -f .token ]; then
  # El token de API se genera una vez en la base de datos y se guarda en .token
  ( cd "$INVENTREE_BACKEND_DIR/InvenTree" && python3 "$RAIZ/scripts/_token.py" )
fi

if toca 1; then
  paso "1 · arrancar InvenTree con el almacén de ejemplo"
  bash scripts/arrancar.sh _snap/00_inicial.sqlite3
  source scripts/env.sh
  python3 scripts/estado.py
fi

if toca 2; then
  paso "2 · qué está por debajo del mínimo"
  source scripts/env.sh
  python3 scripts/revisar_stock.py
fi

if toca 3; then
  paso "3 · dónde está cada unidad"
  source scripts/env.sh
  python3 scripts/donde.py ESP32-WROOM
  python3 scripts/historial.py ESP32-WROOM
fi

if toca 4; then
  paso "4 · el técnico gasta 3 ESP32 y 60 conectores"
  source scripts/env.sh
  python3 scripts/consumo.py ESP32-WROOM=3 JST-XH4=60
  # El estado justo después del consumo también se guarda: es la copia que usa el paso 6
  # del vídeo cuando se ejecuta por separado.
  python3 scripts/_guardar.py _snap/10_tras_consumo.sqlite3
fi

if toca 5; then
  paso "5 · la misma pregunta, después del consumo"
  source scripts/env.sh
  python3 scripts/revisar_stock.py
fi

if toca 6; then
  paso "6 · el parte de reposición en CSV"
  source scripts/env.sh
  python3 scripts/lista_compra.py
  echo
  echo "--- salida/lista_compra.csv ---"
  cat salida/lista_compra.csv
fi

echo
echo "RESULTADO: 3 referencias antes del consumo y 4 después; el parte está en salida/lista_compra.csv"
