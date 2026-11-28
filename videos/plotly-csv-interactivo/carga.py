"""Lo primero que pasa al abrir el CSV tal cual sale de Excel."""
import pandas as pd

MAL = pd.read_csv("datos/ventas.csv")
print("columnas:", list(MAL.columns))
print("filas:", len(MAL))

BIEN = pd.read_csv("datos/ventas.csv", sep=";", decimal=",")
print()
print("columnas:", list(BIEN.columns))
print(BIEN.head(3).to_string(index=False))
print()
print("total facturado:", round(BIEN["total"].sum(), 2), "euros")
