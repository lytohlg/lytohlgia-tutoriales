"""Los limites, medidos: tiempo, escaneos sin capa de texto y firma.

Uso: python3 limites.py
"""
import io
import os
import time

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

SALIDA = "salida"
NOMBRE = "expediente_EXP-2026-0431.pdf"


def sin_texto(ruta):
    """Un PDF que solo tiene un dibujo: como un escaneo sin OCR."""
    c = canvas.Canvas(ruta, pagesize=A4)
    c.rect(80, 500, 400, 220, fill=1)
    c.showPage()
    c.save()


def main():
    ruta = os.path.join(SALIDA, NOMBRE)

    print("[1] cuanto tarda unir: cronometrado")
    t0 = time.time()
    r = PdfReader(ruta)
    r.decrypt(os.environ.get("EXPEDIENTE_CLAVE", "cambiar-esta-clave"))
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    buf = io.BytesIO()
    w.write(buf)
    t = time.time() - t0
    print("    %d paginas releidas y reescritas en %.3f s (%.1f KB)" % (len(r.pages), t, len(buf.getvalue()) / 1024.0))
    print("    es Python puro: funciona en cualquier sitio, y en documentos de")
    print("    cientos de paginas se nota. Aqui se mide, no se supone.")

    print("")
    print("[2] un escaneo sin capa de texto: pypdf no lo puede leer")
    sin_texto("salida/_escaneo_sin_ocr.pdf")
    e = PdfReader("salida/_escaneo_sin_ocr.pdf")
    t = e.pages[0].extract_text() or ""
    print("    caracteres extraidos de la hoja dibujada: %d" % len(t.strip()))
    print("    pypdf mueve paginas; no convierte pixeles en texto. Eso es OCR,")
    print("    otra herramienta. Aqui no se promete lo que no se hace.")

    print("")
    print("[3] lo que este paquete NO demuestra")
    print("    - no firma digitalmente y no certifica validez legal")
    print("    - no comprueba que el contenido sea autentico")
    print("    - la clave viaja en tu entorno: quien la tenga, abre el PDF")
    os.remove("salida/_escaneo_sin_ocr.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
