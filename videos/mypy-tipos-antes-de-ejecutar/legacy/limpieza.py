"""Limpieza de ficheros: código viejo, sin una sola anotación de tipo."""
import csv
import os


def leer_ventas(ruta):
    with open(ruta, newline="") as f:
        return [fila["importe"] for fila in csv.DictReader(f)]


def sumar(valores):
    total = 0
    for v in valores:
        total = total + float(v)
    return total


def main():
    aqui = os.path.dirname(os.path.abspath(__file__))
    ventas = leer_ventas(os.path.join(aqui, "ventas.csv"))
    print("Filas:", len(ventas), "Total:", sumar(ventas))


main()
