#!/usr/bin/env python3
"""Siembra el almacén de ejemplo en una instancia de InvenTree, por su API REST.

Crea: categorías, piezas con su mínimo, ubicaciones físicas y unidades de stock.
Idempotente: si una pieza ya existe (por IPN), no la vuelve a crear.

Variables de entorno:
    INVENTREE_URL    (por defecto http://127.0.0.1:8000)
    INVENTREE_TOKEN  token de API del usuario
"""
import json
import os
import urllib.error
import urllib.request

BASE = os.environ.get("INVENTREE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.environ["INVENTREE_TOKEN"]


def api(path, data=None, method=None):
    hdr = {"Authorization": "Token " + TOKEN}
    cuerpo = None
    if data is not None:
        cuerpo = json.dumps(data).encode()
        hdr["Content-Type"] = "application/json"
    peticion = urllib.request.Request(BASE + "/" + path.lstrip("/"), data=cuerpo, headers=hdr,
                                      method=method or ("POST" if cuerpo else "GET"))
    try:
        with urllib.request.urlopen(peticion, timeout=30) as r:
            texto = r.read().decode()
            return r.status, (json.loads(texto) if texto.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


def uno(ruta, filtro):
    """Devuelve el primer resultado que cumpla el filtro (o None)."""
    s, b = api(ruta)
    if s != 200 or not isinstance(b, list):
        return None
    for x in b:
        if all(str(x.get(k)) == str(v) for k, v in filtro.items()):
            return x
    return None


def crear(ruta, datos, clave, valor):
    existe = uno(ruta, {clave: valor})
    if existe:
        return existe["pk"]
    s, b = api(ruta, datos)
    if s not in (200, 201):
        raise SystemExit(f"KO {ruta} {datos.get('name')}: {s} {b}")
    # api/stock/ es un endpoint masivo: responde con la lista de objetos creados
    if isinstance(b, list):
        return b[0]["pk"]
    return b["pk"]


# ── categorías ────────────────────────────────────────────────────────────────
cat_pasivos = crear("/api/part/category/", {"name": "Pasivos", "description": "Resistencias y condensadores"}, "name", "Pasivos")
cat_chips = crear("/api/part/category/", {"name": "Semiconductores", "description": "Módulos y circuitos integrados"}, "name", "Semiconductores")
cat_conect = crear("/api/part/category/", {"name": "Conectores y cable", "description": "Cableado y conectores"}, "name", "Conectores y cable")

# ── piezas (con mínimo de stock) ──────────────────────────────────────────────
PIEZAS = [
    # IPN, nombre, categoría, mínimo
    ("RES-10K", "Resistencia 10k 1/4W", cat_pasivos, 200),
    ("COND-470", "Condensador electrolítico 470uF 16V", cat_pasivos, 50),
    ("ESP32-WROOM", "Módulo ESP32-WROOM-32", cat_chips, 10),
    ("LM2596", "Regulador LM2596 (step-down)", cat_chips, 15),
    ("JST-XH4", "Conector JST-XH de 4 pines", cat_conect, 100),
    ("USB-C-1M", "Cable USB-C de 1 metro", cat_conect, 5),
]
ids_pieza = {}
for ipn, nombre, cat, minimo in PIEZAS:
    ids_pieza[ipn] = crear("/api/part/", {
        "IPN": ipn, "name": nombre, "category": cat, "minimum_stock": minimo,
        "component": True, "purchaseable": True,
        "description": f"{nombre} · mínimo {minimo} en almacén",
    }, "IPN", ipn)

# ── ubicaciones físicas (el árbol del almacén) ────────────────────────────────
raiz = crear("/api/stock/location/", {"name": "Almacén", "description": "Almacén central"}, "name", "Almacén")
cajon_a = crear("/api/stock/location/", {"name": "Cajón A", "description": "Pasivos", "parent": raiz}, "name", "Cajón A")
cajon_b = crear("/api/stock/location/", {"name": "Cajón B", "description": "Semiconductores", "parent": raiz}, "name", "Cajón B")
estante = crear("/api/stock/location/", {"name": "Estante 2", "description": "Cableado", "parent": raiz}, "name", "Estante 2")
taller = crear("/api/stock/location/", {"name": "Taller", "description": "Banco de trabajo", "parent": raiz}, "name", "Taller")

# ── unidades de stock: cantidad, ubicación y lote ────────────────────────────
STOCK = [
    # IPN, ubicación, cantidad, lote
    ("RES-10K", cajon_a, 640, "L-2026-03"),
    ("COND-470", cajon_a, 38, "L-2026-01"),
    ("ESP32-WROOM", cajon_b, 11, "L-2026-05"),
    ("LM2596", cajon_b, 22, "L-2026-02"),
    ("JST-XH4", cajon_a, 85, "L-2026-04"),
    ("USB-C-1M", estante, 3, "L-2025-11"),
]
ids_stock = []
for ipn, loc, cant, lote in STOCK:
    ids_stock.append(crear("/api/stock/", {
        "part": ids_pieza[ipn], "location": loc, "quantity": cant, "batch": lote,
        "notes": f"Recepción lote {lote}",
    }, "batch", lote))

# ── un movimiento real: el técnico se lleva 4 ESP32 al taller ────────────────
s, b = api("api/stock/%s/transfer/" % ids_stock[2],
           {"location": taller, "quantity": 4, "notes": "Montaje del equipo del cliente"} , method="POST")
if s not in (200, 201):
    # variante: el endpoint puede exigir lista de items
    s, b = api("/api/stock/transfer/", {"items": [{"pk": ids_stock[2], "quantity": 4}],
                                       "location": taller, "notes": "Montaje del equipo del cliente"},
               method="POST")

print("piezas:", len(ids_pieza), "· ubicaciones: 5 · unidades:", len(ids_stock))
print("movimiento al taller:", s, str(b)[:120] if s not in (200, 201) else "OK")
