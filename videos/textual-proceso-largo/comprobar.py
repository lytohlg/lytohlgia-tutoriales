#!/usr/bin/env python3
"""Comprueba que la demo dejó lo que promete el material. Sale 0 solo si todo cuadra."""
import json
import sys
from pathlib import Path

lote = Path("lote")
salida = Path("salida")

csvs = sorted(lote.glob("*.csv"))
jsons = sorted(salida.glob("*.json"))
f041 = (lote / "extracto_041.csv").read_text()

problemas = []
if len(csvs) != 240:
    problemas.append(f"se esperaban 240 CSV en lote/ y hay {len(csvs)}")
# 238: los dos que siguen rotos (118 y 203) no producen JSON
if len(jsons) != 238:
    problemas.append(f"se esperaban 238 JSON en salida/ y hay {len(jsons)}")
if "842.90" not in f041:
    problemas.append("el importe de extracto_041.csv no se corrigió (sigue sin 842.90)")
if "842,90 EUR" in f041:
    problemas.append("extracto_041.csv sigue con el importe mal escrito")

muestra = json.loads((salida / "extracto_001.json").read_text())
for clave in ("fichero", "filas", "total"):
    if clave not in muestra:
        problemas.append(f"el JSON de salida no trae '{clave}'")
if muestra.get("fichero") != "extracto_001.csv":
    problemas.append(f"el JSON no apunta a su fichero: {muestra.get('fichero')}")

# los dos rotos siguen sin JSON: el proceso no los inventó ni los saltó en silencio
for roto in ("extracto_118", "extracto_203"):
    if (salida / f"{roto}.json").exists():
        problemas.append(f"{roto} no se pudo procesar y sin embargo hay JSON")

if problemas:
    print("✘ " + " · ".join(problemas))
    sys.exit(1)

print(f"VERIFICADO: 240 ficheros generados · {len(jsons)} JSON · 2 fallos a la vista "
      f"({', '.join(p.name for p in sorted(salida.glob('*.json'))[:1])} …)")
