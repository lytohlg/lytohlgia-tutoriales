#!/usr/bin/env python3
"""Genera el informe mensual de cada cliente a partir de un CSV.

Un solo script y una sola plantilla: el nombre del cliente y sus cifras salen de los
datos, nunca del texto. Uso:
    python3 generar.py                          # todos los clientes de datos/clientes.csv
    python3 generar.py --solo "Talleres Bravo"  # un cliente concreto
    python3 generar.py --sin-estricto           # SIN StrictUndefined (para comparar)
"""
from __future__ import annotations

import argparse
import csv
import sys
import unicodedata
from collections import OrderedDict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined, UndefinedError

BASE = Path(__file__).resolve().parent


def a_slug(texto: str) -> str:
    """'Ferretería La Clave & Hijos' -> 'ferreteria_la_clave_hijos' (nombre de fichero seguro)."""
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c)
    )
    limpio = "".join(c if c.isalnum() else "_" for c in sin_acentos.lower())
    return "_".join(p for p in limpio.split("_") if p)


def cargar_clientes(ruta: Path) -> "OrderedDict[str, dict]":
    """Agrupa las filas del CSV por cliente, conservando el orden del fichero."""
    clientes: "OrderedDict[str, dict]" = OrderedDict()
    with ruta.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            nombre = fila["cliente"]
            c = clientes.setdefault(nombre, {"nombre": nombre, "contacto": fila["contacto"], "lineas": []})
            for campo in ("descuento",):          # campos opcionales: solo si el CSV los trae
                if campo in fila:
                    c[campo] = fila[campo]
            c["lineas"].append(
                {
                    "concepto": fila["concepto"],
                    "horas": float(fila["horas"]),
                    "precio_hora": float(fila["precio_hora"]),
                }
            )
    return clientes


def main() -> int:
    ap = argparse.ArgumentParser(description="Renderiza el informe mensual de cada cliente.")
    ap.add_argument("--datos", default=str(BASE / "datos" / "clientes.csv"))
    ap.add_argument("--salida", default=str(BASE / "informes"))
    ap.add_argument("--periodo", default="octubre 2026")
    ap.add_argument("--plantilla", default="informe.html", help="plantilla de plantilla/ a usar")
    ap.add_argument("--solo", help="renderiza solo el cliente indicado (nombre exacto)")
    ap.add_argument("--sin-estricto", action="store_true",
                    help="no usa StrictUndefined: un dato que falta se queda en blanco (para comparar)")
    ap.add_argument("--resumen", action="store_true", help="imprime solo el recuento final")
    args = ap.parse_args()

    undefined = Undefined if args.sin_estricto else StrictUndefined
    entorno = Environment(
        loader=FileSystemLoader(str(BASE / "plantilla")),
        undefined=undefined,
        autoescape=True,          # el HTML se escapa solo: un '&' en el nombre no rompe nada
        trim_blocks=True,
        lstrip_blocks=True,
    )
    plantilla = entorno.get_template(args.plantilla)

    clientes = cargar_clientes(Path(args.datos))
    if args.solo:
        if args.solo not in clientes:
            print(f"No existe el cliente «{args.solo}». Hay {len(clientes)}: {', '.join(clientes)}")
            return 2
        clientes = OrderedDict([(args.solo, clientes[args.solo])])

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    for cliente in clientes.values():
        total = sum(l["horas"] * l["precio_hora"] for l in cliente["lineas"])
        try:
            html = plantilla.render(cliente=cliente, periodo=args.periodo)
        except UndefinedError as e:
            # Un dato que la plantilla pide y los datos no traen: se para y se dice cuál.
            print(f"ERROR: la plantilla «{args.plantilla}» pide un dato que los datos no tienen:", file=sys.stderr)
            print(f"       {e}", file=sys.stderr)
            print(f"       cliente: {cliente['nombre']}   datos: {args.datos}", file=sys.stderr)
            return 1
        destino = salida / f"informe_{a_slug(cliente['nombre'])}.html"
        destino.write_text(html, encoding="utf-8")
        if not args.resumen:
            print(f"{destino.name:44s} {len(cliente['lineas'])} conceptos   total {total:8.2f} €")
    print(f"{len(clientes)} informe(s) en {salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
