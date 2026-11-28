"""El mismo gráfico para tus datos: cambias la columna y la ruta, nada más."""
import argparse
import os

import pandas as pd
import plotly.express as px

p = argparse.ArgumentParser()
p.add_argument("--columna", default="tienda", help="columna por la que agrupar")
p.add_argument("--salida", default="salida/personalizado.html")
a = p.parse_args()

df = pd.read_csv("datos/ventas.csv", sep=";", decimal=",")
datos = df.groupby(a.columna, as_index=False)["total"].sum()

fig = px.bar(datos, x=a.columna, y="total", text_auto=".2s",
             title=f"Facturación por {a.columna}")
fig.update_traces(hovertemplate="%{x}<br>%{y:,.0f} €<extra></extra>")
fig.update_layout(yaxis_tickformat=",.0f")
os.makedirs("salida", exist_ok=True)
fig.write_html(a.salida, include_plotlyjs=True)

print(f"{a.salida}: {len(datos)} barras por {a.columna}")
