#!/usr/bin/env bash
# Demo del vídeo «Automatiza 300 fotos de producto con Pillow en minutos» — @lytohlgIA
# Mismo orden que en el vídeo. Rutas relativas, nada hardcodeado, ninguna credencial.
set -euo pipefail

echo "== 0. La marca de agua y las 300 fotos del proveedor (se generan aquí, semilla fija) =="
python datos/marca.py datos/marca.png
python datos/generar_fotos.py datos/fotos 300

echo
echo "== 1. Qué trae la carpeta: variedad y suciedad, contadas =="
python medir.py datos/fotos

echo
echo "== 2. La versión de cinco minutos: se cae en la cuarta foto =="
python lote_ingenuo.py datos/fotos salida_ingenuo || echo "(se ha caído: eso es lo que se demuestra)"
echo "fotos escritas antes de caerse: $(ls salida_ingenuo | wc -l) de 300"

echo
echo "== 3. Sin aplicar el giro que pide el EXIF =="
python lote.py datos/fotos salida_singiro --sin-giro
python comprobar.py salida_singiro

echo
echo "== 4. El lote completo =="
python lote.py datos/fotos salida
python comprobar.py salida

echo
echo "== 5. La marca de agua, por diferencia de píxeles (misma foto, con y sin) =="
python verificar_marca.py "$(ls datos/fotos/*.JPG | head -1)"

echo
echo "== 6. Cuánto cuesta cada punto de calidad (misma foto a 70, 82 y 95) =="
python calidad.py "$(ls datos/fotos/*.JPG | head -1)"

echo
echo "== 7. El registro: qué entró, qué salió y cuáles hay que mirar =="
head -3 registro.csv
echo "filas OK: $(grep -c ',OK,' registro.csv) · filas DANADA: $(grep -c ',DANADA,' registro.csv)"
grep ',DANADA,' registro.csv

echo
echo "== listo: 300 fotos entran, salen iguales y las rotas quedan listadas =="
