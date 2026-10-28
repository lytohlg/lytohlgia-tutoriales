#!/usr/bin/env bash
# Demo del vídeo «WeasyPrint: facturas en PDF desde HTML y CSS, sin maquetar a mano» — @lytohlgIA
# Todo lo que imprime es salida real de WeasyPrint 70.0 sobre este mismo material.
set -euo pipefail
cd "$(dirname "$0")"

LARGA=datos/factura-2026-1042.json
CORTA=datos/factura-2026-1043.json
mkdir -p salida

echo "== 1) un HTML y una hoja de estilos se convierten en un PDF"
python scripts/generar.py "$LARGA" salida/factura.pdf
python scripts/verificar.py salida/factura.pdf "$LARGA"

echo
echo "== 2) la cabecera y la numeración: no están escritas en ninguna página"
pdftotext -layout salida/factura.pdf - | grep -nE "Factura F-|Página [0-9] de"

echo
echo "== 3) la cabecera de la tabla, en todas las páginas o solo en la primera"
python scripts/generar.py "$LARGA" salida/sin-regla.pdf estilos/sin-regla.css
python scripts/verificar.py salida/sin-regla.pdf "$LARGA"

echo
echo "== 4) el mismo HTML, otro cliente: un PDF de una página"
python scripts/generar.py "$CORTA" salida/factura-corta.pdf
python scripts/verificar.py salida/factura-corta.pdf "$CORTA"

echo
echo "== 5) los dos límites que tienes que saber"
python scripts/limites.py

echo
python scripts/comprobar.py
