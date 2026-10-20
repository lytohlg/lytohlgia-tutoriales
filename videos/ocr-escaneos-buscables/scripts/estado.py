#!/usr/bin/env python3
"""Mide, documento a documento, si el PDF TIENE texto seleccionable o no.

La prueba no es una opinion: se lanza pdftotext (poppler) y se cuentan los
caracteres que devuelve. 0 = no hay capa de texto = para un buscador o para
copiar y pegar, el documento es una foto.

Uso: python3 estado.py [carpeta]   (por defecto entrada)
"""
import os
import subprocess
import sys

CARPETA = sys.argv[1] if len(sys.argv) > 1 else "entrada"


def caracteres(pdf):
    r = subprocess.run(["pdftotext", "-q", pdf, "-"], capture_output=True)
    texto = r.stdout.decode("utf-8", "replace")
    return len(texto.replace("\f", "").strip()), texto


def paginas(pdf):
    r = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True)
    for linea in r.stdout.splitlines():
        if linea.startswith("Pages:"):
            return int(linea.split()[1])
    return 0


pdfs = sorted(f for f in os.listdir(CARPETA) if f.lower().endswith(".pdf"))
print("%-26s %7s %9s  %s" % ("DOCUMENTO", "PAGINAS", "CARACTERES", "ESTADO"))
print("-" * 66)
sin_texto = 0
for f in pdfs:
    p = os.path.join(CARPETA, f)
    n, _ = caracteres(p)
    estado = "SIN TEXTO (0 chars)" if n == 0 else "con texto (%d chars)" % n
    sin_texto += (n == 0)
    print("%-26s %7d %9d  %s" % (f, paginas(p), n, estado))
print("-" * 66)
print("documentos: %d | sin capa de texto: %d" % (len(pdfs), sin_texto))
