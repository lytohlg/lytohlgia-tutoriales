FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# poppler-utils da pdftotext: sirve para comprobar con OTRA herramienta
# (no la del video) que el texto del DNI esta o no esta.
RUN apt-get update \
 && apt-get install -y --no-install-recommends poppler-utils fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pymupdf==1.26.5 pillow

# Este entorno NO copia código: los scripts del paquete se montan desde la
# carpeta del repositorio (por eso aquí no hay ningún COPY).
WORKDIR /trabajo

CMD ["bash"]
