#!/usr/bin/env python3
"""Parte de reposición: genera un CSV con lo que falta, listo para pedir al proveedor.

Uso: python3 lista_compra.py
"""
import csv
import json
import os
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("INVENTREE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.environ["INVENTREE_TOKEN"]
SALIDA = os.environ.get("SALIDA", "salida")


def api(path):
    p = urllib.request.Request(BASE + path, headers={"Authorization": "Token " + TOKEN})
    with urllib.request.urlopen(p, timeout=30) as r:
        return json.loads(r.read().decode())


bajo = api("/api/part/?low_stock=true")
os.makedirs(SALIDA, exist_ok=True)
ruta = os.path.join(SALIDA, "lista_compra.csv")

filas = []
for p in sorted(bajo, key=lambda x: x["IPN"]):
    disponible = float(p.get("in_stock") or 0)
    minimo = float(p.get("minimum_stock") or 0)
    filas.append({
        "referencia": p["IPN"],
        "pieza": p["name"],
        "disponible": int(disponible),
        "minimo": int(minimo),
        "pedir": int(max(0.0, minimo - disponible)),
    })

with open(ruta, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["referencia", "pieza", "disponible", "minimo", "pedir"])
    w.writeheader()
    w.writerows(filas)

sello = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
print(f"parte de reposición · {sello}")
for f in filas:
    print(f"  {f['referencia']:<12} pedir {f['pedir']:>4}  (hay {f['disponible']}, mínimo {f['minimo']})")
print(f"\n{len(filas)} referencias · guardado en {ruta}")
