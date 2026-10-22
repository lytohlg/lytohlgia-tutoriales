"""Une el expediente en el orden del indice, endereza, numera y cifra.

El orden lo manda indice.txt, nunca el nombre del fichero.
Cada documento entra con su marcador (outline), asi el paquete se puede navegar.
La numeracion se pinta con reportlab; quien une y cifra es pypdf.

Uso:
    python3 unir.py                       # -> salida/expediente_EXP-2026-0431.pdf
    EXPEDIENTE_CLAVE=otra python3 unir.py
"""
import io
import os
import sys
import time

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ENTRADA = "entrada"
SALIDA = "salida"
NOMBRE = "expediente_EXP-2026-0431.pdf"


def leer_indice(ruta):
    filas = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = [p.strip() for p in linea.split("|")]
            if len(partes) >= 3:
                filas.append((int(partes[0]), partes[1], partes[2]))
    filas.sort()
    return filas


def sello_numero(ancho, alto, n, total):
    """Una hoja transparente con 'Pagina n de total' abajo a la derecha."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(float(ancho), float(alto)))
    c.setFont("Helvetica", 9)
    c.drawRightString(float(ancho) - 40, 24, "Pagina %d de %d" % (n, total))
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def main():
    t0 = time.time()
    indice = leer_indice(os.path.join(ENTRADA, "indice.txt"))
    for orden, fic, _ in indice:
        if not os.path.exists(os.path.join(ENTRADA, fic)):
            print("No se une: falta %s" % fic)
            return 1

    # 1) leer y preparar: enderezar las hojas con marca de giro
    docs = []
    enderezadas = 0
    total_pag = 0
    for orden, fic, titulo in indice:
        r = PdfReader(os.path.join(ENTRADA, fic))
        for p in r.pages:
            if p.rotation % 360 != 0:
                p.rotation = 0          # /Rotate a cero: el contenido no se toca
                enderezadas += 1
        docs.append((titulo, r, len(r.pages)))
        total_pag += len(r.pages)
        print("  leido %-30s %d pag." % (fic, len(r.pages)))

    # 2) unir en el orden del indice, con marcador por documento
    w = PdfWriter()
    for titulo, r, n in docs:
        w.append(r, outline_item=titulo)
        print("  dentro: %-32s +%d pag." % (titulo, n))

    # 3) numerar cada hoja
    for i, p in enumerate(w.pages, 1):
        box = p.mediabox
        p.merge_page(sello_numero(box.width, box.height, i, total_pag))

    print("")
    print("unidas %d paginas de %d documentos | hojas enderezadas: %d"
          % (total_pag, len(docs), enderezadas))

    # 4) cifrar con AES-256 (clave de ejemplo: cambiala en tu .env)
    clave = os.environ.get("EXPEDIENTE_CLAVE", "cambiar-esta-clave")
    w.encrypt(user_password=clave, owner_password=clave, algorithm="AES-256")

    os.makedirs(SALIDA, exist_ok=True)
    destino = os.path.join(SALIDA, NOMBRE)
    with open(destino, "wb") as f:
        w.write(f)
    t = time.time() - t0
    print("escrito: %s (%.1f KB) en %.2f s" % (destino, os.path.getsize(destino) / 1024.0, t))
    print("cifrado: AES-256 con clave del entorno (EXPEDIENTE_CLAVE)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
