#!/usr/bin/env bash
# Comprobaciones del paquete: ejecuta LA MISMA demo que declara el manifiesto (bash demo.sh)
# y verifica la salida. No sustituye a la demo: la corre igual y luego mira el resultado.
set -uo pipefail
cd "$(dirname "$0")/.."

fallos=0
comprobar() { if grep -q "$1" "$2"; then echo "OK    $1"; else echo "FALLO $1"; fallos=$((fallos+1)); fi; }

echo "== ejecutando la demo del manifiesto: bash demo.sh =="
bash demo.sh > /tmp/salida_demo.txt 2>&1
echo "codigo de salida de la demo: $?"

comprobar "INFORME DE VENTAS" /tmp/salida_demo.txt
comprobar "Top 5 clientes" /tmp/salida_demo.txt
comprobar "filas: 120" /tmp/salida_demo.txt
comprobar "FileNotFoundError" /tmp/salida_demo.txt
comprobar "libpython" /tmp/salida_demo.txt

filas_csv=$(( $(wc -l < datos/ventas.csv) - 1 ))
if [ "$filas_csv" -eq 120 ]; then echo "OK    csv con 120 filas"
else echo "FALLO csv con $filas_csv filas"; fallos=$((fallos+1)); fi

echo "fallos: $fallos"
exit $((fallos > 0))
