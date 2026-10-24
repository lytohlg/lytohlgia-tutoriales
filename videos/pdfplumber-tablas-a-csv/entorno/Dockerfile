# Entorno de pruebas del vídeo «pdfplumber: extrae las tablas de un PDF a CSV sin copiar» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-pdfplumber-tablas-a-csv:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# poppler-utils (pdftoppm) NO es la herramienta del vídeo: sirve para fabricar un PDF
# escaneado de verdad (una imagen dentro de un PDF) y medir que ahí no hay texto.
RUN apt-get update \
 && apt-get install -y --no-install-recommends poppler-utils fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# pdfplumber es la herramienta del vídeo. reportlab solo dibuja los albaranes de ejemplo.
RUN pip install --no-cache-dir "pdfplumber==0.11.5" "reportlab==4.2.5"

# Este entorno NO copia código: los scripts y demo.sh se montan desde la carpeta del
# repositorio (por eso aquí no hay ningún COPY).
WORKDIR /trabajo

CMD ["bash"]
