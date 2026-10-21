#!/usr/bin/env python3
"""El lote: encuentra los datos personales de una carpeta y los quita.

Uso: python3 lote.py [v1|v2]

Informa DOS cantidades distintas por documento: lo que ha DETECTADO y las
zonas que ha REDACTADO. No son lo mismo, y confundirlas es lo que hace que
un script parezca correcto cuando no lo es.
"""
import os
import sys

import fitz

from patrones import VERSIONES, buscar

VERSION = sys.argv[1] if len(sys.argv) > 1 else "v1"
ENTRADA = "entrada"
SALIDA = "salida_" + VERSION
os.makedirs(SALIDA, exist_ok=True)

print("patrones: %s (%s)" % (VERSION, ", ".join(sorted(VERSIONES[VERSION]))))
print("%-24s %10s %12s" % ("DOCUMENTO", "DETECTADOS", "REDACTADOS"))
print("-" * 50)

total_datos = total_zonas = 0
for f in sorted(x for x in os.listdir(ENTRADA) if x.endswith(".pdf")):
    doc = fitz.open(os.path.join(ENTRADA, f))
    datos = 0
    zonas = 0
    for pagina in doc:
        texto = pagina.get_text()
        for tipo, patron in VERSIONES[VERSION].items():
            for m in patron.finditer(texto):
                datos += 1
                for r in pagina.search_for(m.group(0)):
                    pagina.add_redact_annot(r, fill=(0, 0, 0))
                    zonas += 1
        pagina.apply_redactions()
    doc.save(os.path.join(SALIDA, f), garbage=4, deflate=True)
    doc.close()
    total_datos += datos
    total_zonas += zonas
    print("%-24s %10d %12d" % (f, datos, zonas))

print("-" * 50)
print("datos detectados: %d | zonas redactadas: %d" % (total_datos, total_zonas))
print("salida: %s" % SALIDA)
