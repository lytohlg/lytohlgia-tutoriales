#!/usr/bin/env python3
"""LA CENSURA FALSA: tapar con un rectángulo negro.

Dibuja un rectángulo negro encima del DNI y guarda el PDF. Después vuelve a
extraer el texto del fichero guardado: lo que salga demuestra si el dato
estaba tapado o seguía ahí debajo.
"""
import fitz

from datos import DNI_A

ORIGEN = "entrada/contrato_alquiler.pdf"
SALIDA = "censura_falsa.pdf"

doc = fitz.open(ORIGEN)
pagina = doc[0]

# Localiza el DNI en la página y tapa cada aparición con un rectángulo negro.
apariciones = pagina.search_for(DNI_A)
print("apariciones del DNI localizadas en la pagina: %d" % len(apariciones))
for r in apariciones:
    pagina.draw_rect(r, color=(0, 0, 0), fill=(0, 0, 0))

doc.save(SALIDA)
doc.close()
print("guardado %s (%d bytes)" % (SALIDA, __import__("os").path.getsize(SALIDA)))

# Y ahora la prueba: ¿qué texto se puede sacar de ese PDF ya "censurado"?
doc = fitz.open(SALIDA)
texto = doc[0].get_text()
doc.close()

lineas = [l for l in texto.splitlines() if DNI_A in l]
print("-" * 60)
print("veces que el DNI sigue apareciendo en el texto: %d" % len(lineas))
for l in lineas:
    print("  > %s" % l.strip())
