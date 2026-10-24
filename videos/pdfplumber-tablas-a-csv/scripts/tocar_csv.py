#!/usr/bin/env python3
"""Cambia UN importe de un CSV, como si alguien lo hubiera tocado a mano en Excel.

Es la prueba negativa del video: el CSV parece correcto, el total ya no cuadra, y la
comprobacion tiene que cazarlo. No toca los PDF: trabaja sobre una copia de la salida.

Uso:
    cp -r salida salida_tocada
    python3 tocar_csv.py salida_tocada/albaran_0310_tabla1.csv
"""
import csv
import sys


def main():
    ruta = sys.argv[1]
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.reader(f, delimiter=";"))
    # fila 0 es la cabecera; se toca el importe de la tercera linea de datos
    antes = filas[3][4]
    filas[3][4] = "%.2f" % (float(antes) - 30.00)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=";").writerows(filas)
    print("importe tocado en %s: %s -> %s" % (ruta, antes, filas[3][4]))


if __name__ == "__main__":
    main()
