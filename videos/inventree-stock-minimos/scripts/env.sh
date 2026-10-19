#!/bin/bash
# Variables comunes de la demo. Lo importante: TODO lo que InvenTree escribe queda dentro de la
# carpeta del paquete (o de su copia en /tmp), nunca en rutas del sistema. Los scripts del vídeo
# lo cargan con `source scripts/env.sh`; así el servidor y los clientes hablan del mismo sitio.

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Servidor de la demo
export INVENTREE_URL="${INVENTREE_URL:-http://127.0.0.1:8000}"

# Base de datos: un único fichero SQLite junto al código
export INVENTREE_DB_ENGINE=sqlite3
export INVENTREE_DB_NAME="$RAIZ/database.sqlite3"
export INVENTREE_SECRET_KEY="${INVENTREE_SECRET_KEY:-clave-local-de-pruebas-1234567890}"

# Directorios de trabajo de InvenTree, dentro de la carpeta: escribibles por cualquier usuario
export INVENTREE_DATA_DIR="$RAIZ/datos_inventree"
export INVENTREE_STATIC_ROOT="$INVENTREE_DATA_DIR/static"
export INVENTREE_MEDIA_ROOT="$INVENTREE_DATA_DIR/media"
export INVENTREE_BACKUP_DIR="$INVENTREE_DATA_DIR/backup"
export INVENTREE_PLUGIN_DIR="$INVENTREE_DATA_DIR/plugins"
export INVENTREE_PLUGIN_FILE="$INVENTREE_DATA_DIR/plugins.txt"
export INVENTREE_SECRET_KEY_FILE="$INVENTREE_DATA_DIR/secret_key.txt"
export INVENTREE_OIDC_PRIVATE_KEY_FILE="$INVENTREE_DATA_DIR/oidc.pem"
# Fichero de configuración: dentro de la carpeta. Si no se fija, InvenTree lo busca en una ruta
# del sistema que no podemos escribir y el arranque falla antes de migrar.
export INVENTREE_CONFIG_FILE="$INVENTREE_DATA_DIR/config.yaml"
mkdir -p "$INVENTREE_STATIC_ROOT" "$INVENTREE_MEDIA_ROOT" \
         "$INVENTREE_BACKUP_DIR" "$INVENTREE_PLUGIN_DIR"

# El token lo genera `scripts/_token.py` la primera vez que se prepara el almacén
if [ -f "$RAIZ/.token" ]; then
    export INVENTREE_TOKEN="$(cat "$RAIZ/.token")"
fi
