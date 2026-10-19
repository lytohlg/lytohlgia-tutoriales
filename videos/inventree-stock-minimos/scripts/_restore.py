#!/usr/bin/env python3
"""Restaura la base de datos de la demo desde una copia (antes de arrancar el servidor).

Uso: python3 scripts/_restore.py _snap/00_inicial.sqlite3
"""
import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
origen = sys.argv[1] if len(sys.argv) > 1 else "_snap/00_inicial.sqlite3"
if not os.path.isabs(origen):
    origen = os.path.join(BASE, origen)
destino = os.path.join(BASE, "database.sqlite3")
for extra in ("-wal", "-shm"):
    if os.path.exists(destino + extra):
        os.remove(destino + extra)
shutil.copyfile(origen, destino)
print("base restaurada:", os.path.basename(origen))
