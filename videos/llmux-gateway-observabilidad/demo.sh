#!/usr/bin/env bash
# Demo del vídeo, de principio a fin. Todo lo que imprime es salida real.
set -uo pipefail
cd "$(dirname "$0")"

rm -f trafico.db upstream.log llmux.log
echo "== 1) arrancar proveedor falso + gateway =="
bash scripts/arranque.sh

echo
echo "== 2) la puerta: sin clave y con clave =="
bash scripts/pide.sh sin-clave
bash scripts/pide.sh con-clave

echo
echo "== 3) la consulta del cliente real (SDK de OpenAI) =="
python3 scripts/cliente.py local-demo

echo
echo "== 4) la captura en SQLite =="
sqlite3 -header -column trafico.db "select status, model from exchanges;"
echo
echo "-- el mapeo del modelo, medido fila a fila (0 = no aparece, 1 = aparece) --"
sqlite3 -header trafico.db "select req_body like '%gpt-4o-mini%' as en_lo_que_pedi, up_req_body like '%gpt-4o-mini%' as en_lo_que_salio from exchanges;"
echo
echo "-- la credencial: entra con Authorization, sale sin ella --"
sqlite3 -header trafico.db "select req_headers like '%local-demo%' as clave_en_la_entrada, up_req_headers like '%local-demo%' as clave_en_la_salida from exchanges;"

echo
python3 scripts/comprobar.py trafico.db
pkill -f upstream.py 2>/dev/null
pkill -x llmux 2>/dev/null
exit 0
