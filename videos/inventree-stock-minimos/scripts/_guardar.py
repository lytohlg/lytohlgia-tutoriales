#!/usr/bin/env python3
"""Guarda una copia consistente de la base de la demo (incluye lo que esté en el WAL).

Uso:
    python3 scripts/_guardar.py _snap/00_inicial.sqlite3

Se usa para dos cosas: dejar la copia del almacén recién sembrado (00_inicial) y la del
estado justo después del consumo del técnico (10_tras_consumo). `_restore.py` hace lo
contrario: devuelve la base de trabajo a una de esas copias.
"""
import os
import sqlite3
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destino = sys.argv[1] if len(sys.argv) > 1 else "_snap/00_inicial.sqlite3"
if not os.path.isabs(destino):
    destino = os.path.join(BASE, destino)
os.makedirs(os.path.dirname(destino), exist_ok=True)

origen = sqlite3.connect(os.path.join(BASE, "database.sqlite3"))
copia = sqlite3.connect(destino)
with copia:
    origen.backup(copia)
copia.close()
origen.close()
print("copia hecha:", os.path.relpath(destino, BASE), os.path.getsize(destino), "bytes")
