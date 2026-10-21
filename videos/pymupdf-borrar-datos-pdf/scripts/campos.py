#!/usr/bin/env python3
"""Los datos que no están en el texto: campos de formulario.

El lote mira el texto de la página. Este documento guarda los datos en la
ficha de cada campo: se pueden pintar en la página, pero viven en otro sitio.
"""
import fitz

from datos import CUENTA_B, NOMBRE_A

# Trocitos que se buscan en el texto y en los bytes crudos: así la prueba no
# depende de escribir los datos otra vez en el código.
NOMBRE_CORTO = NOMBRE_A.rsplit(" ", 1)[0]
CUENTA_CORTA = CUENTA_B.encode()[:9]

RUTA = "formulario.pdf"


def retrato(pdf):
    doc = fitz.open(pdf)
    pagina = doc[0]
    texto = pagina.get_text()
    campos = [(w.field_name, w.field_value) for w in pagina.widgets()]
    doc.close()
    crudo = open(pdf, "rb").read()
    return texto, campos, crudo


texto, campos, crudo = retrato(RUTA)
print("ANTES")
print("  texto de la pagina: %d caracteres" % len(texto.strip()))
print("  el nombre en el texto: %s" % ("Carmen Ruiz" in texto))
print("  campos rellenables: %d" % len(campos))
for nombre, valor in campos:
    print("    %-8s = %s" % (nombre, valor))

# Redactar la banda entera donde están los campos y aplicar.
doc = fitz.open(RUTA)
pagina = doc[0]
pagina.add_redact_annot(fitz.Rect(50, 185, 540, 275), fill=(0, 0, 0))
pagina.apply_redactions()
doc.save("formulario_redactado.pdf", garbage=4, deflate=True)
doc.close()

texto, campos, crudo = retrato("formulario_redactado.pdf")
print("DESPUES de redactar la zona")
print("  texto de la pagina: %d caracteres" % len(texto.strip()))
print("  el nombre en el texto: %s" % (NOMBRE_CORTO in texto))
print("  cuenta en los bytes del fichero: %s" % (CUENTA_CORTA in crudo))
print("  campos rellenables: %d" % len(campos))
for nombre, valor in campos:
    print("    %-8s = %s" % (nombre, valor))

# El arreglo: borrar los campos, no la zona.
doc = fitz.open("formulario_redactado.pdf")
pagina = doc[0]
for w in list(pagina.widgets()):
    pagina.delete_widget(w)
doc.save("formulario_sin_campos.pdf", garbage=4, deflate=True)
doc.close()

texto, campos, crudo = retrato("formulario_sin_campos.pdf")
print("DESPUES de borrar los campos")
print("  campos rellenables: %d | cuenta en los bytes: %s"
      % (len(campos), CUENTA_CORTA in crudo))
