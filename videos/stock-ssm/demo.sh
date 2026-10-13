#!/usr/bin/env bash
# Demo del vídeo «Avisos de stock bajo con Python: inventario real en Docker» — @lytohlgIA
# Reglas: rutas RELATIVAS, valores en variables de entorno, nada hardcodeado.
#
#   bash demo.sh        -> todos los pasos, en orden
#   bash demo.sh 6      -> solo el paso 6
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$RAIZ"

APP="${SSM_APP:-/app}"
PY="${PYTHON:-python3}"
PUERTO="${SSM_PUERTO:-8000}"
API="http://127.0.0.1:${PUERTO}"
LOGIN="/accounts/login/"

[ -f .env ] || cp .env.example .env
set -a
. ./.env
set +a
# La aplicación guarda la base de datos donde le digas; aquí, dentro de esta carpeta.
export DB_NAME="$RAIZ/db.sqlite3"
export LOG_FILE="$RAIZ/ssm.log"
# Los scripts de `scripts/` importan la aplicación por su nombre (`ssm.settings`).
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$APP"

cabecera() { printf '\n### %s\n' "$1"; }

# ── sesiones con la API ───────────────────────────────────────────────────────────────────────
# La API pide sesión: se entra con el mismo formulario que usa una persona en el navegador.
token_csrf() {
  curl -s --max-time 20 -c "$2" "$API$LOGIN" -o /tmp/login.html
  grep -o 'name="csrfmiddlewaretoken" value="[^"]*"' /tmp/login.html | head -1 | cut -d'"' -f4 || true
}

sesion() { # sesion <usuario> <clave> <fichero_de_cookies>
  local tok codigo
  tok="$(token_csrf "$1" "$3")"
  codigo="$(curl -s --max-time 20 -b "$3" -c "$3" -e "$API$LOGIN" -o /tmp/login2.html \
    -w '%{http_code}' -d "username=$1" -d "password=$2" -d "csrfmiddlewaretoken=$tok" "$API$LOGIN")"
  if [ "$codigo" != "302" ]; then
    printf 'ERROR: el login de %s ha sido rechazado (HTTP %s, token de %s caracteres)\n' \
      "$1" "$codigo" "${#tok}" >&2
    return 1
  fi
}

api_get() { curl -s --max-time 20 -b "$2" -H 'Accept: application/json' "$API$1"; }

csrf_de_jar() { awk '$6 == "csrftoken" {print $7}' "$1" | tail -1; }

api_envia() { # api_envia <metodo> <ruta> <cookies> <datos...>
  local metodo="$1" ruta="$2" jar="$3"
  shift 3
  local args=()
  for dato in "$@"; do args+=(-d "$dato"); done
  curl -s --max-time 20 -b "$jar" -c "$jar" -e "$API$LOGIN" \
    -H "X-CSRFToken: $(csrf_de_jar "$jar")" -X "$metodo" "${args[@]}" "$API$ruta"
}

api_post() { local ruta="$1" jar="$2"; shift 2; api_envia POST "$ruta" "$jar" "$@"; }

api_patch() { local ruta="$1" jar="$2"; shift 2; api_envia PATCH "$ruta" "$jar" "$@"; }

servidor_arrancado() { [ "$(curl -s --max-time 5 -o /tmp/latido -w '%{http_code}' "$API$LOGIN")" = "200" ]; }

arranca_servidor() {
  if servidor_arrancado; then return 0; fi
  ( cd "$APP" && "$PY" manage.py runserver "127.0.0.1:${PUERTO}" >"$RAIZ/servidor.log" 2>&1 & )
  for _ in $(seq 1 40); do
    servidor_arrancado && { echo "servidor escuchando en $API"; return 0; }
    sleep 0.25
  done
  echo "ERROR: el servidor no ha arrancado; mira servidor.log" >&2
  return 1
}

# ── pasos ─────────────────────────────────────────────────────────────────────────────────────
paso_0() { # punto de partida reproducible: almacen limpio con el stock cargado
  cabecera "0. Punto de partida"
  pkill -f "manage.py runserver" >/dev/null 2>&1 || true
  rm -f "$DB_NAME" "$RAIZ/ssm.log" "$RAIZ/salida/avisos_estado.json"
  ( cd "$APP" && "$PY" manage.py migrate --noinput >/dev/null )
  ( cd "$APP" && "$PY" manage.py shell < "$RAIZ/scripts/alta_inicial.py" >/dev/null )
  ( cd "$APP" && "$PY" manage.py import_items "$RAIZ/entrada/stock.csv" >/dev/null )
  printf 'almacen limpio y stock cargado desde entrada/stock.csv\n'
  printf 'estado de partida: 12 articulos, ninguno por debajo del minimo\n'
}

