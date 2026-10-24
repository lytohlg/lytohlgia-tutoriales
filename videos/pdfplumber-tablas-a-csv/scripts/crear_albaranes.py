#!/usr/bin/env python3
"""Fabrica tres albaranes en PDF: los datos son inventados y el total lo calcula el propio script.

- albaran_0310.pdf : tabla CON lineas de rejilla dibujadas.
- albaran_0320.pdf : tabla SIN ninguna linea, solo columnas alineadas por texto.
- albaran_0330.pdf : tabla con lineas y una descripcion que ocupa DOS lineas dentro de la celda.

El total impreso dentro del PDF es la suma real de las lineas de ese PDF: asi se puede
comprobar despues, leyendo el propio documento, que lo extraido cuadra.
"""
import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

SALIDA = "entrada"

# (referencia, descripcion, cantidad, precio unitario)
ITEMS = {
    "0310": [
        ("AR-101", "Cable HDMI 2.1 de 3 metros", 4, 12.90),
        ("AR-102", "Regleta de 6 tomas con interruptor", 2, 18.45),
        ("AR-103", "Tornillo M4 x 20 (caja de 100)", 3, 7.20),
        ("AR-104", "Etiquetas adhesivas 50 x 30 mm", 10, 4.15),
        ("AR-105", "Bridas de nylon 200 mm (bolsa)", 5, 3.80),
        ("AR-106", "Fuente de alimentacion 12 V 2 A", 6, 14.60),
        ("AR-107", "Latiguillo de red cat 6 (2 m)", 12, 2.95),
        ("AR-108", "Guantes de trabajo talla L", 8, 1.85),
        ("AR-109", "Cinta aislante negra", 9, 1.40),
        ("AR-110", "Caja de conexiones IP65", 4, 9.75),
        ("AR-111", "Soporte de pared regulable", 3, 22.30),
    ],
    "0320": [
        ("BE-201", "Brazo articulado para monitor", 2, 41.50),
        ("BE-202", "Tornilleria surtida M3-M6", 4, 11.20),
        ("BE-203", "Canaleta de 2 metros", 6, 6.40),
        ("BE-204", "Regleta de superficie 4 tomas", 5, 9.90),
        ("BE-205", "Adaptador USB-C a HDMI", 3, 16.75),
        ("BE-206", "Organizador de cables (set de 5)", 7, 5.30),
        ("BE-207", "Alargo de 5 metros", 4, 13.25),
        ("BE-208", "Base de enchufe empotrable", 8, 4.60),
        ("BE-209", "Fijaciones para pladur (20 uds)", 6, 3.15),
        ("BE-210", "Guia pasacables blanco", 10, 1.95),
        ("BE-211", "Soporte de techo para proyector", 1, 34.80),
    ],
    "0330": [
        ("CL-301", "Monitor 24 pulgadas\n(Full HD, IPS)", 2, 118.90),
        ("CL-302", "Teclado inalambrico\n(distribucion espanola)", 3, 27.40),
        ("CL-303", "Raton optico\n(USB, 1600 dpi)", 3, 9.60),
        ("CL-304", "Hub USB de 4 puertos\n(USB 3.0)", 4, 15.20),
        ("CL-305", "Webcam 1080p\n(con microfono)", 2, 32.55),
        ("CL-306", "Soporte para portatil\n(aluminio)", 5, 21.10),
        ("CL-307", "Cable de red cat 6\n(5 metros)", 6, 4.85),
        ("CL-308", "Filtro de privacidad\n(14 pulgadas)", 3, 12.35),
        ("CL-309", "Auricular con microfono\n(jack 3.5 mm)", 4, 18.70),
        ("CL-310", "Regleta con proteccion\n(6 tomas)", 2, 24.15),
        ("CL-311", "Alfombrilla de escritorio\n(80 x 40 cm)", 3, 13.40),
    ],
}

