"""Genera la carpeta que llega del proveedor: 300 fotos desordenadas y con defectos CONTADOS.

Determinista (seed fija): el número de fotos giradas, con transparencia y dañadas es siempre el mismo,
así que cualquier comprobación que se imprima después es reproducible.

Uso: python datos/generar_fotos.py datos/fotos [N=300]
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

SEED = 7
TAMANOS = [(1600, 1200), (1200, 1600), (1920, 1080), (1080, 1920), (2048, 1536), (1536, 2048),
           (2400, 1600), (1600, 2400), (1800, 1200), (1200, 1800), (3000, 2000), (2000, 3000),
           (1400, 1050), (1050, 1400), (2600, 1733), (1280, 960)]
NOMBRES = ["IMG_{n:04d}.JPG", "DSC_{n:04d}.jpeg", "foto ({n}).jpg", "captura {n:03d}.PNG",
           "proveedor_webp_{n:03d}.webp", "producto-{n:03d}.jpg", "PXL_2026{n:04d}.JPG",
           "sin_nombre_{n}.jpg", "Foto Final ({n}).jpeg", "IMG-{n:04d}.jpg"]


def foto_sintetica(rnd, w, h):
    """Una imagen con contenido y una FRANJA MARCADA en el borde superior real."""
    img = Image.new("RGB", (w, h), tuple(rnd.randint(30, 90) for _ in range(3)))
    d = ImageDraw.Draw(img)
    for _ in range(6):
        x0, y0 = rnd.randint(0, w - 1), rnd.randint(0, h - 1)
        x1, y1 = x0 + rnd.randint(w // 20, w // 3), y0 + rnd.randint(h // 20, h // 3)
        d.rectangle([x0, y0, min(x1, w - 1), min(y1, h - 1)],
                    fill=tuple(rnd.randint(40, 200) for _ in range(3)))
    # Textura: sin grano, una foto sintética de rectángulos planos comprime de forma irreal y las
    # cifras de peso/calidad no se parecen a las de una foto de verdad.
    ruido = Image.effect_noise((w, h), 32).convert("RGB")
    img = Image.blend(img, ruido, 0.13)
    d = ImageDraw.Draw(img)   # OJO: Image.blend devuelve una imagen NUEVA; hay que redibujar sobre ella
    # marcador de "arriba": franja roja del 24% del alto. Rojo = canal R alto y G/B bajos.
    # Gruesa a propósito: al recortar a cuadrado se pierde una franja de los bordes y la marca
    # tiene que sobrevivir al recorte para poder medirla después.
    d.rectangle([0, 0, w - 1, max(8, int(h * 0.24))], fill=(235, 25, 25))
    return img


def main():
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else "datos/fotos")
    n_total = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rnd = random.Random(SEED)
    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.iterdir():
        viejo.unlink()

    indices = list(range(n_total))
    rotadas = set(rnd.sample(indices, 41))
    resto = sorted(set(indices) - rotadas)
    con_alfa = set(rnd.sample(resto, 20))
    resto2 = sorted(set(resto) - con_alfa)
    webp = set(rnd.sample(resto2, 20))
    # Las dañadas salen del grupo JPEG normal: así 41 giradas y 2 dañadas no se solapan y los
    # recuentos que se imprimen después cuadran sin explicaciones.
    resto3 = sorted(set(resto2) - webp)
    danadas = set(rnd.sample(resto3, 2))

    for i in indices:
        w, h = TAMANOS[i % len(TAMANOS)]
        plantilla = NOMBRES[i % len(NOMBRES)]
        nombre = plantilla.format(n=i + 1)
        ruta = destino / nombre
        base = foto_sintetica(rnd, w, h)

        if i in rotadas:
            # Guardada "de lado": lo que se ve bien exige girar 90° en sentido horario
            # (EXIF Orientation=6). La franja marcada queda en el borde IZQUIERDO de los píxeles.
            guardada = base.transpose(Image.Transpose.ROTATE_90)
            exif = Image.Exif()
            exif[274] = 6
            guardada.save(ruta, "JPEG", quality=88, exif=exif)
        elif i in con_alfa:
            rgba = base.convert("RGBA")
            alfa = Image.new("L", rgba.size, 255)
            ImageDraw.Draw(alfa).rectangle([0, int(rgba.height * 0.55), rgba.width, rgba.height], fill=0)
            rgba.putalpha(alfa)
            ruta = ruta.with_suffix(".PNG")
            rgba.save(ruta, "PNG")
        elif i in webp:
            ruta = ruta.with_suffix(".webp")
            base.save(ruta, "WEBP", quality=85)
        else:
            base.save(ruta, "JPEG", quality=88)

        if i in danadas:
            # Corte a mitad de fichero: el decodificador no puede completar la imagen.
            crudo = ruta.read_bytes()
            ruta.write_bytes(crudo[: int(len(crudo) * 0.35)])

    print(f"fotos escritas: {n_total} en {destino}")
    print(f"  giradas por EXIF (Orientation=6): {len(rotadas)}")
    print(f"  con transparencia (PNG con alfa): {len(con_alfa)}")
    print(f"  en webp: {len(webp)}")
    print(f"  truncadas a propósito: {len(danadas)}")


if __name__ == "__main__":
    main()
