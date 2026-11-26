"""La verdad de los datos: lo que hay dentro de pedidos.csv, sin validar nada.

Se usa para comprobar lo que el validador manual deja pasar y cuánto se separa
el total que él calcula del total real de los pedidos que de verdad son válidos.
"""
import csv

FILAS = []
with open("datos/pedidos.csv", newline="", encoding="utf-8") as fh:
    for n, fila in enumerate(csv.DictReader(fh), start=1):
        FILAS.append((n, fila))

print(f"filas en el CSV: {len(FILAS)}")
for n, f in FILAS:
    print(f"  {n}: id={f['id']:<2} importe={f['importe']!r:<9} fecha={f['fecha']:<11} "
          f"email={f['email']:<18} estado={f['estado']!r}")
