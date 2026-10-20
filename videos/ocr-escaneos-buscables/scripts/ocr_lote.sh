#!/bin/bash
# OCR de TODOS los escaneados de entrada/, con una linea de resumen por documento.
set -u
mkdir -p salida
T0=$(date +%s)
for F in entrada/*.pdf; do
  B=$(basename "$F" .pdf)
  INI=$(date +%s)
  ocrmypdf --language spa --output-type pdf --optimize 0 "$F" "salida/${B}_ocr.pdf" >/dev/null 2>&1
  RC=$?
  FIN=$(date +%s)
  TAM=$(stat -c %s "salida/${B}_ocr.pdf" 2>/dev/null || echo 0)
  printf "%-24s rc=%s  %3ss  %8s bytes\n" "$(basename "$F")" "$RC" "$((FIN - INI))" "$TAM"
done
T1=$(date +%s)
echo "------------------------------------------"
echo "documentos procesados: $(ls -1 entrada/*.pdf | wc -l) | tiempo total: $((T1 - T0)) s"
