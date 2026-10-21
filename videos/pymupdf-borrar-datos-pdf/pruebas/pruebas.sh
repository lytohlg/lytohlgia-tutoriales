#!/usr/bin/env bash
# Prueba reproducible del paquete «pymupdf-borrar-datos-pdf».
# Ejecuta el MISMO comando que declara paquete.json y comprueba los números del vídeo.
set -euo pipefail

SALIDA="$(bash demo.sh 2>&1)"
echo "$SALIDA" | tail -20

fallos=0
comprobar() {
  if echo "$SALIDA" | grep -qF "$1"; then
    echo "OK   $1"
  else
    echo "FALLO (no aparece): $1"
    fallos=$((fallos + 1))
  fi
}

comprobar "datos personales localizados en total: 13"
comprobar "veces que el DNI sigue apareciendo en el texto: 1"
comprobar "zonas marcadas para redactar: 1"
comprobar "veces que el DNI aparece en el texto guardado: 0"
comprobar "datos detectados: 13 | zonas redactadas: 13"
comprobar "datos detectados: 14 | zonas redactadas: 14"
comprobar "TOTAL de secretos que siguen en los documentos: 1"
comprobar "TOTAL de secretos que siguen en los documentos: 0"
comprobar "campos con datos del autor que quedan: 0"
comprobar "escaneo: caracteres de texto = 0 | zonas encontradas del DNI = 0"

if [ "$fallos" -ne 0 ]; then
  echo "PRUEBAS: $fallos comprobaciones fallidas"
  exit 1
fi
echo "PRUEBAS: todas las comprobaciones en verde"
