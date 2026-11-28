"""El mismo gráfico, creando antes la columna 'mes' que faltaba."""
import os

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/ventas.csv", sep=";", decimal=",")
df["mes"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m")

fig = px.line(df, x="mes", y="total", color="tienda", markers=True,
              title="Facturación por mes y tienda")
fig.update_xaxes(type="category")
os.makedirs("salida", exist_ok=True)
fig.write_html("salida/arreglado.html", include_plotlyjs=True)
print("salida/arreglado.html:", round(os.path.getsize("salida/arreglado.html") / 1024), "KB")
