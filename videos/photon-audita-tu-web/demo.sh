#!/usr/bin/env bash
# Demo del vídeo «Photon: lo que tu web expone sin que lo sepas» — @lytohlgIA
# Reglas: rutas RELATIVAS, valores en variables de entorno, nada hardcodeado.
# Reproduce EXACTAMENTE la secuencia del vídeo, en el mismo orden.
set -euo pipefail

PHOTON=/opt/photon
MATERIAL=/opt/material
SITIO=/tmp/sitio
PUERTO="${PUERTO:-8765}"
SALIDA="127.0.0.1:$PUERTO"

echo "== Photon: lo que tu web expone sin que lo sepas =="
cd "$PHOTON"

echo
echo "-- 1. Generamos el sitio de prueba (datos falsos, todo local) --"
python3 "$MATERIAL/generar_sitio.py" "$SITIO"
python3 -m http.server "$PUERTO" --bind 127.0.0.1 --directory "$SITIO" >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
sleep 2
curl -s -o /dev/null -w "sitio de prueba: HTTP %{http_code}\n" "http://127.0.0.1:$PUERTO/"

echo
echo "-- 2. Primera pasada con el repo TAL COMO VIENE --"
rm -rf "$SALIDA"
python3 photon.py -u "http://127.0.0.1:$PUERTO/" -l 3 -t 10 --keys -e json || true
echo
echo "Informe obtenido (esto es lo que el tool entrega sin tocar nada):"
for f in files intel endpoints keys; do
  if [ -f "$SALIDA/$f.txt" ]; then echo "  $f.txt: $(wc -l < "$SALIDA/$f.txt") líneas"; else echo "  $f.txt: NO SE HA CREADO"; fi
done

echo
echo "-- 3. Los tres defectos de migración a Python 3 --"
python3 "$MATERIAL/aplicar_parches.py" "$PHOTON"
git diff --stat

echo
echo "-- 4. Segunda pasada, con los arreglos aplicados --"
rm -rf "$SALIDA"
python3 photon.py -u "http://127.0.0.1:$PUERTO/" -l 3 -t 10 --keys -e json

echo
echo "-- 5. El informe --"
for f in files intel endpoints keys; do
  echo "### $f.txt"
  cat "$SALIDA/$f.txt"
  echo
done

echo "-- 6. Export para automatizar --"
python3 "$MATERIAL/resumen_export.py" "$SALIDA/exported.json"

echo
echo "-- 7. Verificación del resultado (no basta con 'no dio error') --"
python3 "$MATERIAL/verificar_resultado.py" "$SALIDA"

echo
echo "== fin: mismo material, ejecutado de verdad =="
