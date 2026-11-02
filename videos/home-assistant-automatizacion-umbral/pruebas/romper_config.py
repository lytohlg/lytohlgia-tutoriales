"""Rompe a propósito la indentación del sensor en config/roto/configuration.yaml.

El corrector de YAML del editor impide escribir un fichero inválido a mano;
este script lo genera en disco para poder demostrar el error de verdad.
Se ejecuta desde la carpeta del material:  python3 pruebas/romper_config.py
"""
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "config" / "roto" / "configuration.yaml"
lineas = p.read_text().splitlines()
salida = []
for linea in lineas:
    if linea.strip().startswith("value_template:"):
        salida.append("       " + linea.strip())   # 7 espacios en vez de 6
    else:
        salida.append(linea)
p.write_text("\n".join(salida) + "\n")
print("roto:", p.name, "-> value_template con 7 espacios")
