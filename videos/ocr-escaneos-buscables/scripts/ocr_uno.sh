#!/bin/bash
# OCR de UN documento, con tiempo y tamano antes/despues.
# Uso: bash ocr_uno.sh nombre.pdf
set -u
F="$1"
BASE="${F%.pdf}"
mkdir -p salida

ANTES=$(stat -c %s "entrada/$F")
T0=$(date +%s)
ocrmypdf --language spa --output-type pdf --optimize 0 \
         "entrada/$F" "salida/${BASE}_ocr.pdf" --skip-big 50 2>&1 | tail -4
T1=$(date +%s)
DESPUES=$(stat -c %s "salida/${BASE}_ocr.pdf" 2>/dev/null || echo 0)

echo "---------------------------------------------"
echo "documento:   $F"
echo "antes:       $ANTES bytes (imagen)"
echo "despues:     $DESPUES bytes (imagen + texto)"
echo "tiempo OCR:  $((T1 - T0)) s"
