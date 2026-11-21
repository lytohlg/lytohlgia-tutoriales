"""La versión que se escribe en cinco minutos y se rompe en la foto veintisiete.

Uso: python lote_ingenuo.py datos/fotos salida_ingenuo
"""
import sys
from pathlib import Path

from PIL import Image

LADO = 1200
origen = Path(sys.argv[1] if len(sys.argv) > 1 else "datos/fotos")
destino = Path(sys.argv[2] if len(sys.argv) > 2 else "salida_ingenuo")
destino.mkdir(exist_ok=True)

marca = Image.open("datos/marca.png").convert("RGBA").resize((200, 77))
hechas = 0
for ruta in sorted(origen.iterdir()):
    if not ruta.is_file():
        continue
    foto = Image.open(ruta)                      # sin giro, sin transparencia, sin red
    final = foto.resize((LADO, LADO))             # y encima deforma
    final.paste(marca, (LADO - 236, LADO - 113), marca)
    final.save(destino / f"{ruta.stem.lower().replace(' ', '_')}.jpg", "JPEG", quality=82)
    hechas += 1

print(f"{hechas} fotos convertidas")
