#!/usr/bin/env python3
"""La parte que casi nadie hace: comprobar que lo extraido es lo que dice el PDF.

Dos modos:

  --carpeta entrada   Lee los PDF, extrae la tabla y comprueba:
                        - fusion de filas partidas (descripcion de dos lineas),
                        - cantidad x precio == importe en cada linea,
                        - suma de importes == TOTAL impreso dentro del PDF,
                        - numero de lineas == LINEAS que declara el PDF.
  --csv salida        Lee los CSV ya volcados (es lo que se envia a contabilidad) y hace
                      las mismas comprobaciones contra el PDF del que salieron. Sirve para
                      cazar un importe tocado a mano despues de exportar.

Si algo no cuadra, lo dice y sale con codigo 1. No adivina: mide.

Uso:
    python3 verificar.py --carpeta entrada
    python3 verificar.py --csv salida --carpeta entrada
"""
import argparse
import csv
import glob
import os
import re

import pdfplumber

from extraer import extraer, fusionar


def numero(texto):
    t = (texto or "").replace("EUR", "").strip().replace(" ", "")
    if "," in t:  # formato espanol: 1.234,56
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def datos_pdf(pdf):
    """Filas de la tabla del PDF + lo que el propio PDF declara (lineas y total)."""
    tabla, _, _ = extraer(pdf, "columnas")
    if not tabla:
        return None, None, None, 0
    bruto = len(tabla) - 1
    filas = fusionar(tabla)
    with pdfplumber.open(pdf) as doc:
        texto = doc.pages[0].extract_text() or ""
    lineas_pdf = int(re.search(r"LINEAS:\s*(\d+)", texto).group(1))
    total_pdf = numero(re.search(r"TOTAL ALBARAN:\s*([\d.,]+ EUR)", texto).group(1))
    return filas, lineas_pdf, total_pdf, bruto


def comprobar(base, filas, lineas_pdf, total_pdf, bruto):
    suma = 0.0
    malas = 0
    for fila in filas:
        c, p, i = numero(fila[2]), numero(fila[3]), numero(fila[4])
        if None in (c, p, i):
            malas += 1
            continue
        if abs(round(c * p, 2) - i) > 0.005:
            malas += 1
        suma = round(suma + i, 2)
    cuadra = (malas == 0 and len(filas) == lineas_pdf and abs(suma - total_pdf) < 0.005)
    print("%-20s filas %2d (bruto %2d) | declaradas %2d | suma %11s | total PDF %11s | mal %d  %s"
          % (base, len(filas), bruto, lineas_pdf, "%.2f" % suma, "%.2f" % total_pdf,
             malas, "CUADRA" if cuadra else "NO CUADRA"))
    return cuadra, len(filas), malas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carpeta", default="entrada")
    ap.add_argument("--csv", default="")
    a = ap.parse_args()

    revisados = 0
    if not a.csv:
        pdfs = sorted(glob.glob(os.path.join(a.carpeta, "*.pdf")))
        revisados = len(pdfs)
        print("comprobando %d albaranes contra el total impreso dentro de cada PDF" % len(pdfs))
        lineas = 0
        descuadres = 0
        for pdf in pdfs:
            base = os.path.basename(pdf)
            filas, lineas_pdf, total_pdf, bruto = datos_pdf(pdf)
            if filas is None:
                print("%-20s sin tabla: nada que comprobar" % base)
                descuadres += 1
                continue
            ok, n, _ = comprobar(base, filas, lineas_pdf, total_pdf, bruto)
            lineas += n
            if not ok:
                descuadres += 1
    else:
        csvs = sorted(glob.glob(os.path.join(a.csv, "*.csv")))
        revisados = len(csvs)
        print("comprobando %d CSV contra el PDF del que salieron" % len(csvs))
        lineas = 0
        descuadres = 0
        for ruta in csvs:
            base = os.path.basename(ruta).split("_tabla")[0]
            pdf = os.path.join(a.carpeta, base + ".pdf")
            _, lineas_pdf, total_pdf, _ = datos_pdf(pdf)
            with open(ruta, newline="", encoding="utf-8") as f:
                filas = [fila for fila in csv.reader(f, delimiter=";")][1:]
            ok, n, _ = comprobar(base + " (CSV)", filas, lineas_pdf, total_pdf, 0)
            lineas += n
            if not ok:
                descuadres += 1

    print()
    if descuadres:
        print("NO VERIFICADO: %d fichero(s) no cuadran" % descuadres)
        raise SystemExit(1)
    print("VERIFICADO: %d albaranes, %d lineas, %d descuadres" % (revisados, lineas, descuadres))


if __name__ == "__main__":
    main()
