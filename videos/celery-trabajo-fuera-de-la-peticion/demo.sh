#!/usr/bin/env bash
# Demo del vídeo «Celery: ejecuta tareas lentas sin bloquear tu web» — @lytohlgIA
# ---------------------------------------------------------------------------
# Ejecuta TODO de verdad: Redis, la web, el trabajador, los reintentos y los estados.
# Tarda alrededor de minuto y medio: los ocho segundos de trabajo son ocho segundos reales.
set -euo pipefail
cd "$(dirname "$0")"

# Si algo falla, que se vea el registro de la web: sin eso, un error del servidor
# aparece solo como "curl: (52) Empty reply from server".
al_fallar() {
  echo "--- algo fallo; ultimas lineas de /tmp/web.log ---"
  tail -n 3 /tmp/web.log 2>/dev/null | cut -c1-110 || echo "(no hay registro)"
}
trap al_fallar ERR

echo "== 0) el tercero: Redis guarda la cola y los resultados"
redis-server --daemonize yes --save '' --appendonly no --dir /tmp
sleep 1
redis-cli ping

echo
echo "== 1) el informe se hace DENTRO de la peticion (lo que se cuelga)"
python app.py > /tmp/web.log 2>&1 &
WEB=$!
trap 'al_fallar; kill "$WEB" 2>/dev/null || true' ERR
trap 'kill "$WEB" 2>/dev/null || true' EXIT
# esperar a que escuche de verdad (importar celery tarda un momento)
for _ in $(seq 1 40); do
  curl -s -o /dev/null "http://127.0.0.1:8000/nada" && break
  sleep 0.25
done
curl -s -o /dev/null -w 'respuesta en: %{time_total}s\n' "http://127.0.0.1:8000/informe?cliente=ACME"

echo
echo "== 2) el mismo informe ENCOLADO, todavia sin trabajador"
for c in ACME BETA GAMMA; do
  curl -s "http://127.0.0.1:8000/informe-cola?cliente=$c"
  echo
done
echo -n "tareas esperando en la cola: "
redis-cli LLEN celery

echo
echo "== 3) arranca el trabajador y se lleva las tres tareas"
celery -A tareas worker --loglevel=info --concurrency=1 \
  --detach --pidfile=/tmp/worker.pid --logfile=/tmp/worker.log
sleep 28
grep -E "ready|Task tareas.informe" /tmp/worker.log | sed 's/^/[trabajador] /'

echo
echo "== 4) una tarea que falla: la cola reintenta sola, con espera creciente"
curl -s "http://127.0.0.1:8000/cobro-cola?cliente=ACME"
echo
sleep 22
grep -E "Retry|raised|succeeded in" /tmp/worker.log | sed 's/^/[trabajador] /'

echo
echo "== 5) el estado de una tarea, consultado desde el codigo"
ID=$(curl -s "http://127.0.0.1:8000/informe-cola?cliente=DELTA" | sed 's/.*"tarea": "//; s/".*//')
echo "tarea: $ID"
python estado.py "$ID"

echo
echo "== 6) que queda dentro de Redis"
redis-cli --scan | sed 's/^/[redis] /' | head -8
echo -n "tareas sin confirmar (unacked): "
redis-cli LLEN unacked 2>/dev/null || echo "0"
