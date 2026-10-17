#!/usr/bin/env bash
# Demo del vídeo «SQL Explorer: el informe de excepciones te llega solo» — @lytohlgIA
# Son los 6 pasos, en el mismo orden que se ve en pantalla. Rutas RELATIVAS y sin
# claves: la base de datos es un SQLite de ejemplo y el correo va a un servidor de
# pruebas local. Este mismo fichero es el que ejecuta la prueba del paquete.
set -euo pipefail

echo "== SQL Explorer: el informe de excepciones te llega solo =="

echo
echo "-- 1. el entorno: Django + SQL Explorer, y los servidores de prueba"
python3 scripts/entorno.py
bash scripts/arrancar_servicios.sh

echo
echo "-- 2. la siembra: pedidos y facturas con datos realistas"
python3 scripts/sembrar.py

echo
echo "-- 3. la consulta de excepciones queda GUARDADA en SQL Explorer"
python3 scripts/crear_consulta.py

echo
echo "-- 4. se ejecuta la consulta guardada (con el motor de la herramienta)"
python3 scripts/ejecutar_consulta.py

echo
echo "-- 5. la alerta: el informe sale por correo y se lee el correo recibido"
python3 scripts/enviar_alerta.py
python3 scripts/leer_correo.py --informe

echo
echo "-- 6. estado: histórico de la consulta y qué pasa si vuelve a lanzarse"
python3 scripts/estado_alertas.py
