"""Generador del informe de ventas. Sin secretos: esto es el codigo normal."""
import csv
from pathlib import Path

RUTA_VENTAS = Path("ventas.csv")


def leer_ventas(ruta=RUTA_VENTAS):
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def total_por_mes(filas):
    totales = {}
    for fila in filas:
        mes = fila["fecha"][:7]
        totales[mes] = totales.get(mes, 0) + float(fila["importe"])
    return totales


if __name__ == "__main__":
    for mes, total in sorted(total_por_mes(leer_ventas()).items()):
        print(mes, round(total, 2))
