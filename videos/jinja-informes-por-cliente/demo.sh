#!/usr/bin/env bash
# Demo del vídeo «Jinja: el mismo informe para cada cliente sin copiar y pegar» — @lytohlgIA
# Reglas: rutas RELATIVAS, valores en variables de entorno, nada hardcodeado.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "== 1. Un comando, un informe por cliente =="
python3 generar.py

echo
echo "== 2. Comprobación del resultado: ¿cada informe es de su cliente? =="
python3 revisar.py

echo
echo "== 3. El '&' del nombre no rompe el HTML (autoescape) =="
grep -o "Ferretería La Clave &amp; Hijos" informes/informe_ferreteria_la_clave_hijos.html | head -1

echo
echo "== 4. La plantilla con descuento y los datos CON descuento: sale =="
python3 generar.py --datos datos/clientes_con_descuento.csv --plantilla informe_descuento.html --salida informes_desc
grep -h "Descuento aplicado" informes_desc/*.html

echo
echo "== 5. Los mismos datos SIN el campo descuento, con StrictUndefined: NO se envía =="
set +e
python3 generar.py --plantilla informe_descuento.html --salida informes_roto 2>&1 | tail -3
echo "codigo de salida: ${PIPESTATUS[0]}"
set -e

echo
echo "== 6. Lo mismo SIN StrictUndefined: el informe sale sin el descuento y no avisa =="
python3 generar.py --plantilla informe_descuento.html --salida informes_roto --sin-estricto
echo "-- ¿aparece la palabra Descuento en algún informe? --"
grep -c "Descuento" informes_roto/*.html || true

echo
echo "== 7. Cien clientes, el mismo código =="
python3 gen_clientes.py --n 100
t0=$(date +%s%N)
python3 generar.py --datos datos/clientes_100.csv --salida informes_100 --resumen
t1=$(date +%s%N)
echo "tiempo: $(( (t1 - t0) / 1000000 )) ms"
ls informes_100 | wc -l

echo
echo "✔ Fin de la demo."
