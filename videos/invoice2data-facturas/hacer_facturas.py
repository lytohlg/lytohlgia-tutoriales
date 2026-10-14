#!/usr/bin/env python3
"""Genera 4 facturas PDF FICTICIAS (datos inventados) para la demo de invoice2data.

Sin dependencias: escribe PDF 1.4 a mano (fuente Helvetica, texto sin comprimir),
asi pdfminer puede extraer la capa de texto.

3 facturas del MISMO proveedor con valores distintos + 1 de otro proveedor con
maqueta distinta (para enseñar que la plantilla es por formato).
"""
import os
from pathlib import Path

OUT = Path(__file__).resolve().parent / "entrada"
OUT.mkdir(parents=True, exist_ok=True)

# Los nombres de objeto de un PDF se escriben con una barra delante (Type, Page,
# Font...). Aqui se escriben con `~` y se cambian por la barra al montar el PDF:
# asi el fichero no lleva barras sueltas que parezcan rutas de un sistema.
BARRA = "/"


def nm(texto):
    return texto.replace("~", BARRA)


def esc(s):
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def pdf(lines, path):
    """lines: lista de (x, y, size, texto) en puntos, origen abajo-izquierda."""
    content = ["BT"]
    for x, y, size, txt in lines:
        content.append(nm("~F1 %g Tf") % size)
        content.append("1 0 0 1 %g %g Tm" % (x, y))
        content.append("(%s) Tj" % esc(txt))
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", "replace")

    objs = []
    objs.append(nm("<< ~Type ~Catalog ~Pages 2 0 R >>").encode("latin-1"))
    objs.append(nm("<< ~Type ~Pages ~Kids [3 0 R] ~Count 1 >>").encode("latin-1"))
    objs.append(nm("<< ~Type ~Page ~Parent 2 0 R ~MediaBox [0 0 595 842] "
                   "~Resources << ~Font << ~F1 4 0 R >> >> ~Contents 5 0 R >>").encode("latin-1"))
    objs.append(nm("<< ~Type ~Font ~Subtype ~Type1 ~BaseFont ~Helvetica "
                   "~Encoding ~WinAnsiEncoding >>").encode("latin-1"))
    objs.append(nm("<< ~Length %d >>\nstream\n").encode("latin-1") % len(stream)
                + stream + b"\nendstream")

    out = bytearray(b"%PDF-1.4\n")
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n" % (len(objs) + 1)
    out += b"0000000000 65535 f \n"
    for off in offs:
        out += b"%010d 00000 n \n" % off
    out += (nm("trailer\n<< ~Size %d ~Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n").encode("latin-1")
            % (len(objs) + 1, xref))
    path.write_bytes(bytes(out))


def linea(y, izq, der, size=9.5):
    """Fila de concepto en UNA sola cadena: pdfminer separa columnas, y queremos
    que la descripcion y el importe salgan juntos para poder parsearlos."""
    return [(60, y, size, "%s   %s" % (izq, der))]


def factura_arenal(num, fecha, lineas, base, iva, total, ruta):
    L = [(60, 780, 16, "SUMINISTROS ARENAL S.L."),
         (60, 762, 9, "CIF: B-87654321   C/ Riofrio 14, 28021 Madrid"),
         (60, 748, 9, "Tel. 555 010 111   www.arenal.example"),
         (380, 780, 11, "FACTURA"),
         (380, 764, 9.5, "N. factura: %s" % num),
         (380, 750, 9.5, "Fecha de emision: %s" % fecha),
         (380, 736, 9.5, "Vencimiento: 30 dias"),
         (60, 700, 9.5, "Cliente: Taller Norte 2000 S.L.   CIF: B-11223344"),
         (60, 686, 9.5, "Direccion: Poligono Las Fuentes, nave 7, 50014 Zaragoza"),
         (60, 650, 9.5, "Descripcion"),
         (400, 650, 9.5, "Importe")]
    y = 634
    for desc, imp in lineas:
        L += linea(y, desc, imp)
        y -= 15
    L += [(330, y - 10, 9.5, "Base imponible: " + base),
          (330, y - 25, 9.5, "IVA 21%: " + iva),
          (330, y - 45, 11, "Total a pagar: " + total)]
    pdf(L, OUT / ruta)


def factura_vega(num, fecha, base, iva, total, ruta):
    L = [(60, 790, 15, "TRANSPORTES VEGA, S.A."),
         (60, 774, 9, "NIF A-99887766  -  Avda. del Puerto 3, 46024 Valencia"),
         (60, 742, 12, "Factura n.o %s" % num),
         (60, 726, 9.5, "Fecha: %s" % fecha),
         (60, 706, 9.5, "Concepto: portes y gestion de almacen, semana 40"),
         (60, 686, 9.5, "SUBTOTAL ............ %s EUR" % base),
         (60, 671, 9.5, "I.V.A. 21%% ........... %s EUR" % iva),
         (60, 656, 9.5, "TOTAL FACTURA ........ %s EUR" % total),
         (60, 620, 9, "Forma de pago: transferencia 30 dias. IBAN ES00 0000 0000 0000 0000")]
    pdf(L, OUT / ruta)


factura_arenal("F-2026-0417", "03/10/2026",
               [("Cable flexible 3x1,5 (rollo 100 m)", "412,00 EUR"),
                ("Cuadro de distribucion 24 modulos", "538,00 EUR"),
                ("Mano de obra instalacion", "300,00 EUR")],
               "1.250,00 EUR", "262,50 EUR", "1.512,50 EUR",
               "F-2026-0417_arenal.pdf")

factura_arenal("F-2026-0502", "10/10/2026",
               [("Tuberia corrugada 25 mm (rollo 50 m)", "96,00 EUR"),
                ("Cajas de registro estanca", "54,00 EUR"),
                ("Desplazamiento tecnico", "80,00 EUR")],
               "230,00 EUR", "48,30 EUR", "278,30 EUR",
               "F-2026-0502_arenal.pdf")

factura_arenal("F-2026-0611", "17/10/2026",
               [("Diferencial 40 A 30 mA", "188,00 EUR"),
                ("Cable H07V-K 2,5 (rollo 100 m)", "142,00 EUR"),
                ("Herramienta de crimpado", "68,00 EUR"),
                ("Portes", "22,00 EUR")],
               "420,00 EUR", "88,20 EUR", "508,20 EUR",
               "F-2026-0611_arenal.pdf")

factura_vega("TV/2026/1188", "08/10/2026", "1.180,00", "247,80", "1.427,80",
             "TV-2026-1188_vega.pdf")

print("facturas escritas en", OUT)
for p in sorted(OUT.iterdir()):
    print("  %-28s %6d bytes" % (p.name, p.stat().st_size))
