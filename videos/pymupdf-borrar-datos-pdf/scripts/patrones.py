#!/usr/bin/env python3
"""Los patrones de datos personales, en un solo sitio.

`v1` es lo que escribiría cualquiera en cinco minutos. `v2` añade el formato
con puntos que se usa en las nóminas: la diferencia entre los dos es el vídeo.
"""
import re

BASE = {
    "DNI": re.compile(r"\b\d{8}[A-Z]\b"),
    "IBAN": re.compile(r"\bES\d{2}(?: \d{4}){5}\b"),
    "TELEFONO": re.compile(r"\b(?:\+34 )?[67]\d{2} \d{3} \d{3}\b"),
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}"),
}

PUNTOS = re.compile(r"\b\d{2}\.\d{3}\.\d{3}-[A-Z]\b")

VERSIONES = {"v1": BASE, "v2": dict(BASE, DNI_PUNTOS=PUNTOS)}


def buscar(texto, version="v1"):
    """Devuelve {tipo: [coincidencias]} con los patrones de esa versión."""
    return {tipo: [m.group(0) for m in patron.finditer(texto)]
            for tipo, patron in VERSIONES[version].items()}
