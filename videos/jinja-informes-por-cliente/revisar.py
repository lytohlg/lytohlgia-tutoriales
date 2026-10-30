#!/usr/bin/env python3
"""Comprueba que cada informe es del cliente que dice ser.

No basta con que el script «termine sin error»: aquí se comprueba el RESULTADO.
  1. existe un fichero por cliente
  2. en cada informe aparece SU nombre y NO aparece el de ningún otro cliente
  3. el total impreso coincide con el recalculado desde el CSV
"""
from __future__ import annotations

import csv
import html as html_lib
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
from generar import a_slug, cargar_clientes  # noqa: E402

TOTAL_RE = re.compile("<th[^>]*>Total</th><th>([0-9.]+) €</th>")


def main() -> int:
    datos = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "datos" / "clientes.csv"
    salida = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "informes"
    clientes = cargar_clientes(datos)
    fallos = 0
    cruzados = 0
    for nombre, c in clientes.items():
        fichero = salida / f"informe_{a_slug(nombre)}.html"
        if not fichero.exists():
            print(f"FALLO  {nombre}: no existe {fichero.name}")
            fallos += 1
            continue
        crudo = fichero.read_text(encoding="utf-8")
        html = html_lib.unescape(crudo)   # el HTML escapa '&' como '&amp;': se compara el texto real
        if nombre not in html:
            print(f"FALLO  {nombre}: su nombre no aparece en {fichero.name}")
            fallos += 1
        intrusos = [otro for otro in clientes if otro != nombre and otro in html]
        if intrusos:
            print(f"FALLO  {nombre}: aparece(n) otro(s) cliente(s) en su informe: {intrusos}")
            cruzados += len(intrusos)
            fallos += 1
        esperado = sum(l["horas"] * l["precio_hora"] for l in c["lineas"])
        m = TOTAL_RE.search(html)
        hallado = float(m.group(1)) if m else None
        if hallado is None:
            print(f"FALLO  {nombre}: no se encuentra el total en el HTML")
            fallos += 1
        elif abs(hallado - esperado) > 0.001:
            print(f"FALLO  {nombre}: total del HTML {hallado:.2f} € != recalculado {esperado:.2f} €")
            fallos += 1
        else:
            print(f"OK     {nombre:28s} {fichero.name:44s} total {hallado:8.2f} €")
    print(f"\n{len(clientes) - fallos}/{len(clientes)} informes correctos · nombres cruzados: {cruzados}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
