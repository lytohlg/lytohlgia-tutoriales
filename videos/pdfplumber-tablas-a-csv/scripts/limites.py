#!/usr/bin/env python3
"""Los limites, medidos en esta maquina y dichos sin adornos.

  1. Una descripcion que ocupa dos lineas dentro de una celda sale partida en dos filas.
  2. Un PDF escaneado (una foto dentro de un PDF) no tiene texto: 0 caracteres, 0 tablas.

Uso:
    python3 limites.py
"""
import glob
import os
import subprocess

import pdfplumber
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from extraer import extraer


def limite_celdas_partidas():
    pdf = "entrada/albaran_0330.pdf"
    tabla, _, _ = extraer(pdf, "columnas")
    bruto = len(tabla) - 1
    con_ref = sum(1 for f in tabla[1:] if (f[0] or "").strip())
    print("1) celdas de dos lineas (%s)" % os.path.basename(pdf))
    print("   filas que devuelve pdfplumber: %d | filas con referencia: %d" % (bruto, con_ref))
    print("   -> %d fila(s) son continuacion de la descripcion y hay que fusionarlas"
          % (bruto - con_ref))


def limite_escaneado():
    origen = "entrada/albaran_0310.pdf"
    tmp = "tmp_limites"
    os.makedirs(tmp, exist_ok=True)
    destino = os.path.join(tmp, "escaneado.pdf")
    try:
        subprocess.run(["pdftoppm", "-r", "120", "-png", "-f", "1", "-l", "1", origen,
                        os.path.join(tmp, "pag")], check=True, capture_output=True, timeout=120)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("2) escaneado: no hay pdftoppm en este entorno, no se puede fabricar el caso. N/A")
        return
    png = sorted(glob.glob(os.path.join(tmp, "pag*.png")))[0]
    c = canvas.Canvas(destino, pagesize=A4)
    c.drawImage(png, 0, 0, width=A4[0], height=A4[1])
    c.showPage()
    c.save()
    with pdfplumber.open(destino) as doc:
        p = doc.pages[0]
        texto = p.extract_text() or ""
        tablas = p.extract_tables(table_settings={
            "vertical_strategy": "text", "horizontal_strategy": "text"})
    print("2) PDF escaneado (%d bytes, la pagina dibujada como imagen)" % os.path.getsize(destino))
    print("   caracteres de texto: %d | tablas: %d" % (len(texto), len(tablas)))
    print("   -> sin capa de texto no hay nada que extraer: primero hay que aplicar OCR")


def main():
    print("LIMITES MEDIDOS (esta maquina, este entorno)")
    print()
    limite_celdas_partidas()
    print()
    limite_escaneado()


if __name__ == "__main__":
    main()
