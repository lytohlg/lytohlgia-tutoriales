"""Marca de agua con transparencia, en PNG con canal alfa.

Uso: python datos/marca.py [datos/marca.png]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ancho, alto = 520, 200
marca = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
d = ImageDraw.Draw(marca)
d.rounded_rectangle([0, 0, ancho - 1, alto - 1], radius=28, fill=(255, 255, 255, 190))
d.rectangle([34, 46, 34 + 96, 46 + 108], fill=(20, 40, 120, 235))
d.rectangle([150, 62, ancho - 30, 92], fill=(20, 40, 120, 235))
d.rectangle([150, 108, ancho - 90, 132], fill=(20, 40, 120, 235))
ruta = Path(sys.argv[1] if len(sys.argv) > 1 else "datos/marca.png")
ruta.parent.mkdir(parents=True, exist_ok=True)
marca.save(ruta)
print(f"marca escrita: {ruta} ({marca.mode} {marca.size[0]}x{marca.size[1]})")
