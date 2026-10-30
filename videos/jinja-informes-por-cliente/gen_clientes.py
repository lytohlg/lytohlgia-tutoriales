#!/usr/bin/env python3
"""Genera un CSV de N clientes inventados para ver que el mismo código escala.

    python3 gen_clientes.py --n 100
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
CONCEPTOS = ["Consultoría", "Mantenimiento", "Formación", "Soporte", "Auditoría", "Implantación"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--salida", default=str(BASE / "datos" / "clientes_100.csv"))
    args = ap.parse_args()

    destino = Path(args.salida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cliente", "contacto", "concepto", "horas", "precio_hora"])
        for i in range(1, args.n + 1):
            cliente = f"Cliente {i:03d}"
            for j in range(1 + i % 3):
                w.writerow([
                    cliente,
                    f"Oficina · ext. {i:02d}",
                    CONCEPTOS[(i + j) % len(CONCEPTOS)],
                    2 + (i + j) % 19,
                    40 + (i % 6) * 5,
                ])
    print(f"{args.n} clientes escritos en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
