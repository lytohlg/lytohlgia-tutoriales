#!/usr/bin/env python3
"""¿Qué hay que reponer? Pregunta a InvenTree qué piezas están por debajo de su mínimo.

Usa el filtro nativo de la API: GET api/part/?low_stock=true
"""
import json
import os
import urllib.request

BASE = os.environ.get("INVENTREE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.environ["INVENTREE_TOKEN"]


def api(path):
    p = urllib.request.Request(BASE + "/" + path.lstrip("/"),
                               headers={"Authorization": "Token " + TOKEN})
    with urllib.request.urlopen(p, timeout=30) as r:
        return json.loads(r.read().decode())


bajo = api("api/part/?low_stock=true")

print(f"{'REFERENCIA':<12}{'DISPONIBLE':>11}{'MÍNIMO':>8}{'FALTAN':>8}  PIEZA")
print("-" * 68)
for p in sorted(bajo, key=lambda x: x["IPN"]):
    disponible = float(p.get("in_stock") or 0)
    minimo = float(p.get("minimum_stock") or 0)
    falta = max(0.0, minimo - disponible)
    print(f"{p['IPN']:<12}{disponible:>11.0f}{minimo:>8.0f}{falta:>8.0f}  {p['name']}")

print("-" * 68)
print(f"{len(bajo)} referencia(s) por debajo del mínimo")
