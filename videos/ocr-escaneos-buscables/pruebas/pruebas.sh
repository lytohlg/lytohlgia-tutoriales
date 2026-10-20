#!/usr/bin/env bash
# Prueba del paquete: ejecuta la demo y comprueba que el resultado está.
# El comando es el mismo que declara paquete.json («bash demo.sh»).
set -uo pipefail
cd "$(dirname "$0")/.."

echo "prueba: bash demo.sh sobre el entorno construido con entorno/Dockerfile"
SALIDA=$(bash demo.sh 2>&1)
RC=$?
echo "$SALIDA" | tail -40

fallos=0
comprobar() {
    if echo "$SALIDA" | grep -q -- "$1"; then
        echo "  OK   $1"
    else
        echo "  FALLO $1"
        fallos=$((fallos + 1))
    fi
}

comprobar "sin capa de texto: 3"
comprobar "documentos procesados: 3"
comprobar "sin capa de texto: 0"
comprobar "ENCONTRADO en contrato_alquiler_ocr.pdf"
comprobar "con la frase: 0"
comprobar "conserva el importe (780)"

if [ "$RC" -ne 0 ]; then
    echo "FALLO: la demo terminó con código $RC"
    fallos=$((fallos + 1))
fi

echo "----------------------------------------"
if [ "$fallos" -eq 0 ]; then
    echo "PRUEBA OK: la demo se reproduce y los resultados están"
    exit 0
fi
echo "PRUEBA KO: $fallos comprobaciones fallidas"
exit 1
