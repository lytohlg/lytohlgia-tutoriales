#!/usr/bin/env bash
# Demo del vídeo «Automatizacion por umbral con Home Assistant: aviso cuando el salon pasa de 30 grados» — @lytohlgIA
# Reglas: rutas RELATIVAS, nada hardcodeado, ningún dato personal.
#
# Qué hace, en el mismo orden que en el vídeo:
#   1) valida la configuración ANTES de arrancar (el error se caza en dos segundos)
#   2) arranca el motor de automatizaciones
#   3) pone el salón a 25 grados  -> no debe dispararse nada
#   4) lo pone a 34 grados        -> la regla entra UNA vez y deja rastro en el registro
set -euo pipefail

CFG=/tmp/casa
ROTO=/tmp/casa_roto
LOG=/tmp/ha.log

rm -rf "$CFG" "$ROTO"
mkdir -p "$CFG" "$ROTO"
cp config/configuration.yaml "$CFG/"
cp config/roto/configuration.yaml "$ROTO/"
echo 22.0 > "$CFG/temp.txt"

echo "== 0) Un error de indentación, cazado antes de arrancar =="
hass --script check_config -c "$ROTO" 2>&1 | tail -4 || true

echo
echo "== 1) ¿La configuración es válida? =="
hass --script check_config -c "$CFG"
echo "codigo de salida: $?"

echo
echo "== 2) Arrancamos el motor =="
hass -c "$CFG" > "$LOG" 2>&1 &
HA_PID=$!
for _ in $(seq 1 90); do
  if grep -q "Home Assistant initialized" "$LOG" 2>/dev/null; then break; fi
  sleep 1
done
grep "Home Assistant initialized" "$LOG" | tail -1
echo "temperatura del salon ahora: $(cat "$CFG/temp.txt") grados"

echo
echo "== 3) 25 grados: no debe pasar nada =="
echo 25.0 > "$CFG/temp.txt"
sleep 14
echo "avisos hasta ahora: $(grep -c AVISO "$LOG" || true)"

echo
echo "== 4) 34 grados: la regla debe dispararse =="
echo 34.0 > "$CFG/temp.txt"
for _ in $(seq 1 40); do
  if grep -q AVISO "$LOG" 2>/dev/null; then break; fi
  sleep 1
done
grep AVISO "$LOG" | tail -1

echo
echo "== 5) Lo que quedó escrito en el registro de avisos =="
cat "$CFG/eventos.log"

kill "$HA_PID" 2>/dev/null || true
wait "$HA_PID" 2>/dev/null || true
echo
echo "✔ Demo terminada."
