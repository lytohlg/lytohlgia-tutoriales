#!/usr/bin/env bash
# Demo del vídeo «Tu IA no puede navegar: 6 llamadas de Claude Quickstarts, una por una» — @lytohlgIA
# Son los mismos comandos del vídeo, en el mismo orden, con rutas relativas.
set -euo pipefail

# Dentro de un contenedor sin namespaces de usuario, Chromium no puede montar su
# sandbox y solo arranca con --no-sandbox. El driver lo añade solo si eres root;
# si no lo eres, le damos este lanzador por CHROME_PATH (ver el propio fichero).
if [ "$(id -u)" -ne 0 ]; then
  export CHROME_PATH="$PWD/chromium-sin-sandbox.sh"
fi

echo "== 1) Las 6 llamadas del ejercicio oficial (sin clave, sin modelo) =="
python3 exercise.py

echo
echo "== 2) Lo mismo contra mi pagina, que tiene un formulario =="
python3 mipagina.py

echo
echo "== 3) Una herramienta que el driver NO implementa =="
python3 fuera_del_driver.py

echo
echo "== 4) Con modelo hace falta una clave: esto es lo que pasa sin ella =="
( python3 run.py "Abre la pagina y dime el titular" 2>&1 || true ) | tail -3

echo
echo "== Listo: 6 llamadas, 4 respondidas y 2 rechazadas =="
echo "== (y el bucle con modelo, que necesita clave: eso es run.py) =="
