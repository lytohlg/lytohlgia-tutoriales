#!/usr/bin/env python3
"""Umbral: usar el perfil dentro de un script, sin nadie mirando.

Devuelve código de salida 1 si alguna columna pasa del umbral de huecos.
Así el control de calidad de un fichero entra en un cron o en un CI.

Ojo: `p_missing` viene como fracción (0.0199 = 1,99%), no como porcentaje.
"""
import json
import sys

ruta = sys.argv[1] if len(sys.argv) > 1 else "perfil.json"
umbral = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
js = json.load(open(ruta, encoding="utf-8"))

malas = []
for col, v in (js.get("variables") or {}).items():
    p = float(v.get("p_missing") or 0.0)
    pct = p * 100 if p <= 1 else p
    if pct > umbral:
        malas.append((col, pct))

print(f"umbral de huecos: {umbral}%   columnas por encima: {len(malas)}")
for col, pct in sorted(malas, key=lambda x: -x[1]):
    print(f"  {col:10s} {pct:.2f}%")
sys.exit(1 if malas else 0)
