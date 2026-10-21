#!/usr/bin/env python3
"""Dónde está el límite: el PDF escaneado.

Si el documento es una foto (un escaneo), el DNI no está en el texto: está
en los píxeles. Aquí se mide qué se puede hacer y qué no, sin adornos.
"""
import hashlib

import fitz

from datos import DNI_A

ORIGEN = "entrada/contrato_alquiler.pdf"

# 1. Convertir la página en una imagen y meterla en un PDF nuevo: eso es un escaneo.
doc = fitz.open(ORIGEN)
pix = doc[0].get_pixmap(dpi=120)
doc.close()

escaneo = fitz.open()
pagina = escaneo.new_page(width=pix.width * 72 / 120, height=pix.height * 72 / 120)
pagina.insert_image(pagina.rect, pixmap=pix)
escaneo.save("escaneo.pdf")
escaneo.close()

# 2. Los patrones, sobre el escaneo: ¿encuentran algo?
doc = fitz.open("escaneo.pdf")
texto = doc[0].get_text()
zonas = doc[0].search_for(DNI_A)
print("escaneo: caracteres de texto = %d | zonas encontradas del DNI = %d"
      % (len(texto.strip()), len(zonas)))
print("=> para el script, este documento no tiene ningún dato personal")
doc.close()

# 3. Y si se tapa a mano: ¿qué pasa con la imagen de dentro?
def huella(pdf):
    doc = fitz.open(pdf)
    xref = doc[0].get_images()[0][0]
    datos = doc.extract_image(xref)["image"]
    doc.close()
    return hashlib.sha256(datos).hexdigest()[:16], len(datos)


doc = fitz.open("escaneo.pdf")
pagina = doc[0]
zona = fitz.Rect(60, 130, 500, 200)          # banda donde está el DNI en la imagen
pagina.add_redact_annot(zona, fill=(0, 0, 0))
pagina.apply_redactions(images=2)            # 2 = borrar los píxeles de la zona
doc.save("escaneo_censurado.pdf", garbage=4, deflate=True)
doc.close()

h1, n1 = huella("escaneo.pdf")
h2, n2 = huella("escaneo_censurado.pdf")
print("imagen incrustada original : sha256 %s  %d bytes" % (h1, n1))
print("imagen incrustada censurada: sha256 %s  %d bytes" % (h2, n2))
print("la imagen de dentro cambió: %s" % ("SI" if h1 != h2 else "NO"))

doc = fitz.open("escaneo_censurado.pdf")
print("texto del escaneo censurado: %d caracteres (sigue sin haber texto)"
      % len(doc[0].get_text().strip()))
doc.close()
