#!/usr/bin/env bash
# Demo del vídeo «python-docx: rellena contratos de Word sin dejar marcadores» — @lytohlgIA
# Son los comandos del vídeo, en el mismo orden y con los mismos números.
# Rutas RELATIVAS: todo se escribe dentro de la carpeta donde ejecutes esto.
set -uo pipefail
cd "$(dirname "$0")"

echo "== doce contratos en un comando, y ninguno con el nombre del cliente anterior =="

echo
echo "-- 0. la plantilla: cinco marcadores, uno de ellos partido en dos trozos"
python3 scripts/crear_plantilla.py
echo
python3 scripts/marcadores.py

echo
echo "-- 1. el atajo del XML: escribe los 12 y se cree que no queda ninguno"
rm -rf salida_xml
python3 scripts/sustituir_xml.py --csv scripts/clientes.csv

echo
echo "-- 2. el camino bueno: los 12 documentos, en un comando"
rm -rf salida
python3 scripts/rellenar.py --csv scripts/clientes.csv
echo
ls -1 salida

echo
echo "-- 3. la comprobación: se releen los 12 y se compara con el CSV"
python3 scripts/verificar.py --csv scripts/clientes.csv

echo
echo "-- 4. comprobación ajena: el XML de un documento, a pelo (unzip)"
unzip -p salida/contrato_01_*.docx word/document.xml | tr '<' '\n' | grep -o "Estimado/a [^<]*" | head -1
echo "marcadores {{ en el XML de los 12:" $(for f in salida/*.docx; do unzip -p "$f" word/document.xml; done | grep -c "{{")

echo
echo "-- 5. un cliente al que le falta el CIF: se detiene y NO emite su contrato"
python3 scripts/rellenar.py --csv scripts/clientes_con_hueco.csv | grep -E "DETENIDO|RESUMEN|medias"
echo "ficheros del cliente 13:" $(ls salida/contrato_13_* 2>/dev/null | wc -l)

echo
echo "-- 6. los límites, medidos"
python3 scripts/limites.py

echo
echo "== fin: 12 contratos rellenados, verificados uno a uno, y nada sale a medias =="
