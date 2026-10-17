#!/usr/bin/env python3
"""Paso 1 — el entorno de la demo.

Ensena (y comprueba) lo que hay montado: Python, Django y SQL Explorer como app
de Django, y las tablas de la propia herramienta creadas con `migrate`.
No hay librería de consola: SQL Explorer se instala dentro de un proyecto Django.
"""
import platform
from contextlib import redirect_stdout
from importlib.metadata import version
from io import StringIO

from arranque import RAIZ, preparar_django

preparar_django()

import django                                                    # noqa: E402
from django.core.management import call_command                  # noqa: E402

# Las tablas de la herramienta (consultas guardadas, histórico...) se crean con
# migrate, igual que en cualquier proyecto Django. La salida larga no interesa aquí.
with redirect_stdout(StringIO()):
    call_command("migrate", verbosity=0, interactive=False)

import sqlite3                                                    # noqa: E402

con = sqlite3.connect(RAIZ / "explorer.db")
tablas = [f[0] for f in con.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
con.close()

print("entorno de la demo")
for etiqueta, valor in (
    ("python", platform.python_version()),
    ("django", django.get_version()),
    ("sql explorer", f"django-sql-explorer {version('django-sql-explorer')}  (app de django)"),
    ("base de la app", f"explorer.db   ({len(tablas)} tablas de la herramienta)"),
    ("datos del negocio", "empresa.db    (la siembra los crea en el paso 2)"),
):
    print(f"  {etiqueta:<18}{valor}")
