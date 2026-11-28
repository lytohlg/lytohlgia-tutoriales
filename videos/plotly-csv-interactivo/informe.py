"""Un solo HTML con los dos gráficos: barras por tienda y línea por mes."""
import os

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

df = pd.read_csv("datos/ventas.csv", sep=";", decimal=",")
df["mes"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m")
por_tienda = df.groupby("tienda", as_index=False)["total"].sum()
por_mes = df.groupby("mes", as_index=False)["total"].sum()

barras = px.bar(por_tienda, x="tienda", y="total")
linea = px.line(por_mes, x="mes", y="total", markers=True)
for traza in barras.data:
    traza.hovertemplate = "%{x}<br>%{y:,.0f} €<extra></extra>"
for traza in linea.data:
    traza.hovertemplate = "%{x} · %{y:,.0f} €<extra></extra>"

fig = make_subplots(rows=1, cols=2, subplot_titles=("Por tienda", "Por mes"))
for traza in barras.data:
    fig.add_trace(traza, row=1, col=1)
for traza in linea.data:
    fig.add_trace(traza, row=1, col=2)
fig.update_layout(title="Informe de ventas 2026", height=520,
                  showlegend=False)
fig.update_yaxes(tickformat=",.0f")
fig.update_xaxes(type="category")

os.makedirs("salida", exist_ok=True)
ruta = "salida/informe.html"
fig.write_html(ruta, include_plotlyjs=True)
print(ruta, "->", round(os.path.getsize(ruta) / 1024), "KB")
print("trazas dentro:", len(fig.data))
