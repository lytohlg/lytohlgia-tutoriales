#!/usr/bin/env bash
# Demo del vídeo «PyInstaller: tu script en un programa que corre sin Python» — @lytohlgIA
# Mismo orden que en el vídeo. Sin red, sin credenciales: la imagen ya trae pyinstaller y rich.
# Se ejecuta sobre una COPIA en /tmp: el árbol del paquete puede venir montado de solo lectura
# (así lo ejecuta el revisor) y PyInstaller necesita escribir build/ y dist/.
set -euo pipefail

ORIGEN="$(cd "$(dirname "$0")" && pwd)"
TRABAJO=/tmp/repro-pyinstaller
rm -rf "$TRABAJO" && mkdir -p "$TRABAJO"
cp -r "$ORIGEN"/. "$TRABAJO"/
cd "$TRABAJO"

echo "== 1. El programa antes de empaquetar: lee el CSV y saca la tabla =="
python resumen.py datos/ventas.csv

echo
echo "== 2. Compilar con una sola orden =="
pyinstaller --onefile --name resumen --add-data "plantilla.txt:." resumen.py 2>&1 | tail -2
ls -lh dist/resumen | awk '{print "ejecutable: " $5 "  " $9}'

echo
echo "== 3. La prueba de verdad: otro directorio, sin el código fuente al lado =="
rm -rf /tmp/prueba && mkdir -p /tmp/prueba
cp dist/resumen datos/ventas.csv /tmp/prueba/
cd /tmp/prueba
./resumen ventas.csv > salida.txt
head -3 salida.txt
echo "python disponible en esta carpeta: $(command -v python3 || echo NO)"

echo
echo "== 4. La versión que se rompe: busca la plantilla 'de al lado' =="
cd "$TRABAJO"
pyinstaller --onefile --name resumen_v1 resumen_v1.py > /dev/null 2>&1 || true
cp dist/resumen_v1 /tmp/prueba/ && cd /tmp/prueba
./resumen_v1 ventas.csv > fallo.txt 2>&1 || true
tail -2 fallo.txt

echo
echo "== 5. Lo que lleva dentro el ejecutable =="
cd "$TRABAJO"
pyi-archive_viewer -l dist/resumen > dentro.txt 2>&1
grep -E "libpython|plantilla" dentro.txt

echo
echo "== listo: un fichero de 11 MB que arranca donde no hay Python =="
