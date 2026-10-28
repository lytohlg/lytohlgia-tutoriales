#!/usr/bin/env python3
"""Los dos límites que hay que saber ANTES de elegir esta herramienta.

1) WeasyPrint no ejecuta JavaScript: si el contenido se genera con JS, no aparece.
2) No inventa fuentes: si la que pides no está instalada en la máquina, sustituye.

Imprime una línea con las dos comprobaciones, medidas sobre el PDF resultante.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from weasyprint import HTML

TEXTO_JS = "TEXTO-INYECTADO-POR-JAVASCRIPT"

HTML_PRUEBA = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 20mm; }}
  body {{ font-family: "Arial Black"; font-size: 11pt; }}
</style></head>
<body>
  <p>Antes del script.</p>
  <script>document.write("{TEXTO_JS}")</script>
  <p>Despues del script.</p>
</body></html>
"""


def texto_del_pdf(pdf: Path) -> str:
    return subprocess.run(
        ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
    ).stdout


def fuentes_del_pdf(pdf: Path) -> list[str]:
    salida = subprocess.run(
        ["pdffonts", str(pdf)], capture_output=True, text=True, check=True
    ).stdout
    nombres = []
    for linea in salida.splitlines()[2:]:
        partes = linea.split()
        if partes:
            nombres.append(partes[0])
    return nombres


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "limites.pdf"
        HTML(string=HTML_PRUEBA).render().write_pdf(pdf)
        texto = texto_del_pdf(pdf)
        fuentes = fuentes_del_pdf(pdf)

    ejecutado = TEXTO_JS in texto
    pedida = "Arial Black"
    embebida = fuentes[0].split("+")[-1] if fuentes else "(ninguna)"
    print(
        f"javascript_ejecutado={'si' if ejecutado else 'no'}  "
        f"texto_del_script_en_el_pdf={'si' if ejecutado else 'no'}  "
        f"fuente_pedida=\"{pedida}\"  fuente_embebida={embebida}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
