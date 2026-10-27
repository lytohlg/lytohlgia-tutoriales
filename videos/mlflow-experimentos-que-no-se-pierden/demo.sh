#!/usr/bin/env bash
# Demo del material — @lytohlgIA
# ---------------------------------------------------------------------------
# Problema: probaste tres configuraciones del modelo, la tabla se pierde y ya
# no sabes cuál de las tres era la que daba el error bueno.
#
# Lo que hace esta demo, en orden y sin intervención:
#   1. entrena tres modelos (Ridge con alpha 0.1, 1.0 y 10.0) y registra cada
#      prueba con sus parámetros, su error y el modelo guardado;
#   2. compara las tres pruebas y dice cuál ganó;
#   3. recupera EL modelo ganador por su etiqueta y predice cuatro casos;
#   4. le pone nombre al ganador (registro de modelos) y muestra su versión;
#   5. filtra las pruebas por parámetro, que es lo que hace falta con 50.
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
rm -rf mlflow.db mlartifacts

echo "=== 1. tres pruebas, cada una registrada ==="
python scripts/entrenar.py

echo
echo "=== 2. comparar: ¿cuál falló menos? ==="
python scripts/comparar.py

echo
echo "=== 3. recuperar el modelo ganador y predecir ==="
python scripts/recuperar.py

echo
echo "=== 4. registro de modelos: nombre y versión ==="
python scripts/registro.py

echo
echo "=== 5. filtrar pruebas por parámetro ==="
python scripts/filtrar.py

echo
echo "VERIFICADO: 3 pruebas registradas · ganadora ridge-alpha-0.1 · rmse 53.010 · modelo recuperado y registrado como version 1"
