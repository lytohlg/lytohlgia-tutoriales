#!/usr/bin/env bash
# Demo del vídeo «Pon los números de tu negocio en un JSON y el script te dice si pierdes dinero» — @lytohlgIA
# ---------------------------------------------------------------------------------
# Es la MISMA secuencia que se ve en pantalla, en el mismo orden: el caso de ejemplo
# del repositorio, el año uno con sus escenarios, mis propios números con el veredicto
# del plan en «no», el análisis de precio a partir de un CSV, el panel de compradores
# y el plan compilado.
#
# El repositorio del autor se clona aparte (./traer_repo.sh) y NO se modifica: la demo
# trabaja sobre la copia que hace ella misma en una carpeta temporal.
#
# Requisitos: python3 (3.10+) y git. La imagen de entorno/Dockerfile ya los trae.
# No hay nada que instalar con pip: las cuatro herramientas son biblioteca estándar.
set -uo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"

if [ ! -d repo ]; then
  ./traer_repo.sh
  echo
fi

TRABAJO="${TMPDIR:-/tmp}/trabajo_founder"
rm -rf "$TRABAJO"
mkdir -p "$TRABAJO"
cp -r "$AQUI/repo" "$TRABAJO/repo"
FS="$TRABAJO/repo"
cd "$FS"

echo "== 1) Qué trae el repositorio =="
ls skills
echo

echo "== 2) El caso de ejemplo: los números del negocio, en un JSON =="
sed -n '1,20p' skills/founder-cfo/example.json
echo "-- el cálculo --"
python3 -B skills/founder-cfo/unit_economics.py skills/founder-cfo/example.json | sed -n '1,24p'
echo

echo "== 3) El año uno mes a mes y la tabla de escenarios =="
python3 -B skills/founder-cfo/unit_economics.py skills/founder-cfo/example.json | sed -n '26,58p'
echo

echo "== 4) Mis números (otro negocio, mismos cálculos) =="
mkdir -p founder
cp "$AQUI/datos/mi_negocio.json" founder/numbers.json
cat founder/numbers.json
echo "-- el informe que escribe en disco --"
python3 -B skills/founder-cfo/unit_economics.py founder/numbers.json --out founder/cfo.md
sed -n '13,22p' founder/cfo.md
echo "-- y el veredicto del plan --"
python3 -B skills/founder-plan/compile.py --check || echo "codigo de salida: $?"
ls -l founder
echo

echo "== 5) El precio: 40 respuestas de clientes (SINTÉTICAS, ver README) =="
head -3 "$AQUI/datos/pricing.csv"
python3 -B skills/founder-pricing/van_westendorp.py "$AQUI/datos/pricing.csv" --price 5.20 --out founder/pricing.md
sed -n '3,12p' founder/pricing.md
echo

echo "== 6) El panel de compradores (reparte fichas; NO las contesta) =="
python3 -B skills/founder-consumer/panel.py init \
  --customer skills/founder-consumer/customer.example.json \
  --pitch skills/founder-consumer/pitch.example.md \
  --n 100 --seed 7
python3 -B skills/founder-consumer/panel.py status
echo

echo "== 7) El plan compilado =="
python3 -B skills/founder-plan/compile.py --check || echo "codigo de salida: $?"
ls -l founder
echo

echo "== Fin: los tres informes están en founder/ (cfo.md, pricing.md y el plan) =="
