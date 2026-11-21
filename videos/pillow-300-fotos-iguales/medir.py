"""Radiografía de la carpeta que llega: qué variedad trae y qué tiene roto.

Uso: python medir.py datos/fotos
"""
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, UnidentifiedImageError

carpeta = Path(sys.argv[1] if len(sys.argv) > 1 else "datos/fotos")
tamanos, formatos, giradas, danadas = Counter(), Counter(), 0, 0
total = 0
for ruta in sorted(carpeta.iterdir()):
    if not ruta.is_file():
        continue
    total += 1
    try:
        with Image.open(ruta) as im:
            im.load()
            tamanos[im.size] += 1
            formatos[im.format] += 1
            if im.getexif().get(274, 1) not in (0, 1):
                giradas += 1
    except (UnidentifiedImageError, OSError):
        danadas += 1
        formatos["ILEGIBLE"] += 1

peso = sum(r.stat().st_size for r in carpeta.iterdir() if r.is_file()) / 1e6
print(f"ficheros: {total} · peso: {peso:.1f} MB")
print(f"tamaños distintos: {len(tamanos)} → " + ", ".join(f"{w}x{h}×{n}" for (w, h), n in tamanos.most_common(4)) + " …")
print("formatos: " + ", ".join(f"{f}×{n}" for f, n in formatos.most_common()))
print(f"con EXIF de giro (hay que rotarlas): {giradas}")
print(f"ilegibles o truncadas: {danadas}")
