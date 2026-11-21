#!/usr/bin/env python3
"""Genera datos/ventas.csv: 120 filas deterministas (semilla fija, sin red)."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(20261121)
CLIENTES = ["ACME", "Norte SL", "Talleres Ruiz", "Panaderia Sol", "Grupo Delta",
            "Ferreteria Vidal", "Clínica Mar", "Estudio Prado"]
SALIDA = Path(__file__).resolve().parent / "ventas.csv"

filas = []
dia = date(2026, 9, 1)
for i in range(120):
    dia = dia + timedelta(days=random.choice([0, 1, 1, 2]))
    filas.append({
        "fecha": dia.isoformat(),
        "cliente": random.choice(CLIENTES),
        "concepto": f"pedido {1000 + i}",
        "importe": f"{random.uniform(45, 890):.2f}",
    })

with open(SALIDA, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["fecha", "cliente", "concepto", "importe"])
    w.writeheader()
    w.writerows(filas)
print(f"escrito {SALIDA} con {len(filas)} filas")
