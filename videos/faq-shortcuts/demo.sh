#!/usr/bin/env bash
# Demo del vídeo «Encuentra lo que repites en tu historial de IA y tapa tus claves» — @lytohlgIA
# Son los MISMOS comandos que se ven en pantalla, en el mismo orden.
# Rutas relativas a esta carpeta: no hay ninguna ruta de máquina.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d repo ]; then
  echo "== el material trae el repositorio original (revisión fijada) =="
  ./traer_repo.sh
  echo
fi

echo "== 0. escenario: historial sintético de 3 agentes =="
python3 escenario.py
export HOME="$PWD/entrada/home"
export CODEX_HOME="$HOME/.codex"
export XDG_CONFIG_HOME="$HOME/.config"
PROY="$PWD/entrada/proyecto-facturas"

echo
echo "== 1. dónde vive el historial =="
ls -1
find entrada -type f | sort
wc -l "$HOME/.claude/history.jsonl" "$HOME"/.codex/sessions/2026/10/01/*.jsonl
head -n 2 "$HOME/.claude/history.jsonl"

echo
echo "== 2. un comando, tres formatos =="
python3 repo/scripts/extract_asks.py "$PROY" | head -9
python3 repo/scripts/extract_asks.py "$PROY" | wc -l
python3 repo/scripts/extract_asks.py "$PROY" --format jsonl | tail -2

echo
echo "== 3. el secreto que estaba dentro =="
python3 repo/scripts/extract_asks.py "$PROY" | grep -i 'api de facturacion'
grep -o 'sk-proj-[A-Za-z0-9]*' "$HOME/.claude/history.jsonl"
python3 repo/scripts/extract_asks.py "$PROY" --no-redact | grep -i 'api de facturacion'
python3 repo/scripts/extract_asks.py "$PROY" | grep -c REDACTED

echo
echo "== 4. contar lo que repites =="
python3 repo/scripts/extract_asks.py "$PROY" | python3 contar.py
python3 repo/scripts/extract_asks.py "$PROY" --since 2026-09-01 | python3 contar.py
python3 repo/scripts/extract_asks.py "$PROY" --source codex | wc -l

echo
echo "== 5. los tests del repositorio (no hace falta creérselo) =="
(cd repo && python3 -m pytest --collect-only -q 2>&1 | tail -7)
(cd repo && python3 -m pytest -v 2>&1 | grep -E 'secrets_are_redacted|min_words|unreadable_source|few_prompts' || true)
(cd repo && python3 -m pytest -q 2>&1 | tail -3)

echo
echo "== fin. la lista es el material; los comandos los eliges tú =="
