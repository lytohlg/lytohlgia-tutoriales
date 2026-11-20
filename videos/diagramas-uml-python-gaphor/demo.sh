#!/usr/bin/env bash
# Demo del vídeo «Genera diagramas UML desde tu código Python con Gaphor» — @lytohlgIA
# Son exactamente los comandos que se ejecutan en pantalla, en el mismo orden.
set -euo pipefail

echo "== 1. Un modelo UML escrito en Python: se guarda y se exporta =="
python3 modelo.py
ls -l salida/Pedidos/

echo
echo "== 2. El modelo es texto y la imagen es una imagen =="
head -c 220 pedidos.gaphor
echo
file salida/Pedidos/Pedidos.png

echo
echo "== 3. Del código existente al diagrama (ast) =="
python3 desde_codigo.py tienda
ls -l salida_tienda/Tienda/

echo
echo "== 4. Añadimos una clase y volvemos a lanzar el mismo script =="
cat tienda_v2/devoluciones.py
python3 desde_codigo.py tienda_v2
ls -l salida_tienda_v2/Tienda_v2/

echo
echo "✔ Listo: dos modelos .gaphor y sus PNG/SVG en salida/ y salida_*."