FECHAS = {"0310": "03/10/2026", "0320": "12/10/2026", "0330": "21/10/2026"}
PROVEEDOR = {"0310": "Suministros Norte", "0320": "Bazar Electronico", "0330": "Cableado Logistico"}

COL_X = {"ref": 45, "desc": 120, "cant": 340, "precio": 430, "importe": 510}
FILA_H = 21
Y_INICIO = 660


def eur(valor):
    """1.234,56 EUR — el formato que usa cualquiera en Espana."""
    texto = "{:,.2f}".format(valor)
    return texto.replace(",", "X").replace(".", ",").replace("X", ".") + " EUR"


def cabecera(c, num, fecha, con_lineas):
    c.setFont("Helvetica-Bold", 15)
    c.drawString(45, 790, "ALBARAN DE ENTREGA")
    c.setFont("Helvetica", 10)
    c.drawString(45, 770, "Proveedor: %s" % PROVEEDOR[num])
    c.drawString(45, 756, "Numero: %s      Fecha: %s" % (num, fecha))
    c.drawString(45, 742, "Destino: almacen central")
    # cabecera de la tabla
    c.setFont("Helvetica-Bold", 9)
    y = 705
    c.drawString(COL_X["ref"], y, "REF")
    c.drawString(COL_X["desc"], y, "DESCRIPCION")
    c.drawRightString(COL_X["cant"] + 30, y, "CANT")
    c.drawRightString(COL_X["precio"] + 40, y, "PRECIO")
    c.drawRightString(COL_X["importe"] + 45, y, "IMPORTE")
    if con_lineas:
        c.line(45, y - 5, 555, y - 5)


def tabla(c, items, con_lineas, dos_lineas):
    total = 0.0
    y = Y_INICIO
    c.setFont("Helvetica", 9)
    for ref, desc, cant, precio in items:
        importe = round(cant * precio, 2)
        total = round(total + importe, 2)
        alto = FILA_H * 2 if dos_lineas and "\n" in desc else FILA_H
        if con_lineas:
            c.rect(45, y - alto + 5, 510, alto)
        partes = desc.split("\n")
        c.drawString(COL_X["ref"], y, ref)
        for k, parte in enumerate(partes):
            c.drawString(COL_X["desc"], y - k * 11, parte)
        c.drawRightString(COL_X["cant"] + 30, y, str(cant))
        c.drawRightString(COL_X["precio"] + 40, y, eur(precio))
        c.drawRightString(COL_X["importe"] + 45, y, eur(importe))
        y -= alto
    return total, y


def un_albaran(num, con_lineas, dos_lineas):
    ruta = os.path.join(SALIDA, "albaran_%s.pdf" % num)
    c = canvas.Canvas(ruta, pagesize=A4)
    cabecera(c, num, FECHAS[num], con_lineas)
    total, y = tabla(c, ITEMS[num], con_lineas, dos_lineas)
    y -= 12
    if con_lineas:
        c.line(45, y + 12, 555, y + 12)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(390, y, "LINEAS: %d" % len(ITEMS[num]))
    c.drawString(390, y - 16, "TOTAL ALBARAN: %s" % eur(total))
    c.showPage()
    c.save()
    return ruta, len(ITEMS[num]), total


def main():
    os.makedirs(SALIDA, exist_ok=True)
    hechos = [
        un_albaran("0310", con_lineas=True, dos_lineas=False),
        un_albaran("0320", con_lineas=False, dos_lineas=False),
        un_albaran("0330", con_lineas=True, dos_lineas=True),
    ]
    print("albaranes escritos en %s/" % SALIDA)
    suma_lineas = 0
    suma_total = 0.0
    for ruta, lineas, total in hechos:
        print("  %-22s %2d lineas   total %14s" % (os.path.basename(ruta), lineas, eur(total)))
        suma_lineas += lineas
        suma_total = round(suma_total + total, 2)
    print("TOTAL: %d lineas, %d albaranes, %s" % (suma_lineas, len(hechos), eur(suma_total)))


if __name__ == "__main__":
    main()
