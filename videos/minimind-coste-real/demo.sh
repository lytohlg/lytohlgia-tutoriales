#!/bin/bash
# Reproduce el experimento del vídeo: preentreno real de MiniMind en CPU.
# Uso: bash demo.sh   (PASOS=5 y SEGUNDOS=150 por defecto)
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
cd "$AQUI"
TRABAJO="build"
PASOS="${PASOS:-5}"

mkdir -p "$TRABAJO"
if [ ! -d "$TRABAJO/minimind/.git" ]; then
  echo "[1/4] clonando el proyecto (commit 858008e, el del vídeo)"
  git clone --depth 1 https://github.com/jingyaogong/minimind.git "$TRABAJO/minimind"
  git -C "$TRABAJO/minimind" checkout -q 858008eb98da4428f78053a1cc4d3a3bd5973629
fi
cd "$TRABAJO/minimind"

echo "[2/4] datos: muestra local de $((PASOS * 8)) líneas"
mkdir -p dataset
head -n $((PASOS * 8)) ../../datos/muestra_200.txt > dataset/muestra.jsonl

echo "[3/4] entrenando $PASOS pasos en CPU (esto tarda minutos, no segundos)"
cd trainer
timeout "${SEGUNDOS:-150}" python train_pretrain.py \
  --epochs 1 --batch_size 8 --accumulation_steps 4 \
  --log_interval 1 --save_interval 1000 --num_workers 0 --max_seq_len 340 \
  --data_path ../dataset/muestra.jsonl > "../../entreno.log" 2>&1 || true
cd ../..

echo "[4/4] midiendo el log"
python ../medir.py entreno.log
