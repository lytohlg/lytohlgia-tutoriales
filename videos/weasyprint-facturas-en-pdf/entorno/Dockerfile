# Entorno de pruebas del vídeo «WeasyPrint: facturas en PDF desde HTML y CSS, sin maquetar a mano» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-weasyprint-facturas-en-pdf:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.13-slim

# WeasyPrint no es Python puro: usa Pango para componer el texto y Fontconfig para
# resolver las fuentes. Sin estas librerías del sistema, el import falla con
# "cannot load library 'libgobject-2.0-0'". poppler-utils es para VERIFICAR el PDF
# (pdfinfo, pdftotext, pdffonts), no para generarlo.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libpango-1.0-0 \
      libpangoft2-1.0-0 \
      libharfbuzz-subset0 \
      libfontconfig1 \
      fonts-dejavu-core \
      poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python, SIEMPRE con la versión fijada:
RUN pip install --no-cache-dir weasyprint==70.0

WORKDIR /trabajo
