#!/usr/bin/env bash
# Demo del vídeo «Panda Router: elige modelo por tarea y por coste, no por moda» — @lytohlgIA
# Reglas: rutas RELATIVAS, sin claves, todo el trabajo dentro de /tmp.
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/AICodeKing/PandaOrchestrator.git}"
TRABAJO="${TRABAJO:-/tmp/panda}"
FORM="./ver_ruta.py"
POOL="claude-haiku-5.5,claude-sonnet-5.5,claude-opus-5.5"
POOL_LOCAL="claude-haiku-5.5,claude-sonnet-5.5,claude-opus-5.5,ollama-qwen3-coder-30b,gpt-oss:20b"
FACIL="Rename a variable in utils.py"
DIFICIL="Migrate our Express auth middleware to use JWT refresh tokens and update all 12 call sites"

echo "== 1/3 clonar el proyecto (una vez, sin historial) =="
if [ ! -d "$TRABAJO/.git" ]; then
  git clone --depth 1 "$REPO_URL" "$TRABAJO"
fi
# El formateador de la tabla viaja con el material y se copia junto al proyecto,
# para que las rutas de dentro sean siempre relativas al directorio de trabajo.
cp -f scripts/ver_ruta.py "$TRABAJO/ver_ruta.py"
cd "$TRABAJO"

echo
echo "== 2/3 instalar el comando (las dependencias ya están en la imagen) =="
python3 -m pip install --user -q -e . --no-deps
export PATH="$HOME/.local/bin:$PATH"
panda-router --help > /dev/null
echo "instalado: panda-router 0.1.0"

echo
echo "== 3/3 las nueve decisiones del vídeo =="
echo
echo "-- 1. tarea facil, pool de tres, modo utilidad --"
panda-router route --no-log --task "$FACIL" --pool "$POOL" --mode max_utility --top-k 3 \
  | python3 "$FORM" 'facil / utilidad'

echo
echo "-- 2. tarea facil, modo calidad --"
panda-router route --no-log --task "$FACIL" --pool "$POOL" --mode max_quality --top-k 3 \
  | python3 "$FORM" 'facil / calidad'

echo
echo "-- 3. tarea facil, umbral 50 por ciento --"
panda-router route --no-log --task "$FACIL" --pool "$POOL" \
  --mode cheapest_above_threshold --min-p 0.50 --top-k 3 \
  | python3 "$FORM" 'facil / umbral 50'

echo
echo "-- 4. tarea dificil, modo utilidad --"
panda-router route --no-log --task "$DIFICIL" --pool "$POOL" --mode max_utility --top-k 3 \
  | python3 "$FORM" 'dificil / utilidad'

echo
echo "-- 5. tarea dificil, umbral 25 por ciento --"
panda-router route --no-log --task "$DIFICIL" --pool "$POOL" \
  --mode cheapest_above_threshold --min-p 0.25 --top-k 3 \
  | python3 "$FORM" 'dificil / umbral 25'

echo
echo "-- 6. catalogo completo, tarea facil --"
panda-router route --no-log --task "$FACIL" --mode max_utility --top-k 3 \
  | python3 "$FORM" 'facil / catalogo'

echo
echo "-- 7. catalogo completo, tarea dificil --"
panda-router route --no-log --task "$DIFICIL" --mode max_utility --top-k 3 \
  | python3 "$FORM" 'dificil / catalogo'

echo
echo "-- 8. limite de coste: 0,001 dolares --"
panda-router route --no-log --task "$DIFICIL" --pool "$POOL" \
  --max-cost 0.001 --top-k 3 \
  | python3 "$FORM" 'dificil / max-cost 0.001'

echo
echo "-- 9. solo modelos locales --"
panda-router route --no-log --task "$DIFICIL" --pool "$POOL_LOCAL" \
  --local-only --top-k 3 \
  | python3 "$FORM" 'dificil / local-only'

echo
echo "FIN: 9 decisiones, ninguna llamada a un modelo real"
