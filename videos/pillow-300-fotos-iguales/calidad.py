"""Cuánto pesa y cuánto se pierde según la calidad del JPEG.

Misma foto, tres calidades. Se mide lo que ocupa y la diferencia media por canal frente a la
imagen de referencia sin comprimir (0 = idéntica, 255 = otra cosa).

Uso: python calidad.py datos/fotos/IMG_0001.JPG
"""
import io
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageOps, ImageStat

LADO = 1200
ruta = Path(sys.argv[1] if len(sys.argv) > 1 else sorted(Path("datos/fotos").glob("*.JPG"))[0])
referencia = ImageOps.fit(ImageOps.exif_transpose(Image.open(ruta)).convert("RGB"), (LADO, LADO),
                          method=Image.Resampling.LANCZOS)

print(f"referencia: {LADO}x{LADO} sin comprimir ({(LADO * LADO * 3) / 1e6:.1f} MB en memoria)")
for calidad in (70, 82, 95):
    buffer = io.BytesIO()
    referencia.save(buffer, "JPEG", quality=calidad, optimize=True, progressive=True)
    crudo = buffer.getvalue()
    vuelta = Image.open(io.BytesIO(crudo)).convert("RGB")
    diferencia = ImageStat.Stat(ImageChops.difference(referencia, vuelta)).mean
    media = sum(diferencia) / len(diferencia)
    print(f"calidad {calidad}: {len(crudo)/1024:6.0f} kB · diferencia media {media:.2f} de 255")
