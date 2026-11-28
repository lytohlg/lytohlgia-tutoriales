#!/usr/bin/env bash
# Demo del vídeo «Plotly: tu CSV en un gráfico interactivo que se abre en el navegador» — @lytohlgIA
# Mismo orden que en el vídeo. Rutas relativas, nada hardcodeado, ninguna credencial.
# Los datos de datos/ventas.csv son de EJEMPLO (sintéticos, generados con gen_datos.py).
set -euo pipefail
mkdir -p salida

echo "== 0. El fichero tal cual sale de Excel (separador ; y coma decimal) =="
head -4 datos/ventas.csv

echo
echo "== 1. Abrirlo en Python: primero sale mal, y así se lee bien =="
python carga.py

echo
echo "== 2. Barras por tienda: un HTML que se abre en el navegador =="
python barras.py

echo
echo "== 3. La misma facturación, mes a mes y con una línea por tienda =="
python linea.py

echo
echo "== 4. Los dos gráficos en un solo informe =="
python informe.py

echo
echo "== 5. Con tus datos: cambias la columna y la ruta, nada más =="
python personaliza.py --columna producto

echo
echo "== 6. El error que te vas a encontrar: pedir una columna que no existe =="
# La última línea del error real es el mensaje de Plotly (incluye las columnas que sí hay).
python error.py 2>&1 | tail -1 || true
python arreglo.py

echo
echo "== 7. Lo que se abre en el navegador (ficheros generados) =="
ls -lh salida/
echo "   -> doble clic en salida/informe.html: es un fichero, no hace falta servidor"

echo
echo "== listo: un CSV se convierte en gráficos interactivos que puedes enviar como un solo fichero =="
