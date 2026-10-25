#!/usr/bin/env bash
# Demo del vídeo «httpx: descargas que no te mienten» — @lytohlgIA
# El "proveedor" es un servidor de pruebas local (scripts/servidor.py) que imita los
# cuatro casos que se ven en un proveedor real: correcto, truncado, 503 pasajero y lento.
# No hay ninguna credencial: se ejecuta entero dentro de esta carpeta.
set -uo pipefail
cd "$(dirname "$0")/scripts"

echo "== 1) La descarga de siempre: urllib, sin comprobar nada =="
python3 -u descarga_ingenua.py --servidor-local --timeout 8

echo
echo "== 2) Lo que ha dejado en disco =="
ls -l descargas_viejo/
wc -l descargas_viejo/*.csv

echo
echo "== 3) La última línea del informe truncado (no acaba en salto de línea) =="
tail -c 45 descargas_viejo/informe-truncado.csv | od -c | tail -2

echo
echo "== 4) La misma descarga con httpx: timeout, reintentos, tamaño y cabecera =="
python3 -u descarga_httpx.py --servidor-local

echo
echo "== 5) El informe que deja la versión que sí comprueba =="
cat informe_descarga.json

echo
echo "== 6) Los bytes que se han archivado (solo lo completo) =="
wc -l descargas/*.csv

echo
echo "== 7) El informe repetido: la huella sha256 del contenido =="
python3 comprobar_huella.py descargas/informe.csv
python3 comprobar_huella.py descargas/informe.csv

echo
python3 - <<'PY'
import json
inf = json.load(open('informe_descarga.json'))
por_ruta = {f['ruta']: f['estado'] for f in inf}
ok = sum(1 for f in inf if f['estado'] == 'ok')
print(f"VERIFICADO: {ok} de {len(inf)} informes completos archivados | "
      f"truncado={por_ruta.get('/informe-truncado')} lento={por_ruta.get('/informe-lento')} "
      f"503={por_ruta.get('/informe-503')}")
PY
