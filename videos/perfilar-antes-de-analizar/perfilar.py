#!/usr/bin/env python3
"""Perfila un CSV y deja el informe en HTML más un resumen en JSON."""
import sys
import time

import pandas as pd
from data_profiling import ProfileReport

ruta = sys.argv[1] if len(sys.argv) > 1 else "datos/ventas_2026.csv"
minimo = "--minimo" in sys.argv
salida = "perfil_min.html" if minimo else "perfil.html"
salida_json = "perfil_min.json" if minimo else "perfil.json"

t0 = time.perf_counter()
df = pd.read_csv(ruta, dtype=str)
t1 = time.perf_counter()
informe = ProfileReport(
    df,
    title="Ventas 2026",
    minimal=minimo,
    explorative=False,
    progress_bar=False,
)
t2 = time.perf_counter()
informe.to_file(salida)
with open(salida_json, "w", encoding="utf-8") as f:
    f.write(informe.to_json())
t3 = time.perf_counter()

print(f"leído:      {t1 - t0:5.1f} s   ({len(df)} filas)")
print(f"perfilado:  {t2 - t1:5.1f} s")
print(f"escrito:    {t3 - t2:5.1f} s")
print(f"informe:    {salida}")
print(f"resumen:    {salida_json}")
