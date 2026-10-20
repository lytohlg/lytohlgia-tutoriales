#!/usr/bin/env python3
"""Fabrica tres PDF ESCANEADOS de verdad: imagen, sin capa de texto.

No son PDF de texto con una etiqueta: se dibuja la pagina, se convierte a imagen,
se le mete un poco de ruido y una rotacion minima (como un escaner de mesa) y se
guarda la imagen dentro del PDF. pdftotext devuelve cero caracteres porque no hay
texto: hay pixeles. Eso es exactamente lo que llega a una oficina.
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1240, 1754          # A4 a 150 ppp, resolucion tipica de escaner
OUT = "entrada"
FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
NEGRITA = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

DOCUMENTOS = [
    (
        "contrato_alquiler.pdf",
        "CONTRATO DE ARRENDAMIENTO",
        [
            "Entre D. Alvaro Menendez Rios, con DNI 44.821.337-K,",
            "y Dna. Lucía Ferrán Olmos, con DNI 51.204.998-B,",
            "se firma el presente contrato de arrendamiento.",
            "",
            "CLÁUSULA SEPTIMA. La renta mensual se fija en 780 euros,",
            "pagadera los cinco primeros dias de cada mes mediante",
            "transferencia a la cuenta ES91 2100 0418 4502 0005 1332.",
            "",
            "CLÁUSULA OCTAVA. La fianza depositada asciende a 1.560 euros",
            "y se devolvera en el plazo de treinta dias naturales.",
        ],
    ),
    (
        "factura_enero.pdf",
        "FACTURA Nº 2026-0041",
        [
            "Proveedor: Suministros Norte S.L.  CIF B-39482115",
            "Cliente: Talleres Ribera S.A.     CIF A-28117420",
            "Fecha de emision: 12 de enero de 2026",
            "",
            "Concepto                     Cantidad      Importe",
            "Tornilleria industrial            240       612,40",
            "Mantenimiento preventivo            1       430,00",
            "Portes                              1        38,50",
            "",
            "IMPORTE TOTAL A PAGAR: 1.080,90 euros",
            "Vencimiento: 11 de febrero de 2026",
        ],
    ),
    (
        "acta_reunion.pdf",
        "ACTA DE LA REUNION DE VECINOS",
        [
            "Fecha: 3 de febrero de 2026. Lugar: portal 4, bajo.",
            "Asistentes: 11 propietarios de los 14 convocados.",
            "",
            "PRIMERO. Se aprueba el presupuesto de 4.820 euros para",
            "la reparacion de la cubierta del edificio.",
            "",
            "SEGUNDO. Se acuerda pedir tres ofertas antes del 30 de",
            "marzo y someterlas a votacion en la proxima reunion.",
            "",
            "TERCERO. El administrador informa del saldo disponible:",
            "9.140 euros en la cuenta comun.",
        ],
    ),
]


def pagina(titulo, lineas, nombre):
    img = Image.new("RGB", (W, H), (252, 251, 247))
    d = ImageDraw.Draw(img)
    f_tit = ImageFont.truetype(NEGRITA, 34)
    f_txt = ImageFont.truetype(FUENTE, 25)

    y = 150
    d.text((110, y), titulo, font=f_tit, fill=(20, 20, 20))
    y += 70
    d.line((110, y, W - 110, y), fill=(120, 120, 120), width=2)
    y += 45
    for linea in lineas:
        d.text((110, y), linea, font=f_txt, fill=(28, 28, 28))
        y += 38
    d.text((110, H - 130), "Documento de ejemplo. Datos inventados.", font=f_txt, fill=(90, 90, 90))

    # Ruido leve del escaner
    px = img.load()
    for _ in range(26000):
        x, y2 = random.randrange(W), random.randrange(H)
        g = random.randrange(205, 240)
        px[x, y2] = (g, g, g - 4)

    # Escaneo torcido: medio grado. Nada exagerado, como la realidad.
    img = img.rotate(0.45, resample=Image.BICUBIC, fillcolor=(252, 251, 247))
    img = img.point(lambda v: min(255, int(v * 1.02)))   # contraste de escaner

    ruta = os.path.join(OUT, nombre)
    img.save(ruta, "PDF", resolution=150.0, quality=72)
    return ruta


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    random.seed(20261017)
    for nombre, titulo, lineas in DOCUMENTOS:
        p = pagina(titulo, lineas, nombre)
        print("escaneado: %-24s %7d bytes" % (os.path.basename(p), os.path.getsize(p)))
    print("3 documentos en entrada (imagen, sin capa de texto)")
