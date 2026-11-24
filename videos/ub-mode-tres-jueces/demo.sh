#!/usr/bin/env bash
# Demo del vídeo «Puse a prueba ub-mode de Uncle Bob con código feo» — @lytohlgIA
# Reglas: rutas RELATIVAS, sin claves, sin red. Todo lo que se ve se ejecuta de verdad.
set -e

echo "───────────────────────────────────────────────"
echo "1) EL MÓDULO FEO: 17 CAMINOS Y DOS COPIAS"
echo "───────────────────────────────────────────────"
wc -l src/pedidos.py
sed -n '1,12p' src/pedidos.py
echo
echo "   las dos funciones de envío, calcadas:"
sed -n '54,58p;71,75p' src/pedidos.py
echo

echo "───────────────────────────────────────────────"
echo "2) LOS TRES TESTS: PASAN EN VERDE"
echo "───────────────────────────────────────────────"
python -m pytest tests -q
echo

echo "───────────────────────────────────────────────"
echo "3) JUEZ 1: CRAP SIN COBERTURA ENLAZADA"
echo "   (busca tests con unittest, no los encuentra)"
echo "───────────────────────────────────────────────"
python -m crapper --root . --source-root src
echo

echo "───────────────────────────────────────────────"
echo "4) LA COBERTURA REAL, EN EL FORMATO QUE ÉL LEE"
echo "───────────────────────────────────────────────"
rm -rf target/coverage .coverage
python -m coverage run --source=src -m pytest tests -q
python -m coverage lcov -o target/coverage/python/lcov.info
python -m coverage report
echo
echo "   notarás que coverage y crapper no dan el mismo %: cuentan cosas distintas"
echo

echo "───────────────────────────────────────────────"
echo "5) JUEZ 1 OTRA VEZ: CRAP CON LA COBERTURA ENLAZADA"
echo "───────────────────────────────────────────────"
python -m crapper --root . --source-root src --use-existing-coverage
echo

echo "───────────────────────────────────────────────"
echo "6) LA FÓRMULA, A MANO"
echo "───────────────────────────────────────────────"
echo "   CRAP = CC^2 * (1-cov)^3 + CC"
python -c "cc=17; c=0.389; print(f'   {cc}^2 * (1-{c})^3 + {cc} = {cc**2*(1-c)**3+cc:.1f}')"
python -c "cc=17; print(f'   con cobertura 1.0: {cc}^2 * 0 + {cc} = {cc}')"
echo

echo "───────────────────────────────────────────────"
echo "7) JUEZ 2: DUPLICACIÓN ESTRUCTURAL"
echo "───────────────────────────────────────────────"
python -m dryer --root . --source-root src
echo

echo "───────────────────────────────────────────────"
echo "8) JUEZ 3: ¿DÓNDE PUEDE INYECTAR UN FALLO?"
echo "───────────────────────────────────────────────"
python -m mutator --root . --source-root src --scan
echo

echo "───────────────────────────────────────────────"
echo "9) JUEZ 3 EJECUTANDO: ¿MIS TESTS LO NOTAN?"
echo "───────────────────────────────────────────────"
set +e
python -m mutator --root . --source-root src --use-existing-coverage \
  --mutate-all --test-command "python -m pytest tests -q"
echo "   código de salida de mutator: $?"
set -e
echo

echo "───────────────────────────────────────────────"
echo "10) EL GATE: LOS TRES JUNTOS, UN VEREDICTO"
echo "───────────────────────────────────────────────"
set +e
python gate.py
echo "   código de salida de gate.py: $?"
set -e
echo

echo "───────────────────────────────────────────────"
echo "11) LA COBERTURA NO BAJA LA COMPLEJIDAD"
echo "───────────────────────────────────────────────"
echo "   con 38.9% de cobertura el CRAP es 83.0; con el 100% sería 17.0"
echo "   la cobertura deja de esconder la complejidad, no la reduce"
echo
echo "fin de la demo"
