#!/usr/bin/env bash
# Demo del vídeo «ha-mcp: tu IA controla tu casa sin integraciones a mano» — @lytohlgIA
#
# Es EXACTAMENTE lo que se ve en pantalla, en el mismo orden: cada bloque es una
# escena del vídeo. Rutas relativas, ningún valor hardcodeado: el token sale del
# entorno o de .env (ver .env.example) y, si no hay ninguno, del servidor de demo
# público del propio proyecto (su token está publicado en su repo).
set -uo pipefail

cd "$(dirname "$0")"

# 0) Entorno: deja un .env utilizable (variables de entorno > .env > demo público)
python3 preparar_entorno.py

echo
echo "################ 1) EL ANTES: la API a pelo ################"
bash escenas/e1_dolor.sh

echo
echo "################ 2) LA PRUEBA: encender y verificar ################"
python3 escenas/e2_prueba.py

echo
echo "################ 3) LAS HERRAMIENTAS: tools/list ################"
python3 escenas/e3_herramientas.py

echo
echo "################ 4) EL DETALLE: JSON-RPC ################"
python3 escenas/e4_detalle.py

echo
echo "################ 5) PREGUNTAR: overview y plantillas ################"
python3 escenas/e5_consultar.py

echo
echo "################ 6) LA CONFIGURACIÓN DEL CLIENTE ################"
python3 escenas/e6_config.py
