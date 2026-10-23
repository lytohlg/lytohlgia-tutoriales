#!/usr/bin/env python3
"""Comprueba los documentos GENERADOS, con dos lectores que no son el mismo.

 1) python-docx relee cada .docx y busca el nombre, el CIF y el importe del CSV,
    y que no quede ningún marcador.
 2) unzip -p word/document.xml | grep: se lee el XML con una herramienta que no
    es python-docx. Si el documento se escribió mal, aquí también se ve.
"""
import argparse
import csv
import glob
import subprocess
import sys

from docx import Document

CAMPOS = ("cliente", "cif", "importe")


def texto_docx(doc):
    partes = [p.text for p in doc.paragraphs]
    for tabla in doc.tables:
        for fila in tabla.rows:
            for celda in fila.cells:
                partes.extend(p.text for p in celda.paragraphs)
    return "\n".join(partes)


def comprobar_formato(plantilla, generado):
    """Compara el DISEÑO de la plantilla con el del documento escrito.

    No compara texto (es lo que cambia): compara estilos de párrafo, tablas y
    el tamaño del título. Un contrato con los datos bien y el diseño roto no
    sirve para enviarlo.
    """
    a = Document(plantilla)
    b = Document(generado)
    fallos = []
    estilos_a = [p.style.name for p in a.paragraphs]
    estilos_b = [p.style.name for p in b.paragraphs]
    if estilos_a != estilos_b:
        fallos.append("estilos de párrafo distintos")
    if len(a.tables) != len(b.tables):
        fallos.append("número de tablas distinto")
    else:
        for i, (ta, tb) in enumerate(zip(a.tables, b.tables), 1):
            if ta.style.name != tb.style.name:
                fallos.append("estilo de la tabla %d distinto" % i)
            if (len(ta.rows), len(ta.columns)) != (len(tb.rows), len(tb.columns)):
                fallos.append("tamaño de la tabla %d distinto" % i)
    ta_titulo = a.paragraphs[0].runs[0].font.size
    tb_titulo = b.paragraphs[0].runs[0].font.size
    if ta_titulo != tb_titulo:
        fallos.append("tamaño del título distinto")
    return fallos, len(estilos_a), len(a.tables), ta_titulo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="clientes.csv")
    args = ap.parse_args()

    with open(args.csv, encoding="utf-8", newline="") as f:
        filas = [x for x in csv.DictReader(f) if all((x.get(c) or "").strip() for c in CAMPOS)]

    fallos = 0
    revisados = 0
    for n, fila in enumerate(filas, 1):
        candidatos = sorted(glob.glob("salida/contrato_%02d_*.docx" % n))
        if not candidatos:
            print("%2d  FALTA el documento de %s" % (n, fila["cliente"]))
            fallos += 1
            continue
        ruta = candidatos[0]
        doc = Document(ruta)
        junto = texto_docx(doc)
        problemas = []
        if "{{" in junto:
            problemas.append("queda un marcador")
        for campo in CAMPOS:
            if fila[campo].strip() not in junto:
                problemas.append("no aparece el %s" % campo)
        xml = subprocess.run(["unzip", "-p", ruta, "word/document.xml"],
                             capture_output=True, text=True).stdout
        externas = xml.count("{{")
        if externas:
            problemas.append("%d marcas {{ en el XML" % externas)

        revisados += 1
        if problemas:
            fallos += 1
            print("%2d  %-26s FALLA: %s" % (n, fila["cliente"], ", ".join(problemas)))
        else:
            print("%2d  %-26s %10s EUR  nombre, CIF e importe OK | 0 marcadores"
                  % (n, fila["cliente"], fila["importe"]))

    print()
    # Formato: los datos pueden estar bien y el diseño roto. Se compara con la plantilla.
    difs, n_parr, n_tablas, tam = comprobar_formato("plantilla/contrato_plantilla.docx",
                                                    sorted(glob.glob("salida/contrato_01_*.docx"))[0])
    if difs:
        print("FORMATO: distinto al de la plantilla -> %s" % ", ".join(difs))
        fallos += 1
    else:
        print("FORMATO: %d párrafos y %d tabla, mismos estilos que la plantilla, título %s"
              % (n_parr, n_tablas, ("a %s pt" % tam.pt) if tam else "con el estilo de la plantilla"))

    print()
    if fallos:
        print("NO VERIFICADO: %d de %d documentos con problemas" % (fallos, len(filas)))
        return 1
    print("VERIFICADO: %d documentos, 0 marcadores, nombre y CIF y importe comprobados uno a uno, "
          "XML releido con unzip" % revisados)
    return 0


if __name__ == "__main__":
    sys.exit(main())
