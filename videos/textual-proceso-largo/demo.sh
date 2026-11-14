#!/usr/bin/env bash
# Demo del vídeo «Textual: ve qué falla en un proceso largo sin leer 240 líneas» — @lytohlgIA
# En el mismo orden que en pantalla. Todo lo que sale aquí es salida real: los 240 ficheros
# se generan, se procesan de verdad y los dos fallos que quedan los produce el código.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf lote salida salida.log

echo "== 1) doscientos cuarenta extractos, y alguno con el importe mal escrito =="
python generar_lote.py 240
echo -n "ficheros en lote/: "; ls lote | wc -l
head -4 lote/extracto_001.csv
head -4 lote/extracto_041.csv

echo
echo "== 2) el camino de siempre: una línea por fichero =="
python -u lote_print.py --pausa 0 > salida.log 2>&1 || true
head -3 salida.log
echo "..."
tail -3 salida.log
grep -n "ERROR" salida.log || true

echo
echo "== 3) la misma tarea en una sola pantalla que se redibuja =="
COLUMNS=100 LINES=32 script -qec "python panel.py --pausa 0.01 --espera-final 1" /dev/null | tail -21

echo
echo "== 4) el fichero que está mal, pasado solo =="
python uno.py lote/extracto_041.csv || true

echo
echo "== 5) se corrige el dato y se vuelve a pasar =="
sed -i 's/,\([0-9][0-9]\) EUR/.\1/' lote/extracto_041.csv
head -3 lote/extracto_041.csv
COLUMNS=100 LINES=32 script -qec "python panel.py --pausa 0 --espera-final 1" /dev/null | tail -7

echo
echo "== 6) lo que queda en disco cuando la pantalla se cierra =="
echo -n "JSON en salida/: "; ls salida | wc -l
cat salida/extracto_001.json
echo
python comprobar.py
