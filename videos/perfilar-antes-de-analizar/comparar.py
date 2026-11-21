#!/usr/bin/env python3
"""Cierra el círculo: lo que YO metí en el fichero contra lo que el perfil encontró.

El generador dejó manifest.json con los defectos contados. El perfilador no ha
visto ese fichero: solo el CSV. Si los números coinciden, el perfil sirve.
"""
import json
import sys

ruta_perfil = sys.argv[1] if len(sys.argv) > 1 else "perfil.json"
man = json.load(open("datos/manifest.json", encoding="utf-8"))["defectos_inyectados"]
js = json.load(open(ruta_perfil, encoding="utf-8"))
v = js.get("variables") or {}
tab = js.get("table") or {}


def missing(col):
    return (v.get(col) or {}).get("n_missing")


filas = [
    ("huecos en importe", man["importe_vacio"], missing("importe")),
    ("huecos en cliente", man["cliente_vacio"], missing("cliente")),
    ("huecos en fecha", man["fecha_vacia"], missing("fecha")),
    ("filas duplicadas enteras", man["filas_duplicadas_enteras"], tab.get("n_duplicates")),
    ("importes negativos (abonos)", man["importes_negativos_legitimos"], (v.get("importe") or {}).get("n_negative")),
]

print(f"{'defecto':32s} {'metido':>8s} {'detectado':>10s}   {'coincide':>8s}")
for nombre, metido, detectado in filas:
    ok = "sí" if detectado == metido else "NO"
    print(f"{nombre:32s} {metido:8d} {str(detectado):>10s}   {ok:>8s}")
