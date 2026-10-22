"""Fabrica el expediente de EJEMPLO: un indice y los PDF sueltos.

Todos los datos son inventados. El indice es la unica fuente del orden: los
nombres de fichero NO llevan numero a proposito, para que el orden lo ponga el
indice y no el orden alfabetico de la carpeta.

Uso:
    python3 sembrar_expediente.py              # 5 de 6 documentos (falta el certificado)
    python3 sembrar_expediente.py --completo    # con el certificado que faltaba
"""
import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

SALIDA = "entrada"

INDICE = [
    ("solicitud_aportacion.pdf", "Solicitud de aportacion"),
    ("dni_titular.pdf", "DNI del titular"),
    ("nomina_ultima.pdf", "Nomina del ultimo mes"),
    ("contrato_alquiler.pdf", "Contrato de alquiler"),
    ("informe_vida_laboral.pdf", "Informe de vida laboral"),
    ("certificado_empresa.pdf", "Certificado de empresa"),
]

PAGINAS = {
    "solicitud_aportacion.pdf": 1,
    "dni_titular.pdf": 1,
    "nomina_ultima.pdf": 1,
    "contrato_alquiler.pdf": 3,
    "informe_vida_laboral.pdf": 2,
    "certificado_empresa.pdf": 1,
}


def hoja(ruta, titulo, lineas, rotar=0):
    """Un PDF simple: un titulo y unas lineas de texto, todo inventado."""
    c = canvas.Canvas(ruta, pagesize=A4)
    w, h = A4
    y = h - 80
    c.setFont("Helvetica-Bold", 16)
    c.drawString(70, y, titulo)
    c.setFont("Helvetica", 11)
    for ln in lineas:
        y -= 26
        c.drawString(70, y, ln)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(70, 40, "Documento de ejemplo. Datos inventados. Sin validez legal.")
    c.showPage()
    c.save()
    if rotar:
        # Un escaneo que llego girado: el contenido es correcto, pero la pagina
        # lleva /Rotate puesto por el escaner. Se marca aqui tal cual.
        girar(ruta, rotar)


def girar(ruta, grados):
    from pypdf import PdfReader, PdfWriter

    r = PdfReader(ruta)
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.pages[0].rotate(grados)
    with open(ruta, "wb") as f:
        w.write(f)


def main():
    completo = "--completo" in sys.argv
    os.makedirs(SALIDA, exist_ok=True)

    with open(os.path.join(SALIDA, "indice.txt"), "w", encoding="utf-8") as f:
        f.write("# indice del expediente EXP-2026-0431\n")
        f.write("# orden | fichero | documento\n")
        for i, (fic, tit) in enumerate(INDICE, 1):
            f.write("%d | %s | %s\n" % (i, fic, tit))

    docs = INDICE if completo else INDICE[:-1]
    for fic, tit in docs:
        ruta = os.path.join(SALIDA, fic)
        npag = PAGINAS[fic]
        if npag > 1:
            # documentos de varias hojas: se escriben hoja a hoja y se unen
            partes = []
            for n in range(1, npag + 1):
                parte = os.path.join(SALIDA, "_p%d.pdf" % n)
                hoja(parte, "%s (hoja %d de %d)" % (tit, n, npag),
                     ["Titular: Titular de Ejemplo", "Referencia: EXP-2026-0431",
                      "Contenido inventado para la demostracion."])
                partes.append(parte)
            from pypdf import PdfWriter
            w = PdfWriter()
            for p in partes:
                w.append(p)
            with open(ruta, "wb") as f:
                w.write(f)
            for p in partes:
                os.remove(p)
        elif fic == "dni_titular.pdf":
            hoja(ruta, tit, ["Titular: Titular de Ejemplo", "Documento: DEMO-0001",
                             "Este escaneo llego girado del escaner."], rotar=90)
        else:
            hoja(ruta, tit, ["Titular: Titular de Ejemplo", "Referencia: EXP-2026-0431",
                             "Contenido inventado para la demostracion."])

    sueltos = sorted(x for x in os.listdir(SALIDA) if x.endswith(".pdf"))
    total = sum(PAGINAS[x] for x in sueltos)
    print("entrada/ sembrada: %d documentos sueltos, %d paginas en total" % (len(sueltos), total))
    for x in sueltos:
        print("  %-28s %d pag." % (x, PAGINAS[x]))
    pide = len(INDICE)
    if len(sueltos) < pide:
        faltan = [t for f_, t in INDICE if f_ not in sueltos]
        print("el indice pide %d documentos; en la carpeta hay %d" % (pide, len(sueltos)))
        print("falta: %s" % ", ".join(faltan))


if __name__ == "__main__":
    main()
