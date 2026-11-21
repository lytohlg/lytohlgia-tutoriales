"""Prueba A/B de la marca de agua: misma foto, una salida con marca y otra sin marca.

No se juzga "mirando": se cuentan los píxeles distintos entre las dos salidas y se comprueba que
TODOS caen dentro del rectángulo donde se pegó la marca.

Uso: python verificar_marca.py datos/fotos/IMG_0001.JPG
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

LADO = 1200
ruta = Path(sys.argv[1] if len(sys.argv) > 1 else sorted(Path("datos/fotos").iterdir())[0])
marca = Image.open("datos/marca.png").convert("RGBA")
marca = marca.resize((LADO // 6, int((LADO // 6) * marca.height / marca.width)), Image.Resampling.LANCZOS)
posicion = (LADO - marca.width - 36, LADO - marca.height - 36)

base = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
base = ImageOps.fit(base, (LADO, LADO), method=Image.Resampling.LANCZOS)

sin_marca = base.copy()
con_marca = base.copy()
con_marca.paste(marca, posicion, marca)

dif = ImageChops.difference(sin_marca, con_marca).convert("L")
cambiados = sum(1 for v in dif.getdata() if v)
caja = dif.getbbox()

esperado = (posicion[0], posicion[1], posicion[0] + marca.width, posicion[1] + marca.height)
print(f"foto: {ruta.name}")
print(f"marca pegada en {posicion} ({marca.width}x{marca.height} px)")
print(f"píxeles cambiados: {cambiados} · zona afectada: {caja}")
print(f"zona dentro del rectángulo esperado: {caja[0] >= esperado[0] and caja[1] >= esperado[1] and caja[2] <= esperado[2] and caja[3] <= esperado[3]}")
