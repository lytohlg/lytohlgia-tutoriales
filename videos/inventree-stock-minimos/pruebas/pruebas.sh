#!/usr/bin/env bash
# Comprobaciones del paquete: la demo tiene que dar los números que se ven en el vídeo.
#
# Ejecuta el MISMO comando que se declara en el paquete (`bash demo.sh`, la secuencia
# completa) y verifica sobre su salida real las tres cosas que el vídeo afirma:
#   · antes del consumo, 3 referencias por debajo del mínimo
#   · después del consumo, 4
#   · el parte de reposición es un CSV con su cabecera
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

echo "== ejecutando la demo completa (la primera vez prepara el almacén: 2-3 min) =="
salida="$(bash demo.sh 2>&1)"
printf '%s\n' "$salida" | tail -25

grep -q "3 referencia(s) por debajo del mínimo" <<< "$salida" \
  || { echo "KO: el estado inicial no da 3 referencias bajo mínimo"; exit 1; }
grep -q "4 referencia(s) por debajo del mínimo" <<< "$salida" \
  || { echo "KO: tras el consumo no da 4 referencias bajo mínimo"; exit 1; }
grep -q "referencia,pieza,disponible,minimo,pedir" <<< "$salida" \
  || { echo "KO: el CSV del parte no tiene cabecera"; exit 1; }
grep -q "3 referencias antes del consumo y 4 después" <<< "$salida" \
  || { echo "KO: la demo no resume el resultado esperado"; exit 1; }

echo "OK: 3 referencias antes, 4 después, CSV con cabecera y resumen final"
