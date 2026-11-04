#!/usr/bin/env bash
# Arranca el proveedor falso y el gateway con la configuración de la demo.
# Usa $PWD para que funcione igual en el contenedor del vídeo y en tu copia.
set -u
TRABAJO="${TRABAJO:-$PWD}"
pkill -f upstream.py 2>/dev/null
pkill -x llmux 2>/dev/null
sleep 0.3

python3 "$TRABAJO/scripts/upstream.py" 9000 > "$TRABAJO/upstream.log" 2>&1 &
llmux --listen 127.0.0.1:8095 \
      --upstream http://127.0.0.1:9000 \
      --api-key local-demo \
      --model-map gpt-4=gpt-4o-mini \
      --set-header "X-Team: research" \
      --sqlite "$TRABAJO/trafico.db" > "$TRABAJO/llmux.log" 2>&1 &
sleep 1.5
echo "gateway en :8095 -> proveedor falso en :9000"
