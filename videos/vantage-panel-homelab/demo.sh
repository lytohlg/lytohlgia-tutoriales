#!/usr/bin/env bash
# Demo del vídeo «Vantage: un panel para tu red y tus servidores» — @lytohlgIA
# Mismo orden que en el vídeo. Rutas relativas, nada hardcodeado, ninguna credencial real.
# Todo ocurre en localhost: no hace falta homelab, ni router, ni pfSense.
set -euo pipefail
TRABAJO="$(mktemp -d)"
cd "$TRABAJO"
BACKEND=/opt/vantage/backend

echo "== 0. Qué hay en esta máquina =="
python -V
python -c "import fastapi, sqlalchemy, uvicorn; print('fastapi', fastapi.__version__)"

echo
echo "== 1. La clave maestra: 32 bytes aleatorios que no salen de aquí =="
head -c 32 /dev/urandom | base64 > clave.key
chmod 600 clave.key
wc -c clave.key
export VANTAGE_MASTER_KEY_FILE="$TRABAJO/clave.key"
export VANTAGE_DATABASE_URL="sqlite:///$TRABAJO/vantage.db"

echo
echo "== 2. La base de datos: sus migraciones, en SQLite =="
cd "$BACKEND" && alembic upgrade head 2>&1 | tail -3

echo
echo "== 3. Arranco el backend (FastAPI) y compruebo que responde =="
cd "$TRABAJO"
uvicorn --factory app.main:create_app --host 127.0.0.1 --port 8000 --no-proxy-headers > uvicorn.log 2>&1 &
SRV=$!
for _ in $(seq 1 30); do curl -sf http://127.0.0.1:8000/healthz >/dev/null 2>&1 && break; sleep 1; done
curl -s http://127.0.0.1:8000/healthz; echo

echo
echo "== 4. El primer admin: un código de un solo uso, no una contraseña por defecto =="
CODIGO=$(python -m app.cli setup-code | tail -1)
echo "codigo: $CODIGO"
curl -s -c cookies.txt -H 'Content-Type: application/json' -X POST http://127.0.0.1:8000/api/v1/setup \
  -d "{\"setup_code\":\"$CODIGO\",\"username\":\"admin\",\"password\":\"Mi-Clave-Larga-2026\"}"; echo
curl -s -b cookies.txt http://127.0.0.1:8000/api/v1/me; echo

echo
echo "== 5. Un dispositivo de la red local: qué integraciones trae =="
curl -s -b cookies.txt http://127.0.0.1:8000/api/v1/integrations \
  | python -c "import sys,json;print(', '.join(i['type_id'] for i in json.load(sys.stdin)))"

echo
echo "== 6. Pruebo una IP de mi red: la política la deja pasar =="
# Dirección de ejemplo de una red doméstica (rango privado RFC 1918): es la puerta de enlace que
# trae por defecto casi cualquier router. No es la red de nadie en concreto; aquí solo sirve para
# que la política vea una dirección privada. Se compone en el propio script para no dejar
# direcciones privadas escritas en el material.
LAN_IP="${LAN_IP:-$(printf '%s.%s.%s.%s' 192 168 1 1)}"
CSRF=$(curl -s -b cookies.txt http://127.0.0.1:8000/api/v1/me | python -c "import sys,json;print(json.load(sys.stdin)['csrf_token'])")
curl -s -b cookies.txt -H 'Content-Type: application/json' -H "X-CSRF-Token: $CSRF" \
  -X POST http://127.0.0.1:8000/api/v1/instances/test \
  -d "{\"type_id\":\"http_check\",\"name\":\"router\",\"config\":{\"url\":\"http://$LAN_IP/\",\"expected_status\":200,\"verify_tls\":true,\"timeout_seconds\":3}}"; echo

echo
echo "== 7. Y ahora el guardián: lo que NO puede tocar =="
for URL in "http://127.0.0.1:8000/healthz" "https://example.com/"; do
  echo "   -> $URL"
  curl -s -b cookies.txt -H 'Content-Type: application/json' -H "X-CSRF-Token: $CSRF" \
    -X POST http://127.0.0.1:8000/api/v1/instances/test \
    -d "{\"type_id\":\"http_check\",\"name\":\"x\",\"config\":{\"url\":\"$URL\",\"expected_status\":200,\"verify_tls\":false,\"timeout_seconds\":3}}"; echo
done

kill $SRV 2>/dev/null || true
