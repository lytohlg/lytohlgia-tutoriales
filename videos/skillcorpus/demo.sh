#!/usr/bin/env bash
# Demo del vídeo «SkillCorpus: 222 skills de agente filtradas y buscables con Python» — @lytohlgIA
# ---------------------------------------------------------------------------
# Es la lista de comandos del vídeo, en el mismo orden y sin nada decorativo. Cada bloque imprime el
# comando que ejecuta (con el `$` delante) para poder leerlo junto al vídeo.
# Una diferencia deliberada, y solo una: el `git clone` se queda en el commit del vídeo en lugar del
# HEAD de hoy (ver README.md, «Resultado esperado»). Sin ese pin el recuento no cuadraría.
set -euo pipefail

COMMIT="${SKILLCORPUS_COMMIT:-7b3a0eaec5594b7f6cb301189c3d626f15409ed0}"
URL="https://github.com/EverMind-AI/SkillCorpus"
LIB="${SKILLCORPUS_LIB:-/work/lib}"
DEPLOY="${SKILLCORPUS_DEPLOY:-/opt/deploy}"

echo "== SkillCorpus: 222 skills de agente filtradas y buscables con Python =="

echo "\$ git clone --depth 1 $URL"
git clone --depth 1 "$URL" 2>&1 | sed 's/^/  /'
cd SkillCorpus
# La única diferencia con el vídeo, y está a la vista: el repositorio se queda donde estaba al grabar.
git fetch -q --depth 1 origin "$COMMIT"
git checkout -q "$COMMIT"
git log -1 --format='  (fijado en %h del %ad)' --date=short

echo
echo "\$ pip install -e ."
pip install -e . 2>&1 | tail -3 | sed 's/^/  /'

echo
echo "\$ python -m skillcorpus.cli --lib $LIB --config $DEPLOY/config.yaml build --sources-config $DEPLOY/mis_fuentes.yaml"
python -m skillcorpus.cli --lib "$LIB" --config "$DEPLOY/config.yaml" build \
  --sources-config "$DEPLOY/mis_fuentes.yaml"

echo
echo "\$ python examples/skillhub_demo.py \"extract tables from a scanned PDF invoice\""
python examples/skillhub_demo.py "extract tables from a scanned PDF invoice"

echo
echo "\$ ls -la $LIB/corpus && head -16 $LIB/corpus/README.md"
ls -la "$LIB/corpus" && head -16 "$LIB/corpus/README.md"

echo
echo "\$ python $DEPLOY/report.py"
python "$DEPLOY/report.py"
