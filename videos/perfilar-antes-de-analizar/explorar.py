#!/usr/bin/env python3
"""Lo que te dice un vistazo rápido con pandas... y lo que NO te dice.

No es una crítica a pandas: es el punto de partida realista. Abres el fichero,
miras la forma y los tipos, y crees que ya sabes lo que hay.
"""
import sys

import pandas as pd

ruta = sys.argv[1] if len(sys.argv) > 1 else "datos/ventas_2026.csv"
df = pd.read_csv(ruta, dtype=str)

print(f"filas: {len(df)}   columnas: {len(df.columns)}")
print("\ntipos que ve pandas:")
for col, t in df.dtypes.items():
    print(f"  {col:10s} {t}")
print(f"\nvalores vacíos en total: {int(df.isna().sum().sum())}")
print("\nY hasta aquí llega el vistazo. Estas tres preguntas siguen sin respuesta:")
print("  1. de esos huecos, ¿cuántos son de cada columna?")
print("  2. la columna fecha es texto: ¿cuántos formatos distintos hay dentro?")
print("  3. ¿cuántas filas están repetidas enteras?")
print("\nResponderlas a mano es un script por pregunta, y cada pregunta nueva es otro script.")
