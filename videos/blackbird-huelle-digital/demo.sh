#!/usr/bin/env bash
# Demo del vídeo «Blackbird: en qué 653 webs existe tu nombre de usuario (y cuáles no eres tú)» — @lytohlgIA
# Reglas: rutas RELATIVAS, valores en variables de entorno, nada hardcodeado.
set -euo pipefail

# Nombre de usuario de ejemplo: un nombre PÚBLICO (Linus Torvalds). No hace falta
# ninguna clave: cambia USUARIO por el tuyo y el resultado será el tuyo.
USUARIO="${USUARIO:-torvalds}"
DIR_BB="${DIR_BB:-blackbird}"

command -v git >/dev/null 2>&1 || { echo "Falta git: apt-get install -y git"; exit 1; }

echo "== 1. La herramienta: quién la firma y qué hace =="
if [ ! -d "$DIR_BB" ]; then
  git clone -q --depth 1 https://github.com/antoniaci/blackbird.git "$DIR_BB"
fi
cd "$DIR_BB"

echo "== 2. Instalación (una vez) =="
python3 -m pip install -q -r requirements.txt
python3 blackbird.py --about > /tmp/about.txt 2>&1 || true
sed -n '13,20p' /tmp/about.txt

echo "== 3. Búsqueda completa: un nombre de usuario en 653 webs =="
python3 blackbird.py -u "$USUARIO" --no-nsfw --csv --json --timeout 10 > /tmp/busqueda.txt 2>&1
tail -4 /tmp/busqueda.txt
echo "-- lo que queda en disco --"
ls results/*/ | head -5

echo "== 4. Verificación de cada hallazgo (nuestro script) =="
cp ../huelle.py .
python3 huelle.py "$USUARIO" --saltar-busqueda

echo "== 5. El informe =="
sed -n '1,12p' "results/informe_${USUARIO}.md"
