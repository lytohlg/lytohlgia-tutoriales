"""Comprueba el expediente ANTES de unirlo: lo que falta y lo que llega torcido.

Sale con codigo 1 si el expediente no se puede cerrar. Ese "no" es el objetivo:
el rechazo ocurre en tu mesa, no en la mesa del cliente.

Uso:
    python3 comprobar.py            # mira entrada/
"""
import os
import sys

from pypdf import PdfReader

ENTRADA = "entrada"


def leer_indice(ruta):
    filas = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = [p.strip() for p in linea.split("|")]
            if len(partes) < 3:
                continue
            filas.append((int(partes[0]), partes[1], partes[2]))
    filas.sort()
    return filas


def main():
    indice = leer_indice(os.path.join(ENTRADA, "indice.txt"))
    print("EXP-2026-0431  documentos que exige el indice: %d" % len(indice))
    print("")
    print("%-5s %-30s %-32s %s" % ("ORD", "FICHERO", "DOCUMENTO", "ESTADO"))
    faltan = []
    giradas = []
    ilegibles = []
    presentes = []
    total = 0
    for orden, fic, titulo in indice:
        ruta = os.path.join(ENTRADA, fic)
        if not os.path.exists(ruta):
            print("%-5d %-30s %-32s FALTA" % (orden, fic, titulo))
            faltan.append((fic, titulo))
            continue
        try:
            r = PdfReader(ruta)
            npag = len(r.pages)
        except Exception as e:
            print("%-5d %-30s %-32s ILEGIBLE (%s)" % (orden, fic, titulo, type(e).__name__))
            ilegibles.append((fic, type(e).__name__))
            continue
        total += npag
        rot = [p.rotation for p in r.pages]
        raras = [(i + 1, g) for i, g in enumerate(rot) if g % 360 != 0]
        estado = "OK (%d pag.)" % npag
        if raras:
            estado = "OK (%d pag.) pero girada: hoja %s" % (
                npag, ", ".join("%d a %d grados" % (h, g) for h, g in raras))
            giradas.extend([(fic, h, g) for h, g in raras])
        print("%-5d %-30s %-32s %s" % (orden, fic, titulo, estado))
        presentes.append(fic)

    print("")
    print("presentes: %d de %d documentos | paginas: %d" % (len(presentes), len(indice), total))

    if faltan or ilegibles:
        print("")
        print("EXPEDIENTE INCOMPLETO: no se une y no se entrega.")
        for fic, titulo in faltan:
            print("  falta: %s (%s)" % (fic, titulo))
        for fic, err in ilegibles:
            print("  ilegible: %s (%s)" % (fic, err))
        return 1

    if giradas:
        print("")
        print("Por unir: %d hoja(s) con marca de giro del escaner." % len(giradas))
    print("")
    print("EXPEDIENTE COMPLETO: %d documentos, %d paginas. Se puede unir." % (len(presentes), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
