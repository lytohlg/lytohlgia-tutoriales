#!/usr/bin/env python3
"""Aplica los tres arreglos de compatibilidad con Python 3 y enseña el antes/después.

Se hace con reemplazos exactos (no con un parche de texto) para que el resultado sea
idéntico byte a byte y para que se vea QUÉ línea cambia y POR QUÉ.

Uso:  python3 aplicar_parches.py [ruta_del_repo]
"""
import pathlib
import sys

REPO = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/opt/photon")

CAMBIOS = [
    (
        "photon.py",
        "flag (?s) al final del patrón: re.error en Python 3.11+",
        "res = re.sub(r'<(script).*?</\\1>(?s)', '', response)",
        "res = re.sub(r'<(script).*?</\\1>', '', response, flags=re.S)",
    ),
    (
        "core/requester.py",
        "solo acepta text/html y text/plain: descarta todo .js",
        "if 'text/html' in response.headers['content-type'] or \\\n"
        "           'text/plain' in response.headers['content-type']:",
        "ctype = response.headers.get('content-type', '')\n"
        "        if 'text/html' in ctype or 'text/plain' in ctype or 'javascript' in ctype:",
    ),
    (
        "core/utils.py",
        "entropy() cuenta str sobre bytes: TypeError en Python 3 y --keys muerto",
        "    for number in range(256):\n"
        "        result = float(string.encode('utf-8').count(\n"
        "            chr(number))) / len(string.encode('utf-8'))",
        "    if not string:\n"
        "        return 0\n"
        "    for number in range(256):\n"
        "        result = float(string.count(chr(number))) / len(string)",
    ),
]

for nombre, motivo, viejo, nuevo in CAMBIOS:
    ruta = REPO / nombre
    texto = ruta.read_text(encoding="utf-8")
    if nuevo in texto:
        print(f"  ya aplicado: {nombre}")
        continue
    if viejo not in texto:
        sys.exit(f"FALLO: no encuentro el fragmento esperado en {nombre}")
    ruta.write_text(texto.replace(viejo, nuevo, 1), encoding="utf-8")
    print(f"  {nombre}: {motivo}")
    for linea in viejo.splitlines():
        print(f"    - {linea.strip()}")
    for linea in nuevo.splitlines():
        print(f"    + {linea.strip()}")

print("los tres arreglos aplicados")
