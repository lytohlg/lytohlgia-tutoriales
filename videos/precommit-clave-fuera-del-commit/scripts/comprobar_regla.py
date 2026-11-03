"""Hook propio: falla si la documentacion deja un PENDIENTE sin resolver.

pre-commit le pasa como argumentos los ficheros que ha seleccionado (types: [markdown]).
Codigo de salida distinto de cero = el commit se para.
"""
import sys
from pathlib import Path

MARCADOR = "PENDIENTE"
problemas = []

for ruta in sys.argv[1:]:
    texto = Path(ruta).read_text(encoding="utf-8", errors="replace")
    for numero, linea in enumerate(texto.splitlines(), 1):
        if MARCADOR in linea:
            problemas.append(f"{ruta}:{numero}: {linea.strip()}")

if problemas:
    print("Documentacion a medias:")
    for problema in problemas:
        print("  " + problema)
    sys.exit(1)

print("Documentacion sin pendientes.")
