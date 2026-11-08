"""Resumen de un CSV de catalogo: filas, titulos distintos y precios."""
import csv
import sys


def resumen(ruta):
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    titulos = {f["titulo"] for f in filas}
    precios = []
    for f in filas:
        try:
            precios.append(float(f["precio"]))
        except ValueError:
            pass
    print(f"{len(filas)} fichas y {len(titulos)} titulos distintos")
    if len(precios) == len(filas):
        media = sum(precios) / len(precios)
        print(f"precio: medio {media:.2f} | mas caro {max(precios)} | mas barato {min(precios)}")
    else:
        print("precio: viene como texto, no se puede calcular (falta el pipeline)")


if __name__ == "__main__":
    resumen(sys.argv[1] if len(sys.argv) > 1 else "catalogo.csv")
