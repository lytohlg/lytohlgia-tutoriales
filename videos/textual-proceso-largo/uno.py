"""Procesa UN fichero y deja que el error salga entero, sin adornos.

Uso: python3 uno.py lote/extracto_041.csv
"""
import sys
import traceback
from pathlib import Path

import procesar

ruta = Path(sys.argv[1])
try:
    print(procesar.procesar(ruta))
except Exception:
    traceback.print_exc()
    sys.exit(1)          # el fichero no se procesó: el proceso termina en fallo
