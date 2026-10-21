#!/usr/bin/env python3
"""LA CENSURA REAL: quitar el dato, no taparlo.

Misma zona, mismo DNI, pero con la API de redacción de PyMuPDF: se marca la
zona con add_redact_annot y se aplica con apply_redactions. El contenido de
esa zona se elimina del documento; no se dibuja nada encima.
"""
import os

import fitz

from datos import DNI_A

ORIGEN = "entrada/contrato_alquiler.pdf"
SALIDA = "censura_real.pdf"

doc = fitz.open(ORIGEN)
pagina = doc[0]

zonas = pagina.search_for(DNI_A)
print("zonas marcadas para redactar: %d" % len(zonas))
for r in zonas:
    pagina.add_redact_annot(r, fill=(0, 0, 0))

pagina.apply_redactions()
doc.save(SALIDA, garbage=4, deflate=True)
doc.close()

# 1. ¿Sigue el texto?
doc = fitz.open(SALIDA)
pagina = doc[0]
texto = pagina.get_text()
lineas = [l for l in texto.splitlines() if DNI_A in l]
print("-" * 62)
print("veces que el DNI aparece en el texto guardado: %d" % len(lineas))
for l in lineas:
    print("  > %s" % l.strip())

# 2. ¿Se ve algo al mirar la zona de cerca?
zona = zonas[0]
pm = pagina.get_pixmap(clip=zona, dpi=150)
claros = sum(1 for y in range(pm.height) for x in range(pm.width)
             if min(pm.pixel(x, y)[:3]) > 200)
print("píxeles claros dentro de la zona redactada: %d de %d"
      % (claros, pm.width * pm.height))
doc.close()

print("bytes del fichero: %d" % os.path.getsize(SALIDA))
