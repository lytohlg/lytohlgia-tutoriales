#!/usr/bin/env bash
# Demo del vídeo «El validador dijo OK y guardó una fecha que no existe: pydantic» — @lytohlgIA
# Mismo orden que en el vídeo. Rutas relativas, nada hardcodeado, ninguna credencial.
set -euo pipefail

echo "== 0. Qué hay dentro del CSV (6 pedidos, sin validar nada) =="
python mirar_csv.py

echo
echo "== 1. El validador manual: dice que todo está bien =="
python valida_manual.py datos/pedidos.csv
echo "-- lo que ha guardado como bueno:"
cat pedidos_limpios.csv

echo
echo "== 2. Instalación (después de ver el problema) =="
python -m pip install --quiet --disable-pip-version-check --root-user-action=ignore "pydantic==2.12.3" "email-validator==2.3.0" || true
python -c "import pydantic; print('pydantic', pydantic.VERSION)"

echo
echo "== 3. El mismo CSV, con un modelo declarativo =="
python modelo.py datos/pedidos.csv

echo
echo "== 4. Una columna mal escrita ya no se ignora =="
python modelo.py datos/pedidos_typo.csv

echo
echo "== 5. Dos reglas propias: coma decimal y estado en mayúsculas =="
python normaliza.py datos/pedidos.csv

echo
echo "== 6. El límite: el id repetido no lo ve el modelo, lo ve el lote =="
python revisar_lote.py

echo
echo
echo "== 7. El flujo real: lo que pasa sale limpio, lo que no pasa va al informe =="
python limpia.py
echo "-- lo que debería llegar a la base de datos:"
cat pedidos_ok.csv
echo "-- la lista de trabajo para arreglar el origen:"
cat informe.csv

echo
echo "== listo: las filas malas salen con nombre y motivo; el id repetido lo caza el lote =="
