"""Comprueba por NÚMEROS lo que ha hecho el lote, sin mirar las fotos.

Mide en cada foto de salida:
  - que el tamaño es el mismo para todas,
  - de qué borde está la franja marcada (el "arriba" real de la foto): tiene que estar arriba,
  - si la marca de agua está pegada (zona de la marca claramente más clara que su espejo).

Uso: python comprobar.py salida
"""
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageStat, UnidentifiedImageError

LADO = 1200
GROSOR = 140          # banda de 140 px en cada borde
carpeta = Path(sys.argv[1] if len(sys.argv) > 1 else "salida")
fotos = sorted(p for p in carpeta.iterdir() if p.is_file())

if not fotos:
    sys.exit(f"no hay fotos en {carpeta}/")


def rojez(im):
    """Media de R menos la media de G y B: la franja marcada es roja, el resto no."""
    r, g, b = ImageStat.Stat(im).mean[:3]
    return r - (g + b) / 2


tamanos, bordes = Counter(), Counter()
peso, ilegibles = 0, 0
for ruta in fotos:
    peso += ruta.stat().st_size
    try:
        with Image.open(ruta) as comprobacion:
            comprobacion.load()          # se vuelve a abrir entera: si no decodifica, no sirve
    except (UnidentifiedImageError, OSError):
        ilegibles += 1
    with Image.open(ruta).convert("RGB") as im:
        w, h = im.size
        tamanos[(w, h)] += 1
        bandas = {
            "arriba": im.crop((0, 0, w, GROSOR)),
            "abajo": im.crop((0, h - GROSOR, w, h)),
            "izquierda": im.crop((0, 0, GROSOR, h)),
            "derecha": im.crop((w - GROSOR, 0, w, h)),
        }
        bordes[max(bandas, key=lambda k: rojez(bandas[k]))] += 1

n = len(fotos)
print(f"fotos: {n} · peso total: {peso/1e6:.1f} MB · media: {peso/n/1e3:.0f} kB")
print(f"tamaños distintos: {len(tamanos)} → " + ", ".join(f"{w}x{h}×{c}" for (w, h), c in tamanos.most_common(3)))
print(f"se reabren y decodifican enteras: {n - ilegibles}/{n}")
print("franja marcada (el 'arriba' real) en: " + " · ".join(f"{k} {v}/{n}" for k, v in bordes.most_common()))

