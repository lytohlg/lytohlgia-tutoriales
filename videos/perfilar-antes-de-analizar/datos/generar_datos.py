#!/usr/bin/env python3
"""Genera el fichero de ventas CON la suciedad contada de antemano.

La gracia del vídeo: el generador apunta en manifest.json exactamente qué
defectos mete (y cuántos). Después el perfilador tiene que encontrarlos sin
saber nada de este fichero. Si coinciden, la demo prueba algo.

Determinista: misma semilla, mismo fichero.
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(20261121)
AQUI = Path(__file__).resolve().parent
FILAS = 60000

# ── Defectos que vamos a meter (y luego exigiremos al perfil) ────────────────
N_IMPORTE_VACIO = 1200       # 2,0 %
N_CLIENTE_VACIO = 40
N_FECHA_VACIA = 90
N_DUPLICADOS = 300           # filas repetidas enteras
N_ABONOS = 700               # importes negativos LEGÍTIMOS (devoluciones)
FORMATOS_FECHA = ["iso", "dmy", "mdy"]
REPARTO_FECHA = [0.65, 0.25, 0.10]

CANALES = ["Web", "web", "WEB ", "Tienda", "tienda", "Teléfono"]
CLIENTES = [f"Cliente {i:04d}" for i in range(1, 901)]


def fecha_txt(d: date, formato: str) -> str:
    if formato == "iso":
        return d.isoformat()
    if formato == "dmy":
        return d.strftime("%d/%m/%Y")
    return d.strftime("%m/%d/%Y")


filas = []
inicio = date(2026, 1, 1)
for i in range(FILAS):
    d = inicio + timedelta(days=random.randint(0, 300))
    fmt = random.choices(FORMATOS_FECHA, weights=REPARTO_FECHA, k=1)[0]
    base = round(random.lognormvariate(3.4, 0.9), 2)
    filas.append({
        "pedido_id": f"P{100000 + i}",
        "fecha": fecha_txt(d, fmt),
        "cliente": random.choice(CLIENTES),
        "canal": random.choice(CANALES),
        "importe": f"{base:.2f}",
        "unidades": str(random.randint(1, 12)),
    })

# 1) Huecos: se vacían campos concretos (se cuentan por columna)
vacias_importe = set(random.sample(range(FILAS), N_IMPORTE_VACIO))
for i in vacias_importe:
    filas[i]["importe"] = ""
for i in random.sample(range(FILAS), N_CLIENTE_VACIO):
    filas[i]["cliente"] = ""
for i in random.sample(range(FILAS), N_FECHA_VACIA):
    filas[i]["fecha"] = ""

# 2) Abonos: solo entre las filas que NO se han vaciado, para que salgan 700 clavados
candidatas_abono = [i for i in range(FILAS) if i not in vacias_importe]
for i in random.sample(candidatas_abono, N_ABONOS):
    filas[i]["importe"] = f"-{float(filas[i]['importe']):.2f}"

# 3) Duplicados: SOLO se copian filas completas y positivas, para no inflar ningún recuento
completas = [
    i for i, r in enumerate(filas)
    if r["importe"] and r["cliente"] and r["fecha"] and not r["importe"].startswith("-")
]
for i in random.sample(completas, N_DUPLICADOS):
    filas.append(dict(filas[i]))
random.shuffle(filas)

salida = AQUI / "ventas_2026.csv"
with salida.open("w", encoding="utf-8") as f:
    f.write("pedido_id,fecha,cliente,canal,importe,unidades\n")
    for r in filas:
        f.write(",".join(r[c] for c in ["pedido_id", "fecha", "cliente", "canal", "importe", "unidades"]) + "\n")

manifest = {
    "fichero": salida.name,
    "filas_escritas": len(filas),
    "columnas": ["pedido_id", "fecha", "cliente", "canal", "importe", "unidades"],
    "defectos_inyectados": {
        "importe_vacio": N_IMPORTE_VACIO,
        "cliente_vacio": N_CLIENTE_VACIO,
        "fecha_vacia": N_FECHA_VACIA,
        "filas_duplicadas_enteras": N_DUPLICADOS,
        "importes_negativos_legitimos": N_ABONOS,
        "formatos_de_fecha_distintos": len(FORMATOS_FECHA),
        "variantes_de_canal": len(CANALES),
    },
}
(AQUI / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"escrito {salida.name}: {len(filas)} filas, {salida.stat().st_size / 1024:.0f} KB")
print(json.dumps(manifest["defectos_inyectados"], ensure_ascii=False, indent=1))
