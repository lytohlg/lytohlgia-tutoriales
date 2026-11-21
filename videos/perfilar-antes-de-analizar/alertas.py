#!/usr/bin/env python3
"""Imprime las alertas del perfil, tal como las escribe el propio informe.

No reescribe ni resume nada: cada línea es un elemento del bloque `alerts`
del resumen JSON. Si el informe no marca nada, aquí no sale nada.
"""
import json
import sys

ruta = sys.argv[1] if len(sys.argv) > 1 else "perfil.json"
js = json.load(open(ruta, encoding="utf-8"))
alertas = js.get("alerts") or []
print(f"{len(alertas)} alerta{'s' if len(alertas) != 1 else ''}\n")
for a in alertas:
    print(f"  · {a}")
