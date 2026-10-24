#!/usr/bin/env python3
"""Vuelca a CSV las tablas de todos los PDF de una carpeta.

Un fichero por PDF. Separador ';' porque es el que espera Excel en castellano, y los importes
se escriben como numero puro (12,90 -> 12.90) para que la hoja sume sola.

Uso:
    python3 volcar.py --carpeta entrada --salida salida
"""
import argparse
import csv
import glob
import os

from extraer import extraer, fusionar


def limpiar(celda):
    return "" if celda is None else " ".join(celda.split())


def numero(texto):
    """'1.234,56 EUR' -> 1234.56 ; devuelve None si no es un importe."""
    t = (texto or "").replace("EUR", "").strip().replace(" ", "")
    if "," in t:  # formato espanol: 1.234,56
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carpeta", default="entrada")
    ap.add_argument("--salida", default="salida")
    a = ap.parse_args()
    os.makedirs(a.salida, exist_ok=True)

    pdfs = sorted(glob.glob(os.path.join(a.carpeta, "*.pdf")))
    print("PDF en %s/: %d" % (a.carpeta, len(pdfs)))
    total_filas = 0
    escritos = 0
    for pdf in pdfs:
        tabla, _, _ = extraer(pdf, "columnas")
        base = os.path.splitext(os.path.basename(pdf))[0]
        if not tabla:
            print("  %-20s sin tabla" % base)
            continue
        destino = os.path.join(a.salida, "%s_tabla1.csv" % base)
        filas = [tabla[0]] + fusionar(tabla)
        with open(destino, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            for fila in filas:
                celdas = [limpiar(c) for c in fila]
                for j in (3, 4):
                    if j < len(celdas):
                        n = numero(celdas[j])
                        if n is not None:
                            celdas[j] = "%.2f" % n
                w.writerow(celdas)
        print("  %-20s -> %-26s %2d filas" % (base, os.path.basename(destino), len(filas)))
        escritos += 1
        total_filas += len(filas) - 1
    print("ESCRITO: %d CSV, %d filas de datos" % (escritos, total_filas))


if __name__ == "__main__":
    main()
