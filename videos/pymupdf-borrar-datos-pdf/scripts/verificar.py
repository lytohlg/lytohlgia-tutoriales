#!/usr/bin/env python3
"""La verificación que NO depende del script que redactó.

Abre los PDF de salida, saca su texto y busca una lista cerrada de secretos
conocidos (los que se sembraron en datos_conocidos.txt). También mira los
bytes en crudo del fichero. Si algo sobrevive, sale aquí.

Uso: python3 verificar.py <carpeta>
"""
import os
import sys

import fitz

CARPETA = sys.argv[1] if len(sys.argv) > 1 else "salida_v1"
CONOCIDOS = [l.strip() for l in open("datos_conocidos.txt") if l.strip()]

print("secretos conocidos a buscar: %d" % len(CONOCIDOS))
print("carpeta verificada: %s" % CARPETA)
print("-" * 66)

total_fugas = 0
for f in sorted(x for x in os.listdir(CARPETA) if x.endswith(".pdf")):
    ruta = os.path.join(CARPETA, f)
    doc = fitz.open(ruta)
    texto = "\n".join(p.get_text() for p in doc)
    doc.close()
    crudo = open(ruta, "rb").read()
    fugas = []
    for s in CONOCIDOS:
        if s in texto or s.encode() in crudo:
            fugas.append(s)
    total_fugas += len(fugas)
    print("%-24s fugas: %d %s" % (f, len(fugas), " ".join(fugas)))

print("-" * 66)
print("TOTAL de secretos que siguen en los documentos: %d" % total_fugas)
