#!/usr/bin/env python3
"""La primera versión: lee la plantilla "de al lado". En la carpeta del código funciona."""
import csv
import statistics
import sys

from rich.console import Console


def main() -> int:
    filas = list(csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8")))
    for r in filas:
        r["importe"] = float(r["importe"])
    plantilla = open("plantilla.txt", encoding="utf-8").read().strip()
    consola = Console()
    consola.print(f"[bold]{plantilla}[/bold]")
    consola.print(f"filas: {len(filas)}   total: "
                  f"{sum(r['importe'] for r in filas):,.2f} EUR   "
                  f"media: {statistics.mean(r['importe'] for r in filas):,.2f} EUR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
