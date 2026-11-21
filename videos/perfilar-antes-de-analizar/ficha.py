#!/usr/bin/env python3
"""Ficha de una columna concreta, leída del resumen JSON del perfil."""
import json
import sys

ruta = sys.argv[1] if len(sys.argv) > 1 else "perfil.json"
col = sys.argv[2] if len(sys.argv) > 2 else "importe"
js = json.load(open(ruta, encoding="utf-8"))

v = (js.get("variables") or {}).get(col)
if not v:
    print(f"no hay columna {col!r} en el informe")
    sys.exit(1)

print(f"columna {col}   (tipo detectado: {v.get('type')})")
for clave, etiqueta in (
    ("n", "valores"),
    ("n_missing", "huecos"),
    ("p_missing", "proporción de huecos"),
    ("n_distinct", "valores distintos"),
    ("n_zeros", "ceros"),
    ("n_negative", "negativos"),
    ("min", "mínimo"),
    ("max", "máximo"),
    ("mean", "media"),
):
    if clave in v:
        val = v[clave]
        if isinstance(val, float):
            val = f"{val:.4g}"
        print(f"  {etiqueta:22s} {val}")

dist = v.get("value_counts_without_nan") or {}
if dist:
    top = sorted(dist.items(), key=lambda kv: -kv[1])[:5]
    print("  más repetidos:")
    for k, n in top:
        print(f"    {k!r:14s} {n}")
