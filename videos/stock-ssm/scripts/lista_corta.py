"""Lista corta del stock: lee la respuesta JSON de la API y la imprime en una línea por artículo.

    curl ... | python3 scripts/lista_corta.py

Sin argumentos: muestra los artículos con menos de 15 unidades (los que están cerca de la raya).
Con `--todos`: los muestra todos.
"""

import json
import sys

LIMITE = 15
datos = json.load(sys.stdin)
todos = "--todos" in sys.argv
filas = sorted(datos.get("results", []), key=lambda fila: fila["sku"])

for fila in filas:
    if todos or fila["quantity"] < LIMITE:
        print(f'{fila["sku"]:>9} {fila["quantity"]:>4} unidades  {fila["description"]}')
print(f'({len(filas)} articulos, pagina {datos.get("current_page")} de {datos.get("total_pages")})')