paso_1() { # la base de datos
  cabecera "1. La base de datos del almacen"
  [ -d "$APP" ] || { echo "falta la aplicacion en $APP: construye la maquina (ver README)" >&2; exit 1; }
  "$PY" --version
  "$PY" -m django --version
  ( cd "$APP" && "$PY" manage.py migrate --noinput )
}

paso_2() { # usuarios y grupos
  cabecera "2. Usuarios y permisos"
  ( cd "$APP" && "$PY" manage.py shell < "$RAIZ/scripts/alta_inicial.py" )
}

paso_3() { # carga del stock
  cabecera "3. El stock que ya tienes, cargado desde la hoja"
  ( cd "$APP" && "$PY" manage.py import_items "$RAIZ/entrada/stock.csv" | tail -3 )
  printf '\n--- control por ORM ---\n'
  ( cd "$APP" && "$PY" "$RAIZ/scripts/control_stock.py" )
}

paso_4() { # la API
  cabecera "4. La API del almacen"
  arranca_servidor
  printf -- '-- sin sesion --\n'
  curl -s -o /tmp/r.json -w 'HTTP %{http_code}\n' "$API/api/items/"
  cat /tmp/r.json
  printf -- '\n-- con sesion (almacen) --\n'
  sesion "$DEMO_USUARIO_ALMACEN" "$DEMO_ALMACEN_CLAVE" /tmp/almacen.jar
  api_get "/api/items/?page_size=2" /tmp/almacen.jar | "$PY" -m json.tool
}

paso_5() { # baja de stock real
  cabecera "5. Baja de stock: la tienda pide y el almacen despacha"
  arranca_servidor
  sesion "$DEMO_USUARIO_ALMACEN" "$DEMO_ALMACEN_CLAVE" /tmp/almacen.jar
  sesion "$DEMO_USUARIO_TIENDA" "$DEMO_TIENDA_CLAVE" /tmp/tienda.jar
  pide() { # pide <sku> <unidades>
    printf '%s pide %s unidades de %s -> ' "$DEMO_USUARIO_TIENDA" "$2" "$1"
    api_post "/api/transfer/" /tmp/tienda.jar "sku=$1" "transfer_quantity=$2"
    printf ' | '
    api_post "/api/complete-transfer/" /tmp/almacen.jar "sku=$1" "quantity=$2" \
      "shop_user_id=$DEMO_USUARIO_TIENDA"
    printf '\n'
  }
  pide ALM-1004 8
  pide ALM-1010 5
  printf -- '\n-- lo que queda en el almacen (solo los que bajan de 15) --\n'
  api_get "/api/items/?ordering=sku&page_size=100" /tmp/almacen.jar | "$PY" "$RAIZ/scripts/lista_corta.py"
}

paso_6() { # el aviso
  cabecera "6. El aviso"
  arranca_servidor
  "$PY" "$RAIZ/scripts/avisos_stock.py"
}

paso_7() { # no repite + recuperacion
  cabecera "7. Repetir sin cambios y reponer"
  arranca_servidor
  printf -- '-- segunda pasada, sin tocar nada --\n'
  "$PY" "$RAIZ/scripts/avisos_stock.py"
  printf -- '\n-- el almacen repone ALM-1010 a 25 unidades --\n'
  api_patch "/api/items/ALM-1010/" /tmp/almacen.jar "sku=ALM-1010" "quantity=25"
  printf '\n'
  "$PY" "$RAIZ/scripts/avisos_stock.py"
}

paso_8() { # API caida
  cabecera "8. Si el almacen no contesta"
  set +e
  "$PY" "$RAIZ/scripts/avisos_stock.py" --api "http://127.0.0.1:8099"
  printf 'codigo de salida: %s\n' "$?"
  set -e
}

todo() {
  echo "== Avisos de stock bajo con Python: inventario real en Docker =="
  paso_0
  paso_1
  paso_2
  paso_3
  paso_4
  paso_5
  paso_6
  paso_7
  paso_8
  printf '\n== demo terminada ==\n'
}

case "${1:-todo}" in
  todo) todo ;;
  olvidar) "$PY" "$RAIZ/scripts/avisos_stock.py" --olvidar > /tmp/olvido.log; echo "avisos olvidados" ;;
  "")
    echo "uso: bash demo.sh [todo|0|1|2|3|4|5|6|7|8|olvidar] [mas pasos]" >&2; exit 1 ;;
  *)
    for p in "$@"; do
      case "$p" in
        0|1|2|3|4|5|6|7|8) "paso_$p" ;;
        *) echo "paso desconocido: $p (uso: todo|0..8|olvidar)" >&2; exit 1 ;;
      esac
    done ;;
esac
