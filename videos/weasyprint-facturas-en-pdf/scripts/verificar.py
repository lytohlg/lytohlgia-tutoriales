#!/usr/bin/env python3
"""Comprueba el PDF generado contra los datos que debía contener.

No se fía de que el script «haya terminado sin error»: abre el PDF, lo pasa a texto
y cuenta lo que tiene que estar. Uso:

    python scripts/verificar.py salida/factura.pdf datos/factura-2026-1042.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def euros(valor: float) -> str:
    return f"{valor:.2f}".replace(".", ",")


def paginas_de_texto(pdf: Path) -> list[str]:
    salida = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [p for p in salida.split("\f") if p.strip()]


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    pdf = Path(sys.argv[1])
    datos = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    paginas = paginas_de_texto(pdf)
    n = len(paginas)

    # 1) La cabecera de página tiene que estar en TODAS las páginas: el CSS la repite.
    cabecera = sum(1 for p in paginas if datos["cliente"] in p and datos["numero"] in p)

    # 2) La numeración tiene que decir el número correcto en cada página.
    numeracion = sum(
        1 for i, p in enumerate(paginas, 1) if f"Página {i} de {n}" in p
    )

    # 3) La cabecera de la tabla se repite en cada página (thead + table-header-group).
    cabecera_tabla = sum(1 for p in paginas if "Descripción" in p and "Importe" in p)

    # 4) Ninguna fila partida: la referencia y su importe, en la misma línea.
    partidas = []
    for linea in datos["lineas"]:
        importe = euros(linea["cantidad"] * linea["precio"])
        encontrada = False
        for pagina in paginas:
            for texto in pagina.splitlines():
                if linea["ref"] in texto:
                    encontrada = True
                    if importe in texto:
                        partidas.append(None)  # fila entera: se anula al final
                        break
            else:
                continue
            break
        if not encontrada:
            partidas.append(linea["ref"] + "(no aparece)")
    rotas = [r for r in partidas if r]

    print(
        f"{pdf.as_posix()}  paginas={n}  cabecera={cabecera}/{n}  "
        f"numeracion={numeracion}/{n}  cabecera_tabla={cabecera_tabla}/{n}  "
        f"filas_partidas={len(rotas)}"
    )
    if rotas:
        print("  filas que perdieron su importe: " + ", ".join(rotas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
