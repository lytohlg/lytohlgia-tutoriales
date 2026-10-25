"""Control de repetidos: guarda una huella del informe aceptado y la compara.

Content-Length te dice si el fichero llego entero. No te dice si es EL MISMO
fichero de ayer: si el proveedor repite, los bytes cuadran igual. Con la huella
y la fecha se detecta en el acto.
"""
import hashlib
import os
import sys

fichero = sys.argv[1] if len(sys.argv) > 1 else "descargas/informe.csv"
marca = fichero + ".huella"
hoy = "2026-10-19"

with open(fichero, "rb") as f:
    huella = hashlib.sha256(f.read()).hexdigest()[:16]
lineas = sum(1 for _ in open(fichero, encoding="utf-8"))

if not os.path.exists(marca):
    with open(marca, "w") as f:
        f.write(f"{huella} {hoy}\n")
    print(f"huella nueva  sha256 {huella}  {lineas} lineas -> se archiva")
else:
    anterior, fecha = open(marca).read().split()
    if anterior == huella:
        print(f"MISMO fichero que el {fecha}  (sha256 {huella})")
        print("no se vuelve a archivar: el proveedor no ha actualizado nada")
    else:
        with open(marca, "w") as f:
            f.write(f"{huella} {hoy}\n")
        print(f"huella distinta: antes {anterior} ({fecha}), ahora {huella}")
        print("se archiva la version nueva")
