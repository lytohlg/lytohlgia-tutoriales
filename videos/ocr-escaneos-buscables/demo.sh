#!/usr/bin/env bash
# Demo del vídeo «OCRmyPDF: convierte un PDF escaneado en texto que se puede buscar» — @lytohlgIA
# Son los comandos del vídeo, en el mismo orden y con los mismos números.
# Rutas RELATIVAS: todo se escribe dentro de la carpeta donde ejecutes esto.
set -euo pipefail

echo "== de foto a texto: OCR sobre escaneos, con comprobación =="

echo
echo "-- 1. tres escaneos de verdad (imagen, sin capa de texto)"
python3 scripts/sembrar_escaneos.py

echo
echo "-- 2. cuánto texto tiene cada uno ANTES (pdftotext)"
python3 scripts/estado.py entrada

echo
echo "-- 3. así se ve el original: ni una letra que buscar"
pdftotext entrada/contrato_alquiler.pdf - | head -3 || true
echo "(vacío: el PDF es una imagen)"

echo
echo "-- 4. el comando: añadir la capa de texto a toda la carpeta"
bash scripts/ocr_lote.sh

echo
echo "-- 5. cuánto texto tiene cada uno DESPUÉS"
python3 scripts/estado.py salida

echo
echo "-- 6. lo que antes no se podía buscar"
bash scripts/buscar.sh "renta mensual" salida
echo
bash scripts/buscar.sh "presupuesto" salida

echo
echo "-- 7. la misma búsqueda en la carpeta SIN procesar (no hay nada que buscar)"
bash scripts/buscar.sh "renta mensual" entrada

echo
echo "-- 8. un documento suelto, contado paso a paso (bytes y segundos)"
bash scripts/ocr_uno.sh contrato_alquiler.pdf

echo
echo "-- 9. repetir el comando no duplica el texto (--skip-text)"
ocrmypdf --language spa --skip-text --output-type pdf \
    salida/contrato_alquiler_ocr.pdf salida/contrato_otra_vez.pdf
A=$(pdftotext salida/contrato_alquiler_ocr.pdf - | tr -d '\f' | wc -c)
B=$(pdftotext salida/contrato_otra_vez.pdf - | tr -d '\f' | wc -c)
echo "caracteres antes: $A | después de repetir el comando: $B"

echo
echo "-- 10. el límite: qué pasa con un escaneo malo"
python3 scripts/limite.py

echo
echo "== fin: los PDF de salida/ tienen texto y se pueden buscar =="
