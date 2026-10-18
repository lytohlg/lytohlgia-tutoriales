#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Muestra con qué versiones se hizo la prueba: es lo primero que se enseña en el vídeo."""
import importlib.metadata as md
import os
import platform
import subprocess
import sys

# (etiqueta ya alineada, módulo a importar, nombre de la distribución en pip)
FILAS = [
    ('paddleocr:    ', 'paddleocr', 'paddleocr'),
    ('paddlepaddle: ', 'paddle', 'paddlepaddle'),
    ('pypdfium2:    ', 'pypdfium2', 'pypdfium2'),
]


def version(modulo, dist):
    """Primero el __version__ del módulo; si no lo tiene, el de la distribución instalada."""
    try:
        mod = __import__(modulo)
        v = getattr(mod, '__version__', None)
        if v:
            return v
    except Exception:                                      # noqa: BLE001
        pass
    try:
        return md.version(dist)
    except Exception as e:                                 # noqa: BLE001
        return f'no instalado ({e.__class__.__name__})'


print('== Entorno de la prueba ==')
print(f'Python:       {platform.python_version()}')
for etiqueta, modulo, dist in FILAS:
    print(f'{etiqueta}{version(modulo, dist)}')
try:
    v = subprocess.run(['pdftotext', '-v'], capture_output=True, text=True)
    print('pdftotext:    ' + (v.stderr.strip().splitlines() or ['no disponible'])[0])
except FileNotFoundError:
    print('pdftotext:    no disponible')
print(f'arquitectura: {platform.machine()}  CPUs: {os.cpu_count()}')
sys.exit(0)
