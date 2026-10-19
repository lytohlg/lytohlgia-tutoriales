#!/usr/bin/env python3
"""¿Quién movió las piezas y cuándo? Historial de movimientos de una referencia.

Uso: python3 historial.py ESP32-WROOM
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


pieza = api(f"/api/part/?IPN={IPN}")[0]
movimientos = api(f"/api/stock/track/?part={pieza['pk']}")


def nombre_usuario(valor):
    """El campo user es el pk del usuario: se resuelve a su nombre."""
    if valor in (None, "", 0):
        return "-"
    try:
        return api(f"/api/user/{valor}/")["username"][:9]
    except Exception:
        return f"#{valor}"


print(f"historial de {pieza['IPN']} · {pieza['name']}")
print()
print(f"{'FECHA':<18}{'QUÉ PASÓ':<32}{'USUARIO':<9}NOTAS")
print("-" * 88)
for m in movimientos[-8:]:
    fecha = (m.get("date") or "")[:16]
    que = (m.get("label") or "cambio")[:31]
    notas = (m.get("notes") or "")[:32]
    print(f"{fecha:<18}{que:<32}{nombre_usuario(m.get('user')):<9}{notas}")
print("-" * 88)
print(f"{len(movimientos)} movimiento(s) registrados · cantidad actual: {float(pieza['in_stock']):.0f}")
