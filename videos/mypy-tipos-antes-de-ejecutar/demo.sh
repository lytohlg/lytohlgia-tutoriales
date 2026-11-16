#!/usr/bin/env bash
# Demo del vídeo «mypy: encuentra el error de tipos antes de ejecutar el programa» — @lytohlgIA
# Reproduce, en el mismo orden que el vídeo, cómo un fallo de forma (un texto donde
# se espera un número, un None que se usa como número) se ve ANTES de ejecutar.
# Rutas relativas, sin datos personales: se puede ejecutar en un contenedor limpio.
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"

echo "== 1. EL PUNTO DE PARTIDA: el proyecto entero, tal cual está =="
cd proyecto
mypy . || true
echo

echo "== 2. POR QUÉ IMPORTA: el mismo proyecto, ejecutado con un dato real =="
python main.py || true
echo

echo "== 3. EL AVISO CON CONTEXTO: fichero, línea y tipo esperado =="
mypy --pretty --show-error-codes main.py || true
echo

echo "== 4. EL ARREGLO: se copia el proyecto, se aplica el parche de verdad =="
cd "$AQUI"
rm -rf /tmp/arreglado
cp -r proyecto /tmp/arreglado
cd /tmp/arreglado
patch -p1 < "$AQUI/arreglo.txt"
echo

echo "== 5. AHORA: mypy limpio y el programa hace su trabajo =="
mypy .
python main.py
echo

echo "== 6. EL CÓDIGO VIEJO: sin anotaciones no hay nada que comprobar =="
cd "$AQUI/legacy"
echo "-- mypy sin --strict:"
mypy . || true
echo "-- mypy --strict:"
mypy --strict . || true
echo "-- el programa funciona igual (los avisos son de forma, no de funcionamiento):"
python limpieza.py
