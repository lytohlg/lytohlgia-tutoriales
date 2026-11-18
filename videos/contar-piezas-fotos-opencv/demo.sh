#!/usr/bin/env bash
# Demo del vídeo «OpenCV en Python: contar piezas en una foto y que el número cuadre» — @lytohlgIA
# Reglas: rutas RELATIVAS, nada hardcodeado, nada de red.
#
# Son los mismos comandos que se ven en el vídeo, en el mismo orden.
# La instalación no está aquí porque va aparte (el vídeo la enseña en su propio paso):
#   pip install opencv-python-headless==4.10.0.84 numpy==2.1.3
# Ver la sección «Pasos» del README.
set -euo pipefail

echo "== OpenCV en Python: contar piezas en una foto y que el número cuadre =="
echo

echo "1) Las fotos: 12 bandejas y un manifiesto con lo que hay de verdad"
python3 generar_fotos.py --salida fotos | tail -3
echo

echo "2) Contar con umbral + contornos (lo primero que hace todo el mundo)"
python3 contar.py --carpeta fotos --verdad fotos/manifiesto.csv
echo

echo "3) Las que fallan, una por una"
python3 contar.py --carpeta fotos --verdad fotos/manifiesto.csv | grep FALTAN
echo

echo "4) La bandeja vacía: cero también es una respuesta"
python3 contar.py --foto fotos/p06.png
grep -n AREA_ contar.py
echo

echo "5) La peor de las doce, con las dos formas de contarla"
python3 contar.py --foto fotos/p10.png
python3 contar.py --foto fotos/p10.png --separar-tocadas
echo

echo "6) Las doce fotos, partiendo las piezas que se tocan"
python3 contar.py --carpeta fotos --verdad fotos/manifiesto.csv --separar-tocadas \
    --salida informe_tocadas.csv --marcadas marcadas_tocadas
echo

echo "7) El CSV que se lleva a Excel"
head -4 informe_tocadas.csv
wc -l informe_tocadas.csv
echo

echo "8) Hasta dónde aguanta: 70, 80 y 90 por ciento de solape"
for s in 0.70 0.80 0.90; do
    python3 generar_fotos.py --salida "d$s" --solape "$s" --solo p10 > /dev/null
    echo "--- solape $s"
    python3 contar.py --carpeta "d$s" --verdad "d$s/manifiesto.csv" --separar-tocadas | tail -3
done
echo
echo "Fotos marcadas en marcadas_tocadas/ (una caja por pieza, numerada)."
