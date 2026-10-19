#!/usr/bin/env python3
"""Estado del almacén: ¿qué hay dentro de InvenTree? (por su API, sin abrir el navegador)"""
import json
import os
import urllib.request

BASE = os.environ.get("INVENTREE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.environ["INVENTREE_TOKEN"]


def api(path):
    p = urllib.request.Request(BASE + path, headers={"Authorization": "Token " + TOKEN})
    with urllib.request.urlopen(p, timeout=30) as r:
        return json.loads(r.read().decode())


info = api("/api/")
piezas = api("/api/part/")
ubicaciones = api("/api/stock/location/")
unidades = api("/api/stock/")

print(f"InvenTree {info['version']}  ·  API v{info['apiVersion']}")
print(f"piezas en catálogo : {len(piezas)}")
print(f"ubicaciones        : {len(ubicaciones)}")
print(f"unidades de stock  : {len(unidades)}")

# ¿cuántas piezas hay físicamente? la suma de las cantidades de cada unidad
total = sum(float(u["quantity"]) for u in unidades)
print(f"piezas contadas    : {total:.0f}")

print("\nmapa del almacén:")
for u in sorted(ubicaciones, key=lambda x: x.get("pathstring") or ""):
    n = sum(1 for s in unidades if s.get("location") == u["pk"])
    print(f"  {u.get('pathstring') or u['name']:<28} {n} unidad(es) de stock")
