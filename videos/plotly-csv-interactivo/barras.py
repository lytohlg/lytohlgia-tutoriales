"""Un gráfico de barras por tienda, en un fichero HTML que se abre en el navegador."""
import os

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/ventas.csv", sep=";", decimal=",")
por_tienda = df.groupby("tienda", as_index=False)["total"].sum()

fig = px.bar(por_tienda, x="tienda", y="total", text_auto=".2s",
             title="Facturación por tienda (2026)")
fig.update_traces(hovertemplate="%{x}<br>%{y:,.0f} €<extra></extra>")
fig.update_layout(yaxis_tickformat=",.0f")
os.makedirs("salida", exist_ok=True)
fig.write_html("salida/barras.html", include_plotlyjs=True)

print(por_tienda.to_string(index=False))
print("salida/barras.html:", round(os.path.getsize("salida/barras.html") / 1024), "KB")
