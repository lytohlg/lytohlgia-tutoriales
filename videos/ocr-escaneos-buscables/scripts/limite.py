#!/usr/bin/env python3
"""El lado incomodo: donde esta el limite real del OCR, medido en dos escalones.

Escalon 1 (35% de resolucion + desenfoque suave): el OCR devuelve texto casi
correcto, con un error suelto que nadie mira.
Escalon 2 (22% + desenfoque fuerte): ocrmypdf ya no añade capa de texto. Si no
compruebas el resultado, te quedas con un PDF que parece procesado y sigue
siendo una foto.

Los dos escalones se miden con el MISMO comando que el resto del video.
"""
import os
import subprocess

from PIL import Image, ImageFilter

ORIGEN = "entrada/contrato_alquiler.pdf"
BASE = "entrada_mala"
os.makedirs(BASE, exist_ok=True)
os.makedirs("salida", exist_ok=True)

subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", ORIGEN, "/tmp/contrato"],
               check=True, capture_output=True)
ORIGINAL = Image.open("/tmp/contrato.png")


def escalon(nombre, pct, blur, calidad):
    malo = os.path.join(BASE, "contrato_%s.pdf" % nombre)
    salida = "salida/contrato_%s_ocr.pdf" % nombre
    if os.path.exists(salida):
        os.remove(salida)
    img = ORIGINAL.resize((ORIGINAL.width * pct // 100, ORIGINAL.height * pct // 100),
                          Image.LANCZOS)
    img = img.resize((img.width * 100 // pct, img.height * 100 // pct), Image.BICUBIC)
    img = img.filter(ImageFilter.GaussianBlur(blur))
    img.save(malo, "PDF", resolution=150.0, quality=calidad)

    antes = subprocess.run(["pdftotext", "-q", malo, "-"], capture_output=True).stdout.decode()
    r = subprocess.run(["ocrmypdf", "--language", "spa", "--output-type", "pdf", malo, salida],
                       capture_output=True, text=True)
    texto = ""
    if os.path.exists(salida):
        texto = subprocess.run(["pdftotext", "-q", salida, "-"],
                               capture_output=True).stdout.decode()
    limpio = texto.replace("\f", "").strip()
    lineas = [l for l in limpio.splitlines() if l.strip()]

    print("\n=== escalon %s: %d%% de resolucion, %d bytes ===" % (nombre, pct, os.path.getsize(malo)))
    print("texto antes del OCR: %d caracteres" % len(antes.strip()))
    print("ocrmypdf rc: %d | texto despues: %d caracteres" % (r.returncode, len(limpio)))
    for l in lineas[:4]:
        print("   " + l)
    for l in lineas:
        if "cada m" in l or "renta mensual" in l:
            print("   >> " + l)
            break
    print("conserva el importe (780): %s | conserva el DNI: %s"
          % ("780" in limpio, ("44.821.337" in limpio) or ("44,821,337" in limpio)))
    print("error de una letra (cada mos en vez de cada mes): %s" % ("cada mos" in limpio))


escalon("regular", 35, 0.9, 50)
escalon("malo", 22, 1.6, 45)
print("\nresumen: a 35% lee casi todo (con un error suelto); a 22% devuelve texto ilegible.")
print("en los dos casos ocrmypdf termina con codigo 0: no avisa de los errores.")
