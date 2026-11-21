"""Recorre la carpeta de fotos y deja una versión igual para todas.

Qué hace con cada foto:
  1. la abre y le aplica el giro que pide el EXIF (si no, sale de lado),
  2. aplana la transparencia sobre fondo blanco (JPEG no tiene canal alfa),
  3. la recorta a un cuadrado de 1200x1200 sin deformarla,
  4. le pega la marca de agua con transparencia,
  5. la guarda en la carpeta de salida y anota una línea en registro.csv.
Si una foto no se puede abrir, la anota como dañada y SIGUE con la siguiente.

Uso: python lote.py datos/fotos salida [--sin-giro]
"""
import csv
import sys
import time
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

LADO = 1200
CALIDAD = 82
FONDO = (255, 255, 255)
SIN_GIRO = "--sin-giro" in sys.argv


def preparar_marca():
    marca = Image.open("datos/marca.png").convert("RGBA")
    escala = LADO // 6
    return marca.resize((escala, int(escala * marca.height / marca.width)), Image.Resampling.LANCZOS)


def main():
    origen = Path(sys.argv[1] if len(sys.argv) > 1 else "datos/fotos")
    destino = Path(sys.argv[2] if len(sys.argv) > 2 else "salida")
    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.glob("*.jpg"):
        viejo.unlink()

    marca = preparar_marca()
    filas, escritas, danadas, giradas, aplanadas = [], 0, 0, 0, 0
    bytes_in, bytes_out = 0, 0
    t0 = time.time()

    for ruta in sorted(origen.iterdir()):
        if not ruta.is_file():
            continue
        try:
            with Image.open(ruta) as foto:
                bytes_in += ruta.stat().st_size
                if not SIN_GIRO:
                    orientacion = foto.getexif().get(274, 1)
                    if orientacion not in (0, 1):
                        giradas += 1
                    foto = ImageOps.exif_transpose(foto)

                if foto.mode in ("RGBA", "LA", "P"):
                    plano = foto.convert("RGBA")
                    lienzo = Image.new("RGB", plano.size, FONDO)
                    lienzo.paste(plano, mask=plano.getchannel("A"))
                    foto, aplanadas = lienzo, aplanadas + 1
                else:
                    foto = foto.convert("RGB")

                final = ImageOps.fit(foto, (LADO, LADO), method=Image.Resampling.LANCZOS)
                final.paste(marca, (LADO - marca.width - 36, LADO - marca.height - 36), marca)

                salida = destino / f"{ruta.stem.lower().replace(' ', '_')}.jpg"
                final.save(salida, "JPEG", quality=CALIDAD, optimize=True, progressive=True)
        except (UnidentifiedImageError, OSError, ValueError) as error:
            danadas += 1
            filas.append({"origen": ruta.name, "salida": "", "estado": "DANADA",
                          "motivo": type(error).__name__, "ancho": "", "alto": "", "bytes": ""})
            continue

        escritas += 1
        bytes_out += salida.stat().st_size
        filas.append({"origen": ruta.name, "salida": salida.name, "estado": "OK", "motivo": "",
                      "ancho": final.width, "alto": final.height, "bytes": salida.stat().st_size})

    with open(destino.parent / "registro.csv", "w", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=["origen", "salida", "estado", "motivo", "ancho", "alto", "bytes"])
        escritor.writeheader()
        escritor.writerows(filas)

    segundos = time.time() - t0
    print(f"{len(filas)} fotos leídas · {escritas} escritas en {destino}/ · {danadas} dañadas (ver registro.csv)")
    print(f"{giradas} giradas por EXIF corregidas · {aplanadas} con transparencia aplanadas")
    print(f"peso: {bytes_in/1e6:.1f} MB → {bytes_out/1e6:.1f} MB "
          f"({(1 - bytes_out/max(bytes_in,1))*100:.0f}% menos) · tiempo: {segundos:.0f} s")


if __name__ == "__main__":
    main()
