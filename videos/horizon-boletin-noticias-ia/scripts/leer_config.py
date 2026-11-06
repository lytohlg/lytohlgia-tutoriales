#!/usr/bin/env python3
"""Lee el config real del boletín y dice, en cuatro líneas, qué va a hacer.

Uso: python3 scripts/leer_config.py ejemplo/config.json
No necesita red ni clave: solo interpreta el fichero de configuración.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def fuentes_activas(cfg: dict) -> list[str]:
    """Devuelve las fuentes que están activadas en el config."""
    nombres: list[str] = []
    for clave, valor in (cfg.get("sources") or {}).items():
        if isinstance(valor, dict) and valor.get("enabled"):
            nombres.append(clave)
        elif isinstance(valor, list):
            for entrada in valor:
                if isinstance(entrada, dict) and entrada.get("enabled"):
                    nombres.append(entrada.get("name") or clave)
    return nombres


def main() -> int:
    ruta = Path(sys.argv[1] if len(sys.argv) > 1 else "ejemplo/config.json")
    cfg = json.loads(ruta.read_text(encoding="utf-8"))

    ia = cfg.get("ai") or {}
    proc = cfg.get("processing") or {}
    perfil = proc.get("default_profile") or "?"
    ajustes = (proc.get("profile_settings") or {}).get(perfil) or {}

    idiomas = ia.get("languages") or []
    print(f"modelo: {ia.get('model', '?')}")
    print(f"idioma del boletín: {', '.join(idiomas) if idiomas else '(sin definir)'}")
    print(f"perfil por defecto: {perfil} · umbral de corte: {ajustes.get('threshold', '?')}")
    print("fuentes activas: " + ", ".join(fuentes_activas(cfg)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
