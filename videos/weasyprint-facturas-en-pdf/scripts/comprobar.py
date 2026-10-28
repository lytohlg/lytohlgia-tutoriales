#!/usr/bin/env python3
"""Comprobación final de la demo: una sola línea con todo lo que se ha verificado.

No confía en que los pasos anteriores «hayan ido bien»: vuelve a medir el PDF con
pdftotext y falla (exit 1) si algo no se cumple.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
SALIDA = BASE / "salida"
LARGA = BASE / "datos" / "factura-2026-1042.json"
CORTA = BASE / "datos" / "factura-2026-1043.json"


def corre(*args: str) -> str:
    return subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, check=True
    ).stdout


def metricas(pdf: Path, datos: Path) -> dict:
    texto = corre(str(AQUI / "verificar.py"), str(pdf), str(datos))
    linea = [l for l in texto.splitlines() if "paginas=" in l][0]
    campos = dict(re.findall(r"(\w+)=(\S+)", linea.split("  ", 1)[1]))
    return campos


def main() -> int:
    fallos = []

    buena = metricas(SALIDA / "factura.pdf", LARGA)
    mala = metricas(SALIDA / "sin-regla.pdf", LARGA)
    corta = metricas(SALIDA / "factura-corta.pdf", CORTA)
    limites = corre(str(AQUI / "limites.py")).strip()

    if int(buena["paginas"]) < 3:
        fallos.append(f"la factura larga tiene {buena['paginas']} páginas, se esperaban 3 o más")
    for campo in ("cabecera", "numeracion", "cabecera_tabla"):
        valor, total = buena[campo].split("/")
        if valor != total:
            fallos.append(f"{campo}: {buena[campo]} páginas")
    if buena["filas_partidas"] != "0":
        fallos.append(f"con la regla hay {buena['filas_partidas']} filas partidas")
    if int(mala["cabecera_tabla"].split("/")[0]) != 1:
        fallos.append(
            f"sin la regla la cabecera de tabla aparece en {mala['cabecera_tabla']} páginas "
            "(se esperaba solo en la primera): la demo no demuestra la diferencia"
        )
    if corta["paginas"] != "1":
        fallos.append(f"la factura corta tiene {corta['paginas']} páginas")
    if "javascript_ejecutado=si" in limites:
        fallos.append("se ejecutó JavaScript: el límite no se cumple")
    if "Arial" in limites.split("fuente_embebida=")[-1]:
        fallos.append("la fuente pedida sí se embebió: el límite no se cumple")

    if fallos:
        for f in fallos:
            print(f"FALLOS: {f}")
        return 1

    fuente = limites.split("fuente_embebida=")[-1].strip()
    print(
        f"VERIFICADO: {buena['paginas']} páginas · cabecera {buena['cabecera']} · "
        f"numeración {buena['numeracion']} · cabecera de tabla {buena['cabecera_tabla']} "
        f"(sin la regla, {mala['cabecera_tabla']}) · filas partidas {buena['filas_partidas']} · "
        f"otro cliente en {corta['paginas']} página · sin JavaScript · "
        f"fuente pedida Arial Black -> embebida {fuente}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
