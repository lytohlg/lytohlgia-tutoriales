#!/usr/bin/env python3
"""Verifica el RESULTADO de la demo, no solo que el proceso terminara sin excepción.

Comprueba que el informe contiene exactamente lo que se esperaba encontrar en el sitio de
prueba. Si falta algo, sale con error: la demo no se da por buena.
"""
import pathlib
import sys

base = pathlib.Path(sys.argv[1])
for nombre in ("intel.txt", "endpoints.txt", "keys.txt"):
    if not (base / nombre).exists():
        sys.exit(f"FALLO: no existe {nombre}")

intel = (base / "intel.txt").read_text(encoding="utf-8")
endpoints = (base / "endpoints.txt").read_text(encoding="utf-8")
keys = (base / "keys.txt").read_text(encoding="utf-8")

esperados = [
    "laura.mendez@example.com",
    "presupuestos@example.com",
    "jorge.puente@example.com",
    "admin@example.com",
    "contacto.backup@example.com",
]
faltan = [e for e in esperados if e not in intel]
if faltan:
    sys.exit(f"FALLO: correos no encontrados: {faltan}")
if "clientes" not in endpoints:
    sys.exit("FALLO: el endpoint del JS no se extrajo")
if "c9K2mQ4tR7yX1zVb3Nw9Hp5L" not in keys:
    sys.exit("FALLO: la cadena de alta entropía no se extrajo")

print("OK: 5/5 correos, endpoint del JS y la cadena de alta entropía")
