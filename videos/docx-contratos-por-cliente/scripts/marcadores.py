#!/usr/bin/env python3
"""Lista los marcadores {{...}} que trae la plantilla, estén donde estén.

No busca solo en los párrafos del cuerpo: también en las celdas de las tablas,
que es donde suele esconderse el que nadie ve.
"""
import re
import sys

from docx import Document

PATRON = re.compile(r"\{\{[A-Z0-9_]+\}\}")


def textos(doc):
    """Devuelve (dónde, texto) del cuerpo y de cada celda."""
    for i, p in enumerate(doc.paragraphs, 1):
        yield "párrafo %d" % i, p.text
    for ti, tabla in enumerate(doc.tables, 1):
        for fi, fila in enumerate(tabla.rows, 1):
            for ci, celda in enumerate(fila.cells, 1):
                for p in celda.paragraphs:
                    yield "tabla %d fila %d col %d" % (ti, fi, ci), p.text


def main():
    doc = Document("plantilla/contrato_plantilla.docx")
    vistos = {}
    apariciones = 0
    for donde, texto in textos(doc):
        for m in PATRON.findall(texto):
            apariciones += 1
            vistos[m] = vistos.get(m, 0) + 1
            print("%-22s %s" % (donde, m))
    print()
    print("marcadores distintos: %d | apariciones: %d" % (len(vistos), apariciones))
    for m, n in sorted(vistos.items()):
        print("  %-14s x%d" % (m, n))
    return 0 if vistos else 1


if __name__ == "__main__":
    sys.exit(main())
