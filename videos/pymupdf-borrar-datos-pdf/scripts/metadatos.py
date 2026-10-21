#!/usr/bin/env python3
"""Los metadatos: lo que el documento cuenta de ti sin que se vea.

Autor, programa que lo creó, fechas. No está en la página: está en la ficha
del fichero, y viaja con él cuando lo mandas.
"""
import fitz

ORIGEN = "salida_v2/contrato_alquiler.pdf"
SALIDA = "contrato_limpio.pdf"

doc = fitz.open(ORIGEN)
print("metadatos ANTES de limpiar:")
for k, v in doc.metadata.items():
    if v:
        print("  %-14s %s" % (k, v))

doc.set_metadata({})
doc.del_xml_metadata()
doc.save(SALIDA, garbage=4, deflate=True)
doc.close()

doc = fitz.open(SALIDA)
print("metadatos DESPUÉS:")
IGNORAR = {"format", "encryption"}          # no son datos del documento
quedan = [(k, v) for k, v in doc.metadata.items() if v and k not in IGNORAR]
for k, v in doc.metadata.items():
    print("  %-14s %s" % (k, v or "(vacío)"))
doc.close()
print("campos con datos del autor que quedan: %d" % len(quedan))
