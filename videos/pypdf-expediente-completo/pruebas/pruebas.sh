#!/usr/bin/env bash
# Prueba reproducible del paquete «pypdf-expediente-completo».
# Ejecuta el MISMO comando que declara paquete.json y comprueba los números del vídeo.
set -euo pipefail

SALIDA="$(bash demo.sh 2>&1)"
echo "$SALIDA" | tail -25

fallos=0
comprobar() {
  if echo "$SALIDA" | grep -qF "$1"; then
    echo "OK   $1"
  else
    echo "FALLO (no aparece): $1"
    fallos=$((fallos + 1))
  fi
}

comprobar "EXPEDIENTE INCOMPLETO: no se une y no se entrega."
comprobar "falta: certificado_empresa.pdf"
comprobar "ILEGIBLE (PdfStreamError)"
comprobar "ilegible: nomina_ultima.pdf (PdfStreamError)"
comprobar "EXPEDIENTE COMPLETO: 6 documentos, 9 paginas. Se puede unir."
comprobar "1 hoja(s) con marca de giro del escaner"
comprobar "unidas 9 paginas de 6 documentos | hojas enderezadas: 1"
comprobar "cifrado: AES-256 con clave del entorno (EXPEDIENTE_CLAVE)"
comprobar "bloqueado: FileNotDecryptedError"
comprobar "cifrado detectado por qpdf: AES-256 (AESv3)"
comprobar "VERIFICADO: 6 documentos en el orden del indice, 9 paginas, cifrado AES-256, ninguna hoja girada"
comprobar "MANIFIESTO CUADRA: 6 documentos, 9 paginas, cada marcador en su pagina"
comprobar "caracteres extraidos de la hoja dibujada: 0"

if [ "$fallos" -ne 0 ]; then
  echo "PRUEBAS: $fallos comprobaciones fallidas"
  exit 1
fi
echo "PRUEBAS: todas las comprobaciones en verde"
