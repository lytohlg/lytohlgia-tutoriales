#!/usr/bin/env python3
"""Cuenta, documento a documento, cuántos datos personales se pueden sacar.

La prueba no es una opinión: se extrae el texto con PyMuPDF y se pasan los
patrones. Lo que salga aquí es lo que cualquiera puede copiar de ese PDF.

Uso: python3 estado.py [carpeta]
"""
import os
import sys

import fitz

from patrones import buscar

CARPETA = sys.argv[1] if len(sys.argv) > 1 else "entrada"

print("%-24s %7s %8s %6s %6s %6s %6s" %
      ("DOCUMENTO", "CHARS", "TOTAL", "DNI", "IBAN", "TEL", "EMAIL"))
print("-" * 70)

total = 0
for f in sorted(x for x in os.listdir(CARPETA) if x.endswith(".pdf")):
    doc = fitz.open(os.path.join(CARPETA, f))
    texto = "\n".join(p.get_text() for p in doc)
    doc.close()
    hallazgos = buscar(texto)
    n = sum(len(v) for v in hallazgos.values())
    total += n
    print("%-24s %7d %8d %6d %6d %6d %6d" %
          (f, len(texto.strip()), n, len(hallazgos["DNI"]),
           len(hallazgos["IBAN"]), len(hallazgos["TELEFONO"]),
           len(hallazgos["EMAIL"])))

print("-" * 70)
print("datos personales localizados en total: %d" % total)
