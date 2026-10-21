#!/usr/bin/env python3
"""Un formulario rellenable: los datos están en CAMPOS, no en el texto.

Es el formulario de alta que manda un banco o un seguro: se rellena en el
propio PDF y los valores se guardan en la ficha de cada campo.
"""
import fitz

from datos import CUENTA_B, NOMBRE_A

doc = fitz.open()
page = doc.new_page(width=595, height=842)
page.insert_textbox(fitz.Rect(60, 60, 535, 100), "SOLICITUD DE ALTA DE CUENTA",
                    fontsize=14, fontname="hebo")
page.insert_textbox(fitz.Rect(60, 110, 535, 150),
                    "Rellene los campos y envíe este mismo fichero firmado.",
                    fontsize=10, fontname="helv")

CAMPOS = [
    ("titular", "Nombre del titular", NOMBRE_A, 200),
    ("cuenta", "Cuenta de abono", CUENTA_B, 260),
]

for nombre, etiqueta, valor, y in CAMPOS:
    page.insert_text((60, y), etiqueta + ":", fontsize=10, fontname="helv")
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_name = nombre
    w.field_value = valor
    w.rect = fitz.Rect(200, y - 11, 520, y + 6)
    w.text_fontsize = 9
    page.add_widget(w)

doc.save("formulario.pdf")
doc.close()
print("formulario.pdf creado: %d campos" % len(CAMPOS))
