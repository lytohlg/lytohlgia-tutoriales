"""La misma facturación, mes a mes y con una línea por tienda."""
import os

import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/ventas.csv", sep=";", decimal=",")
df["mes"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m")
por_mes = df.groupby(["mes", "tienda"], as_index=False)["total"].sum()

fig = px.line(por_mes, x="mes", y="total", color="tienda", markers=True,
              title="Facturación por mes y tienda")
fig.update_traces(hovertemplate="%{x} · %{y:,.0f} €<extra></extra>")
fig.update_layout(yaxis_tickformat=",.0f", hovermode="x unified")
fig.update_xaxes(type="category")
os.makedirs("salida", exist_ok=True)
fig.write_html("salida/linea.html", include_plotlyjs=True)

print("puntos dibujados:", len(por_mes))
print("salida/linea.html:", round(os.path.getsize("salida/linea.html") / 1024), "KB")
