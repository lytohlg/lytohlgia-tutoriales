#!/usr/bin/env bash
# Demo del video «pdfplumber: extrae las tablas de un PDF a CSV sin copiar» — @lytohlgIA
# Son los comandos del video, en el mismo orden y con los mismos numeros.
# Rutas RELATIVAS: todo se escribe dentro de la carpeta donde ejecutes esto.
set -uo pipefail

echo "== la tabla esta en el PDF; el problema es que no la ves =="

echo
echo "-- 0. tres albaranes fabricados aqui, con el total calculado por el propio script"
rm -rf entrada salida salida_tocada
python3 scripts/crear_albaranes.py

echo
echo "-- 1. la estrategia por defecto: el que no tiene lineas dibujadas da 0 tablas"
python3 scripts/extraer.py --pdf entrada/albaran_0310.pdf | tail -3
python3 scripts/extraer.py --pdf entrada/albaran_0320.pdf | tail -2

echo
echo "-- 2. usando el texto como rejilla: encuentra algo, pero mal"
python3 scripts/extraer.py --pdf entrada/albaran_0320.pdf --estrategia text

echo
echo "-- 3. las columnas se sacan de la cabecera y se busca solo en la tabla"
python3 scripts/extraer.py --pdf entrada/albaran_0320.pdf --estrategia columnas

echo
echo "-- 4. todo a CSV: un fichero por PDF"
python3 scripts/volcar.py --carpeta entrada --salida salida
echo
cat salida/albaran_0320_tabla1.csv | head -4

echo
echo "-- 5. la comprobacion: recalculado contra el total impreso en cada PDF"
python3 scripts/verificar.py --carpeta entrada

echo
echo "-- 6. prueba negativa: alguien toca un importe en el CSV y la comprobacion lo caza"
cp -r salida salida_tocada
python3 scripts/tocar_csv.py salida_tocada/albaran_0310_tabla1.csv
if python3 scripts/verificar.py --csv salida_tocada --carpeta entrada; then
  echo "(inesperado: no lo ha cazado)"
else
  echo "(codigo de salida 1: no se manda a contabilidad)"
fi

echo
echo "-- 7. los limites, medidos"
python3 scripts/limites.py 2>&1

echo
echo "== VERIFICADO: 3 albaranes, 33 lineas, 0 descuadres =="
