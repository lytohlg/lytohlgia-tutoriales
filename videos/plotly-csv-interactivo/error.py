"""El error de verdad: pedir una columna que no existe."""
import pandas as pd
import plotly.express as px

df = pd.read_csv("datos/ventas.csv", sep=";", decimal=",")
fig = px.line(df, x="mes", y="total")
print("dibujado")
