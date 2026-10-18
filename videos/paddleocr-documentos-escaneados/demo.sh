#!/usr/bin/env bash
# Demo del vídeo «PaddleOCR: busca dentro de tus PDF escaneados con Python» — @lytohlgIA
# Reglas: rutas RELATIVAS, valores en variables de entorno, nada hardcodeado.
# Ejecútala desde la raíz de esta carpeta:   bash demo.sh
set -euo pipefail

echo "== PaddleOCR: busca dentro de tus PDF escaneados con Python =="

echo
echo "-- 1. Con qué se ha hecho la prueba ----------------------------------------"
python3 scripts/entorno.py

echo
echo "-- 2. El corpus de prueba (documentos inventados, escaneados de verdad) -----"
python3 scripts/generar_corpus.py

echo
echo "-- 3. El problema: ni el PDF ni la carpeta se pueden buscar -----------------"
# Un PDF escaneado es una imagen: no tiene capa de texto. Cero caracteres extraíbles.
echo -n "caracteres que saca pdftotext de una factura: "
pdftotext "documentos/factura_02_F-2026-0442.pdf" - | wc -c
echo -n "ficheros de la carpeta que contienen F-2026-0443 buscando texto: "
grep -rIl "F-2026-0443" documentos | wc -l || true

echo
echo "-- 4. Índice: OCR de cada página a una base de datos local -------------------"
python3 scripts/indexar.py

echo
echo "-- 5. Llega una factura nueva: el índice lee SOLO lo que ha cambiado --------"
cp documentos_nuevos/*.pdf documentos/
python3 scripts/indexar.py

echo
echo "-- 6. La búsqueda que antes era imposible -----------------------------------"
python3 scripts/buscar.py "F-2026-0443"
python3 scripts/buscar.py "MANT-2026-03"

echo
echo "-- 7. Comprobación campo a campo contra la verdad del corpus -----------------"
python3 scripts/comprobar.py

echo
echo "-- 8. Dónde falla: un documento mal escaneado -------------------------------"
python3 scripts/limites.py

echo
echo "== Fin de la demo =="
