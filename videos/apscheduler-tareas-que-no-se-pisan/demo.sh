#!/usr/bin/env bash
# Demo del vídeo: un script que se ejecuta solo, no se pisa y sobrevive al reinicio.
# Todo lo que imprime es salida real de APScheduler 3.11.3.
set -euo pipefail
cd "$(dirname "$0")"

export AGENDA_DB="${AGENDA_DB:-agenda.sqlite}"
SAL="$(mktemp -d)"
rm -f "$AGENDA_DB"

echo "== 1) una tarea cada 2 segundos, sin nadie delante =="
python scripts/informe.py | tee "$SAL/informe.txt"

echo
echo "== 2) tarea de 3 s programada cada 1 s: max_instances=1 =="
python scripts/lento.py 2>&1 | tee "$SAL/lento.txt"

echo
echo "== 3) tarea con hora vencida y 60 s de gracia =="
python scripts/perdido.py 2>&1 | tee "$SAL/perdido.txt"

echo
echo "== 4) guardar la agenda en disco y salir del proceso =="
python scripts/agenda.py | tee "$SAL/agenda.txt"

echo
echo "== 5) otro proceso lee el mismo fichero y ejecuta lo guardado =="
python scripts/listar.py 2>&1 | tee "$SAL/listar.txt"

echo
python scripts/comprobar.py "$SAL"
rm -rf "$SAL"
