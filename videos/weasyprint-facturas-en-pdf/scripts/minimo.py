#!/usr/bin/env python3
"""El PDF más pequeño posible con WeasyPrint: seis líneas y ni una dependencia más."""
from pathlib import Path

from weasyprint import HTML

html = "<h1>Hola</h1><p>Un PDF de una página, generado desde una cadena de texto.</p>"
HTML(string=html).write_pdf(Path("salida/minimo.pdf"))
print("generado: salida/minimo.pdf")
