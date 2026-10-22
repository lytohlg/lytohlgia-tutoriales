"""Manifiesto: que documento quedo en que pagina del paquete final.

El indice dice QUE documentos y en QUE orden. Este script comprueba que el PDF
cerrado cumple eso: recorre los marcadores y compara su pagina con la que sale
de sumar las paginas de cada documento del indice.

Uso: python3 manifiesto.py
"""
import os
import sys

from pypdf import PdfReader

ENTRADA = "entrada"
SALIDA = "salida"
NOMBRE = "expediente_EXP-2026-0431.pdf"


def leer_indice():
    filas = []
    with open(os.path.join(ENTRADA, "indice.txt"), encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            p = [x.strip() for x in linea.split("|")]
            if len(p) >= 3:
                filas.append((int(p[0]), p[1], p[2]))
    filas.sort()
    return filas


def main():
    ruta = os.path.join(SALIDA, NOMBRE)
    r = PdfReader(ruta)
    r.decrypt(os.environ.get("EXPEDIENTE_CLAVE", "cambiar-esta-clave"))
    indice = leer_indice()
    marcas = list(r.outline)

    print("MANIFIESTO  %s  (%d paginas)" % (NOMBRE, len(r.pages)))
    print("%-4s %-30s %-8s %-8s %-8s %s" % ("POS", "DOCUMENTO", "DESDE", "HASTA", "MARCA", "ESTADO"))
    esperado = 1
    fallos = 0
    for (orden, fic, titulo), item in zip(indice, marcas):
        n = len(PdfReader(os.path.join(ENTRADA, fic)).pages)
        desde, hasta = esperado, esperado + n - 1
        pagina = r.get_destination_page_number(item) + 1
        ok = pagina == desde and getattr(item, "title", "") == titulo
        fallos += 0 if ok else 1
        print("%-4d %-30s %-8d %-8d %-8d %s" % (orden, titulo, desde, hasta, pagina,
                                                "coincide" if ok else "NO COINCIDE"))
        esperado = hasta + 1

    if len(marcas) != len(indice):
        print("marcadores: %d, documentos en el indice: %d" % (len(marcas), len(indice)))
        fallos += 1
    print("")
    if fallos:
        print("MANIFIESTO NO CUADRA: %d discrepancia(s)" % fallos)
        return 1
    print("MANIFIESTO CUADRA: %d documentos, %d paginas, cada marcador en su pagina"
          % (len(indice), len(r.pages)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
