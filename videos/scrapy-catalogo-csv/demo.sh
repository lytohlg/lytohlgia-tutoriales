#!/usr/bin/env bash
# Demo del vídeo «Scrapy: reunir un catalogo entero en un CSV sin escribir un bucle» — @lytohlgIA
# Son los mismos comandos del vídeo, en el mismo orden, con rutas relativas.
set -euo pipefail

echo "== 1) El bucle manual: una pagina, veinte filas =="
python3 lento.py

echo
echo "== 2) Crear el proyecto y el spider =="
rm -rf catalogo
scrapy startproject catalogo
cp spiders/libros.py catalogo/catalogo/spiders/libros.py
wc -l catalogo/catalogo/spiders/libros.py

echo
echo "== 3) Primera pasada: el catalogo entero a CSV =="
( cd catalogo && scrapy crawl libros -O ../catalogo.csv 2>&1 \
    | grep -E "item_scraped_count|response_received_count|elapsed_time_seconds" )
wc -l catalogo.csv
head -4 catalogo.csv
python3 analiza.py catalogo.csv

echo
echo "== 4) El pipeline: precio a numero y descarte del repetido =="
cp pipelines.py catalogo/catalogo/pipelines.py
cat settings_add.py >> catalogo/catalogo/settings.py
( cd catalogo && scrapy crawl libros -O ../catalogo_limpio.csv 2>&1 \
    | grep -E "item_scraped_count|item_dropped_count|elapsed_time_seconds" )
head -3 catalogo_limpio.csv
python3 analiza.py catalogo_limpio.csv

echo
echo "== Listo: dos CSV, 1.000 fichas y un duplicado descartado =="
