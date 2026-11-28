"""Genera datos/ventas.csv (datos de EJEMPLO, sintéticos) con formato de export de Excel:
separador ';', decimales con coma, importes como texto."""
import csv
import random

random.seed(11)
TIENDAS = ["Centro", "Norte", "Sur"]
PRODUCTOS = ["teclado", "ratón", "monitor"]
PRECIOS = {"teclado": 19.9, "ratón": 9.5, "monitor": 129.0}
filas = []
for tienda in TIENDAS:
    for mes in range(1, 13):
        for prod in PRODUCTOS:
            base = {"Centro": 40, "Norte": 25, "Sur": 18}[tienda]
            unidades = random.randint(base, base + 25)
            precio = PRECIOS[prod]
            total = round(unidades * precio, 2)
            filas.append([
                f"2026-{mes:02d}-01",
                tienda,
                prod,
                str(unidades),
                str(precio).replace(".", ","),
                f"{total:.2f}".replace(".", ","),
            ])

with open("datos/ventas.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["fecha", "tienda", "producto", "unidades", "precio_unitario", "total"])
    w.writerows(filas)
print("filas:", len(filas))
print("suma total:", round(sum(float(r[5].replace(",", ".")) for r in filas), 2))
