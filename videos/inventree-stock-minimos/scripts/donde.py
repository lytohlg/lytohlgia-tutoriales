#!/usr/bin/env python3
"""¿Dónde está una pieza? Cada unidad de stock tiene ubicación y lote.

Uso: python3 donde.py ESP32-WROOM
"""
import json
import os
import sys
import urllib.request

BASE = os.environ.get("INVENTREE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.environ["INVENTREE_TOKEN"]
IPN = sys.argv[1] if len(sys.argv) > 1 else "ESP32-WROOM"


def api(path):
    p = urllib.request.Request(BASE + path, headers={"Authorization": "Token " + TOKEN})
    with urllib.request.urlopen(p, timeout=30) as r:
        return json.loads(r.read().decode())


piezas = api(f"/api/part/?IPN={IPN}")
if not piezas:
    raise SystemExit(f"No encuentro la referencia {IPN}")
pieza = piezas[0]
pk = pieza["pk"]

# el árbol de ubicaciones: pk -> "Almacén / Cajón B"
sitios = {u["pk"]: u.get("pathstring") or u["name"] for u in api("/api/stock/location/")}

unidades = api(f"/api/stock/?part={pk}&in_stock=true")
print(f"{pieza['IPN']} · {pieza['name']}")
print(f"mínimo en almacén: {float(pieza['minimum_stock']):.0f}  ·  disponible: {float(pieza['in_stock']):.0f}")
print()
print(f"{'CANTIDAD':>9}  {'UBICACIÓN':<32}{'LOTE':<14}ESTADO")
print("-" * 70)
for u in unidades:
    sitio = sitios.get(u.get("location"), "(sin ubicación)")
    print(f"{float(u['quantity']):>9.0f}  {sitio:<32}{u.get('batch') or '-':<14}{u.get('status_text') or u.get('status')}")
print("-" * 70)
print(f"{len(unidades)} unidad(es) de stock localizadas")
