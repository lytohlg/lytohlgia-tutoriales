#!/usr/bin/env bash
# Demo del vídeo «Cómo detectar el código falso que escribe una IA» — @lytohlgIA
# Lo que se ve en pantalla, en el mismo orden. Rutas relativas, todo dentro de esta carpeta.
# El repositorio público se trae con ./traer_repo.sh (revisión fijada).
#
# Nota sobre el proyecto falso: los ficheros de C van guardados como `.c.txt` porque el índice
# de este repositorio didáctico no admite extensiones de código compilado. La demo los copia a una
# carpeta de trabajo en /tmp con su extensión real `.c` y audita esa copia, nunca estos originales.
set -uo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"

if [ ! -d repo ]; then
  ./traer_repo.sh
fi

AUDIT="repo/skills/hardware-in-the-loop/templates/tools/audit_placeholders.py"

# --- preparacion: el proyecto falso, con las extensiones reales, en una copia de trabajo
TRABAJO="${TMPDIR:-/tmp}/proyecto_falso"
rm -rf "$TRABAJO"
cp -r proyecto_falso "$TRABAJO"
mv "$TRABAJO/firmware/barometro.c.txt" "$TRABAJO/firmware/barometro.c"

echo "== 0) El proyecto que el agente dio por terminado =="
find "$TRABAJO" -name '*.c' -o -name '*.py' | sort
echo

echo "== 1) La puerta mira el proyecto, sin exigir nada =="
python3 -I "$AUDIT" --root "$TRABAJO"
echo "codigo de salida: $?"
echo

echo "== 2) La misma puerta, exigiendo que bloquee =="
python3 -I "$AUDIT" --root "$TRABAJO" --fail-on-new
echo "codigo de salida: $?"
echo

echo "== 3) La deuda que ya existia se firma como linea base =="
python3 -I "$AUDIT" --root "$TRABAJO" --write-baseline > /dev/null
python3 -I "$AUDIT" --root "$TRABAJO" --fail-on-new
echo "codigo de salida: $?"
echo

echo "== 4) El agente anade un driver mas, con la misma trampa =="
cp nuevo/bomba.c.txt "$TRABAJO/firmware/bomba.c"
python3 -I "$AUDIT" --root "$TRABAJO" --fail-on-new
echo "codigo de salida: $?"
echo

echo "== 5) El andamio del metodo, generado desde las respuestas del proyecto =="
python3 -I repo/skills/hardware-in-the-loop/scripts/scaffold.py \
  --answers answers.json --dest "${TMPDIR:-/tmp}/mi_placa" | head -3
echo

echo "== 6) La puerta sobre el andamio recien creado =="
cd "${TMPDIR:-/tmp}/mi_placa"
python3 -I tools/audit_placeholders.py --root . --fail-on-new
echo "codigo de salida: $?"
echo
echo "Listo: la puerta informa, bloquea lo nuevo, y el andamio nace en verde."
