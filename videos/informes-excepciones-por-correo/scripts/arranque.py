#!/usr/bin/env python3
"""Arranque común de los scripts de la demo.

Prepara el proyecto Django (el de `proyecto/`) para poder importar la app SQL
Explorer desde un script suelto, sin repetir estas cuatro líneas en cada uno.
"""
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]     # la carpeta de la demo (donde está demo.sh)
PROYECTO = RAIZ / "proyecto"

DESTINO_INFORME = "operaciones@example.com"


def preparar_django():
    """Deja Django listo y devuelve la carpeta de la demo (para rutas relativas)."""
    sys.path.insert(0, str(PROYECTO))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informes.settings")
    os.chdir(RAIZ)

    import django

    django.setup()
    return RAIZ
