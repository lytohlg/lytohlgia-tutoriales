#!/usr/bin/env python3
"""Resumen de ventas en una tabla. Uso: resumen datos/ventas.csv"""
import csv
import statistics
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table


def carpeta_datos() -> Path:
    """Dónde viven los ficheros que VIAJAN con el ejecutable.

    Empaquetado con PyInstaller, el programa no vive junto a sus ficheros: el
    arrancador los descomprime en sys._MEIPASS. Si se busca "aquí al lado"
    (open("plantilla.txt")) funciona en la carpeta del código y falla en cuanto
    alguien copia el ejecutable a otro sitio. Eso es lo que arregla esta función.
    """
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent


def leer_ventas(ruta: str) -> list[dict]:
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for r in filas:
        r["importe"] = float(r["importe"])
    return filas


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: resumen <ventas.csv>")
        return 2

    filas = leer_ventas(sys.argv[1])
    total = sum(r["importe"] for r in filas)
    importes = [r["importe"] for r in filas]
    plantilla = (carpeta_datos() / "plantilla.txt").read_text(encoding="utf-8").strip()

    consola = Console()
    consola.print(f"[bold]{plantilla}[/bold]")
    consola.print(f"filas: {len(filas)}   total: {total:,.2f} EUR")
    consola.print(f"ticket medio: {statistics.mean(importes):,.2f} EUR   "
                  f"mediana: {statistics.median(importes):,.2f} EUR")

    por_cliente: dict[str, float] = {}
    for r in filas:
        por_cliente[r["cliente"]] = por_cliente.get(r["cliente"], 0.0) + r["importe"]
    top = sorted(por_cliente.items(), key=lambda kv: kv[1], reverse=True)[:5]

    tabla = Table(title="Top 5 clientes por facturacion")
    tabla.add_column("cliente")
    tabla.add_column("importe", justify="right")
    for nombre, importe in top:
        tabla.add_row(nombre, f"{importe:,.2f} EUR")
    consola.print(tabla)
    return 0


if __name__ == "__main__":
    sys.exit(main())
