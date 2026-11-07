#!/usr/bin/env bash
# Demo del vídeo «Tres agentes de IA en el mismo repositorio sin pisarse» — @lytohlgIA
# ---------------------------------------------------------------------------------
# Es la misma secuencia que se ve en pantalla, en el mismo orden: se crea el registro,
# se dan de alta tres ventanas, se abre una tarea con dueño y revisor, se intenta
# demostrar con una prueba DISTINTA de la pactada (el sistema la rechaza), se demuestra
# con la pactada, se entrega el paquete, el revisor lo acusa y lo revisa, y se cierra.
#
# Todo lo que se escribe (registro, alcance, informe) va a una carpeta temporal: el
# repositorio se clona aparte con ./traer_repo.sh y NO se modifica.
#
# Requisitos: python3 (3.12+), git. La imagen de entorno/Dockerfile ya los trae.
set -uo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"

if [ ! -d repo ]; then
  echo "== 0) Traigo el repositorio público (revisión fijada) =="
  ./traer_repo.sh
  echo
fi

TRABAJO="${TMPDIR:-/tmp}/trabajo_squadra"
REG="$TRABAJO/registro"
rm -rf "$TRABAJO"
mkdir -p "$REG"

PROYECTO="$AQUI/repo"
S() { python3 -B "$PROYECTO/scripts/squadra.py" --root "$REG" "$@"; }

echo "== 1) Qué versión exacta del material se está usando =="
python3 -B "$PROYECTO/scripts/squadra.py" --version
echo

echo "== 2) Registro nuevo y tres ventanas dadas de alta =="
cd "$PROYECTO"
S init --name escuadra --project "$PROYECTO" --lang en --temporary | grep committed
S agent --id coord --identity Coordinador --role coordinator --client manual --repo "$PROYECTO" | grep committed
S agent --id builder --identity Constructor --role builder --client manual --repo "$PROYECTO" | grep committed
S agent --id reader --identity Revisor --role reviewer --client manual --repo "$PROYECTO" | grep committed
echo "-- censo de ventanas --"
S census --project "$PROYECTO" | grep '"agent"'
echo

echo "== 3) El alcance y la PRUEBA se escriben antes de empezar =="
printf 'Verificar el entorno antes de tocar codigo.\n' > "$TRABAJO/alcance.md"
printf '["python3","-B","scripts/squadra.py","--version"]\n' > "$TRABAJO/prueba.json"
cat "$TRABAJO/alcance.md"
cat "$TRABAJO/prueba.json"
echo

echo "== 4) Tarea con dueño, revisor, alcance y prueba pactada =="
S task --actor coord --id T1 --owner builder --reviewer reader --title "Verificar el entorno" \
      --repo "$PROYECTO" --scope-file "$TRABAJO/alcance.md" --proof-file "$TRABAJO/prueba.json" \
      | grep -E 'committed|"task"'
echo "-- el constructor acusa recibo y arranca --"
S ack --actor builder --message assign-T1 | grep committed
S start --actor builder --task T1 | grep committed
echo

echo "== 5) Intento de demostrar con OTRA prueba (debe ser rechazado) =="
S prove --actor builder --task T1 -- python3 -B scripts/squadra.py doctor --quick | grep -i 'proof'
echo

echo "== 6) Demostración con la prueba pactada (debe ser aceptada) =="
S prove --actor builder --task T1 -- python3 -B scripts/squadra.py --version | tail -4
echo

echo "== 7) Entrega: paquete con hash y copia congelada =="
S deliver --actor builder --task T1 | sed -n '1,5p'
echo

echo "== 8) El revisor recibe el paquete y lo acusa =="
IN=$(S inbox --agent reader)
echo "$IN" | sed -n '1,12p'
ID=$(echo "$IN" | sed -n 's/.*"id": "\(review-[0-9a-f]*\)".*/\1/p' | awk 'NR==1')
echo "paquete: $ID"
S ack --actor reader --message "$ID" | grep committed
echo

echo "== 9) Revisión independiente y cierre de la tarea =="
printf 'Aceptado: la prueba se ejecuto sobre el paquete entregado.\n' > "$TRABAJO/informe.md"
S review --actor reader --task T1 --verdict accepted --report "$TRABAJO/informe.md" | grep -E 'committed|review'
S check --actor coord --task T1 | grep -iE 'verified|closed'
S close --actor coord --task T1 | grep committed
echo

echo "== 10) Tablero final =="
S board | tail -8
