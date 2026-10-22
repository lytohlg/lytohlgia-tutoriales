FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# qpdf y poppler-utils (pdfinfo) NO son la herramienta del vídeo: sirven para comprobar
# con OTRA herramienta que el cifrado y el giro son lo que decimos que son.
RUN apt-get update \
 && apt-get install -y --no-install-recommends qpdf poppler-utils fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# pypdf con el extra "crypto" (sin él, el cifrado AES-256 no funciona).
# reportlab solo dibuja los PDF de ejemplo y el número de página.
RUN pip install --no-cache-dir "pypdf[crypto]==6.1.1" "reportlab==4.2.5"

# Este entorno NO copia código: los scripts y el demo.sh se montan desde la carpeta del
# repositorio (por eso aquí no hay ningún COPY).
WORKDIR /trabajo

CMD ["bash"]
