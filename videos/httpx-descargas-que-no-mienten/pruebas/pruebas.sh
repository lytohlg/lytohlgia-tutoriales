#!/usr/bin/env bash
# Prueba real de este material — @lytohlgIA
# ---------------------------------------------------------------------------
# Es exactamente la prueba que se hizo ANTES de publicar el vídeo:
#   1) construye el entorno que describe entorno/Dockerfile
#   2) ejecuta la demo dentro de un contenedor limpio, sin privilegios, con la
#      carpeta montada en SOLO LECTURA (el script no puede tocar el original)
#      y una copia de trabajo en /tmp
# Si esto termina sin errores, tu copia funciona.
# ---------------------------------------------------------------------------
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGEN="repro-httpx-descargas-que-no-mienten:local"

echo "[1/2] Construyendo el entorno desde entorno/Dockerfile ..."
docker build -q -t "$IMAGEN" "$AQUI/entorno"

echo "[2/2] Ejecutando la demo en un contenedor limpio ..."
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$AQUI:/trabajo:ro" "$IMAGEN" \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'

echo
echo "✔ Prueba terminada sin errores."

# Comprobaciones sobre el resultado: lo que el vídeo afirma, medido aquí.
python3 - <<'PY'
import json, pathlib, sys
base = pathlib.Path('/tmp/repro/scripts')
trunc = base / 'descargas_viejo/informe-truncado.csv'
bien = base / 'descargas/informe.csv'
datos = trunc.read_bytes()
assert len(datos) == 1200, f'truncado: {len(datos)} bytes (se esperaban 1200)'
assert datos.count(b'\n') == 40, f'truncado: {datos.count(chr(10).encode())} saltos'
assert not datos.endswith(b'\n'), 'el truncado NO deberia acabar en salto de linea'
assert len(bien.read_text().splitlines()) == 201, 'informe completo: se esperaban 201 lineas'
inf = json.loads((base / 'informe_descarga.json').read_text())
assert all(f['estado'] != 'valido' for f in inf if 'truncado' in f['ruta']), 'el truncado no puede archivarse'
print(f'OK: 1200 bytes / 40 lineas truncadas, {len(bien.read_text().splitlines())} lineas completas, '
      f'{sum(1 for f in inf if f["estado"] == "valido")} de {len(inf)} validos')
PY
