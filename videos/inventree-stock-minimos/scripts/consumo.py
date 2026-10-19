#!/usr/bin/env python3
"""El técnico gasta piezas en el cliente: descuenta stock REAL en InvenTree, no en una libreta.

Uso: python3 consumo.py ESP32-WROOM=3 JST-XH4=60
"""
import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("INVENTREE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.environ["INVENTREE_TOKEN"]


def api(path, datos=None, metodo=None):
    cabecera = {"Authorization": "Token " + TOKEN}
    cuerpo = None
    if datos is not None:
        cuerpo = json.dumps(datos).encode()
        cabecera["Content-Type"] = "application/json"
    p = urllib.request.Request(BASE + path, data=cuerpo, headers=cabecera,
                               method=metodo or ("POST" if cuerpo else "GET"))
    try:
        with urllib.request.urlopen(p, timeout=30) as r:
            texto = r.read().decode()
            return r.status, (json.loads(texto) if texto.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


pedido = [a.split("=") for a in sys.argv[1:]] or [["ESP32-WROOM", "3"]]

for ipn, cantidad in pedido:
    piezas = api(f"/api/part/?IPN={ipn}")[1]
    if not piezas:
        print(f"{ipn}: no existe")
        continue
    pieza = piezas[0]
    unidades = api(f"/api/stock/?part={pieza['pk']}&in_stock=true")[1]
    origen = next((u for u in unidades if float(u["quantity"]) >= float(cantidad)), None)
    if origen is None:
        print(f"{ipn}: no hay ninguna unidad con {cantidad} piezas")
        continue
    estado, respuesta = api("/api/stock/remove/", {
        "items": [{"pk": origen["pk"], "quantity": float(cantidad)}],
        "notes": "Consumo en el montaje del cliente 4471",
    })
    if estado in (200, 201):
        print(f"{ipn}: {cantidad} uds consumidas  (unidad {origen['pk']}, quedan "
              f"{float(origen['quantity']) - float(cantidad):.0f} en esa ubicación)")
    else:
        print(f"{ipn}: ERROR {estado} {respuesta}")

print("\nstock total después del consumo:")
for ipn, _ in pedido:
    piezas = api(f"/api/part/?IPN={ipn}")[1]
    if piezas:
        print(f"  {ipn}: {float(piezas[0]['in_stock']):.0f} disponibles")
