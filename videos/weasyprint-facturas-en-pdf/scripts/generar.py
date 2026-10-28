#!/usr/bin/env python3
"""Genera una factura en PDF a partir de tres piezas:

    datos/*.json   -> el contenido (cliente, líneas, importes)
    plantillas/*.html -> la estructura
    estilos/*.css  -> el aspecto y las reglas de paginación

Uso:
    python scripts/generar.py datos/factura-2026-1042.json salida/factura.pdf [estilos/factura.css]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from weasyprint import CSS, HTML

BASE = Path(__file__).resolve().parent.parent
PLANTILLA = BASE / "plantillas" / "factura.html"
CSS_POR_DEFECTO = BASE / "estilos" / "factura.css"


def euros(valor: float) -> str:
    """1234.5 -> '1234,50' (coma decimal, sin separador de miles)."""
    return f"{valor:.2f}".replace(".", ",")


def fila_html(linea: dict) -> str:
    importe = linea["cantidad"] * linea["precio"]
    return (
        "<tr>"
        f'<td class="ref">{linea["ref"]}</td>'
        f'<td>{linea["concepto"]}</td>'
        f'<td class="num">{linea["cantidad"]}</td>'
        f'<td class="num">{euros(linea["precio"])}</td>'
        f'<td class="num">{euros(importe)}</td>'
        "</tr>"
    )


def rellenar(plantilla: str, valores: dict[str, str]) -> str:
    """Sustituye {{clave}} por su valor. Sin motor de plantillas: es texto."""

    def sustituir(m: re.Match) -> str:
        return valores[m.group(1)]

    return re.sub(r"\{\{(\w+)\}\}", sustituir, plantilla)


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    datos_path = Path(sys.argv[1])
    salida = Path(sys.argv[2])
    css_path = Path(sys.argv[3]) if len(sys.argv) > 3 else CSS_POR_DEFECTO

    datos = json.loads(datos_path.read_text(encoding="utf-8"))
    lineas = datos["lineas"]
    base_imponible = sum(l["cantidad"] * l["precio"] for l in lineas)
    iva = round(base_imponible * datos["iva"], 2)

    valores = {
        "cliente": datos["cliente"],
        "nif": datos["nif"],
        "direccion": datos["direccion"],
        "numero": datos["numero"],
        "fecha": datos["fecha"],
        "vencimiento": datos["vencimiento"],
        "lineas": "\n      ".join(fila_html(l) for l in lineas),
        "base": euros(base_imponible),
        "iva_pct": f"{int(datos['iva'] * 100)}",
        "iva": euros(iva),
        "total": euros(base_imponible + iva),
        "n_lineas": str(len(lineas)),
    }

    html = rellenar(PLANTILLA.read_text(encoding="utf-8"), valores)
    documento = HTML(string=html, base_url=str(BASE)).render(
        stylesheets=[CSS(filename=str(css_path))]
    )
    salida.parent.mkdir(parents=True, exist_ok=True)
    documento.write_pdf(salida)

    kb = salida.stat().st_size / 1024
    print(
        f"generado: {salida.as_posix()}  lineas={len(lineas)}  "
        f"paginas={len(documento.pages)}  tamano={kb:.0f} KB  css={css_path.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
