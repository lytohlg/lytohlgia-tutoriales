#!/usr/bin/env python3
"""Lista las tareas guardadas, ordenadas por vencimiento.

Uso:
    python3 tareas.py             # todas, ordenadas por fecha limite
    python3 tareas.py --semana    # solo lo que vence en los proximos 7 dias
    python3 tareas.py --vencidas  # solo lo atrasado
"""
import argparse
import sqlite3
from datetime import date, timedelta

DB = "tareas.db"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--semana", action="store_true")
    ap.add_argument("--vencidas", action="store_true")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    consulta = ("SELECT vencimiento, tipo, tarea, remitente FROM tareas "
                "ORDER BY vencimiento IS NULL, vencimiento")
    filas = con.execute(consulta).fetchall()

    hoy = date.today()
    if args.semana:
        filas = [f for f in filas if f[0] and hoy <= date.fromisoformat(f[0]) <= hoy + timedelta(days=7)]
    if args.vencidas:
        filas = [f for f in filas if f[0] and date.fromisoformat(f[0]) < hoy]

    if not filas:
        print("no hay tareas que mostrar")
        return

    print(f"{'VENCE':<12} {'DIAS':>5}  {'TIPO':<10} TAREA")
    print("-" * 74)
    for vencimiento, tipo, tarea, remitente in filas:
        if vencimiento:
            dias = (date.fromisoformat(vencimiento) - hoy).days
            cuando = "HOY" if dias == 0 else (f"{dias}" if dias > 0 else f"{dias} ATRASADA")
        else:
            dias, cuando = None, "sin fecha"
        print(f"{vencimiento or '--':<12} {cuando:>5}  {tipo:<10} {tarea}")
        print(f"{'':<12} {'':>5}  {'':<10} de {remitente}")
    print(f"\n{len(filas)} tareas")


if __name__ == "__main__":
    main()
