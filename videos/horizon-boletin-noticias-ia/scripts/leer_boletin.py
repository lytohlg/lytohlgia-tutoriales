#!/usr/bin/env python3
"""Lee un boletín ya generado y resume lo que trae, sin abrir el markdown a mano.

Uso: python3 scripts/leer_boletin.py ejemplo/boletin-es.md
Es el fichero que el programa escribe en data/summaries/ al terminar.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CABECERA = re.compile(r"From\s+(\d+)\s+items,\s+(\d+)\s+important content pieces were selected", re.I)
ITEM = re.compile(r"^\s*\d+\.\s+\[(.+?)\]\((\S+?)\)\s+.*?([\d.]+)\s*/\s*10", re.M)
BLOQUE = re.compile(r"\*\*「(.+?)」\*\*")


def main() -> int:
    ruta = Path(sys.argv[1] if len(sys.argv) > 1 else "ejemplo/boletin-es.md")
    texto = ruta.read_text(encoding="utf-8")

    cab = CABECERA.search(texto)
    recogidas, seleccionadas = (int(cab.group(1)), int(cab.group(2))) if cab else (0, 0)
    items = ITEM.findall(texto)

    print(f"piezas recogidas: {recogidas}")
    print(f"seleccionadas: {seleccionadas}")
    if items:
        notas = [float(n) for _, _, n in items]
        print(f"nota media: {sum(notas) / len(notas):.1f}/10")
        for titulo, _, nota in items:
            print(f"- {nota}/10 {titulo.strip()}")

    bloques = []
    for nombre in BLOQUE.findall(texto):
        if nombre not in bloques:
            bloques.append(nombre)
    print("bloques por pieza: " + ", ".join(bloques[:4]) + ("…" if len(bloques) > 4 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
