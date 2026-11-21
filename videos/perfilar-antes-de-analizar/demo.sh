#!/usr/bin/env bash
# Demo del vídeo «Mira qué esconde tu Excel antes de analizarlo con ydata-profiling» — @lytohlgIA
# Reglas: rutas RELATIVAS, sin claves, sin red. Todo lo que se ve se ejecuta de verdad.
set -e

echo "───────────────────────────────────────────────"
echo "1) EL FICHERO QUE TE HAN MANDADO"
echo "───────────────────────────────────────────────"
python datos/generar_datos.py
echo
ls -lh datos/ventas_2026.csv
wc -l datos/ventas_2026.csv
head -4 datos/ventas_2026.csv
echo

echo "───────────────────────────────────────────────"
echo "2) UN VISTAZO CON PANDAS: FORMA Y TIPOS"
echo "───────────────────────────────────────────────"
python explorar.py datos/ventas_2026.csv
echo

echo "───────────────────────────────────────────────"
echo "3) EL PERFIL: UN COMANDO, UN INFORME"
echo "───────────────────────────────────────────────"
python perfilar.py datos/ventas_2026.csv
ls -lh perfil.html perfil.json
echo

echo "───────────────────────────────────────────────"
echo "4) LAS ALERTAS, TAL COMO LAS ESCRIBE EL INFORME"
echo "───────────────────────────────────────────────"
python alertas.py perfil.json
echo

echo "───────────────────────────────────────────────"
echo "5) LA FICHA DE UNA COLUMNA: importe"
echo "───────────────────────────────────────────────"
python ficha.py perfil.json importe
echo

echo "───────────────────────────────────────────────"
echo "5b) LA MISMA FICHA EN DOS COLUMNAS DE TEXTO"
echo "───────────────────────────────────────────────"
python ficha.py perfil.json canal
echo
python ficha.py perfil.json fecha
echo

echo "───────────────────────────────────────────────"
echo "5c) LA FECHA: TRES FORMATOS, DOS LECTURAS POSIBLES"
echo "───────────────────────────────────────────────"
python fechas.py datos/ventas_2026.csv
echo

echo "───────────────────────────────────────────────"
echo "6) SOLO LAS COLUMNAS CON HUECOS, FILTRANDO EL JSON"
echo "───────────────────────────────────────────────"
jq -r '.variables | to_entries[] | select(.value.n_missing > 0) | "\(.key): \(.value.n_missing) huecos"' perfil.json
echo

echo "───────────────────────────────────────────────"
echo "7) EL CÍRCULO CERRADO: LO QUE METÍ CONTRA LO QUE ENCONTRÓ"
echo "───────────────────────────────────────────────"
python comparar.py perfil.json
echo

echo "───────────────────────────────────────────────"
echo "8) MODO MÍNIMO: MENOS PREGUNTAS, MENOS TIEMPO"
echo "───────────────────────────────────────────────"
python perfilar.py datos/ventas_2026.csv --minimo
ls -lh perfil_min.html
echo

echo "fin de la demo"
