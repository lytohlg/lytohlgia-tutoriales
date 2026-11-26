"""Lo que un modelo NO hace: mirar la fila de al lado.

Pydantic valida UN registro. El id repetido es un problema del LOTE y hay que
comprobarlo aparte. Este script enseña el límite y la solución mínima.
"""
import csv
from collections import Counter

from normaliza import Pedido
from pydantic import ValidationError

ids = []
for n, fila in enumerate(csv.DictReader(open("datos/pedidos.csv", encoding="utf-8")), start=1):
    try:
        ids.append((n, Pedido.model_validate(fila).id))
    except ValidationError:
        pass  # las filas que no pasan el modelo ya las cuenta modelo.py

cuenta = Counter(i for _, i in ids)
repetidos = {i for i, c in cuenta.items() if c > 1}
print(f"pedidos que pasan el modelo: {len(ids)}")
print(f"ids repetidos en el lote:    {sorted(repetidos) or 'ninguno'}")

vistos = set()
for n, i in ids:
    if i in vistos and i in repetidos:
        print(f"  fila {n}: el id {i} ya había salido antes")
    vistos.add(i)
