#!/usr/bin/env python3
"""La fecha, en manos de quien la lee: día primero o mes primero.

El fichero mezcla tres formatos. Cuando la fecha se interpreta sola, el lector
tiene que ADIVINAR el orden, y adivinar aquí cuesta un dato mal puesto que no
protesta. Se comparan las dos lecturas posibles del MISMO fichero.
"""
import sys

import pandas as pd

ruta = sys.argv[1] if len(sys.argv) > 1 else "datos/ventas_2026.csv"
df = pd.read_csv(ruta, dtype=str)

mes_primero = pd.to_datetime(df["fecha"], format="mixed", dayfirst=False, errors="coerce")
dia_primero = pd.to_datetime(df["fecha"], format="mixed", dayfirst=True, errors="coerce")

distintas = int((mes_primero != dia_primero).sum())
print(f"filas que cambian según cómo se lea: {distintas} de {len(df)}")
print(f"  mes/día (por defecto):  mínimo {mes_primero.min()}   máximo {mes_primero.max()}")
print(f"  día/mes:                mínimo {dia_primero.min()}   máximo {dia_primero.max()}")
print(f"  filas que no se pueden leer de ninguna forma: {int(mes_primero.isna().sum() - df['fecha'].isna().sum())}")
