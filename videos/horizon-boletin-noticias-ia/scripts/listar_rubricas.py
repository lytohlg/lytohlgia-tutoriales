#!/usr/bin/env python3
"""Lista los perfiles del boletín y enseña la rúbrica real de uno de ellos.

Uso: python3 scripts/listar_rubricas.py ejemplo/reglas tech-news
Un perfil son tres ficheros de texto (match.md, analysis.md, enrichment.md)
más profile.json, que dice qué fichero hace cada cosa.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def bandas(analysis_md: str) -> list[str]:
    """Extrae las líneas de rúbrica que empiezan por «- **n-m»."""
    salida = []
    for linea in analysis_md.splitlines():
        limpia = linea.strip()
        if limpia.startswith("- **") and "/10" not in limpia[:0]:
            salida.append(limpia)
    return salida


def main() -> int:
    base = Path(sys.argv[1] if len(sys.argv) > 1 else "ejemplo/reglas")
    elegido = sys.argv[2] if len(sys.argv) > 2 else "tech-news"

    perfiles = sorted(p for p in base.iterdir() if p.is_dir())
    print(f"perfiles: {len(perfiles)}")

    for p in perfiles:
        textos = [n for n in ("match.md", "analysis.md", "enrichment.md") if (p / n).exists()]
        print(f"- {p.name}: {len(textos)} ficheros de texto ({', '.join(textos)}) + profile.json")

    carpeta = base / elegido
    if not carpeta.exists():
        print(f"aviso: no existe el perfil «{elegido}»")
        return 0

    try:
        meta = json.loads((carpeta / "profile.json").read_text(encoding="utf-8"))
        print(f"perfil elegido: {meta.get('name', elegido)} (id {meta.get('id', elegido)})")
    except (OSError, json.JSONDecodeError):
        print(f"perfil elegido: {elegido}")

    analysis = (carpeta / "analysis.md").read_text(encoding="utf-8")
    print("rúbrica de puntuación:")
    for linea in bandas(analysis)[:6]:
        print("  " + linea)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
