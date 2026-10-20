#!/bin/bash
# Busca una frase dentro de TODOS los PDF de una carpeta y dice en cual esta.
# Uso: bash buscar.sh "renta mensual" salida
set -u
FRASE="${1:?falta la frase}"
CARPETA="${2:-salida}"
ENCONTRADOS=0
for F in "$CARPETA"/*.pdf; do
  [ -e "$F" ] || continue
  LINEA=$(pdftotext "$F" - 2>/dev/null | grep -i -m1 -- "$FRASE")
  if [ -n "$LINEA" ]; then
    ENCONTRADOS=$((ENCONTRADOS + 1))
    echo "ENCONTRADO en $(basename "$F")"
    echo "   $LINEA"
  fi
done
echo "--------------------------------------"
echo "documentos revisados: $(ls -1 "$CARPETA"/*.pdf 2>/dev/null | wc -l) | con la frase: $ENCONTRADOS"
