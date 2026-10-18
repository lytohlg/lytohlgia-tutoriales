# Entorno de pruebas del vídeo «PaddleOCR: busca dentro de tus PDF escaneados con Python» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-paddleocr-documentos-escaneados:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# Dependencias del sistema: las que exige PaddleOCR/OpenCV (libgl1, libglib2.0-0, libgomp1),
# las fuentes para generar los documentos de prueba y poppler-utils para el pdftotext del principio.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgl1 \
      libglib2.0-0 \
      libgomp1 \
      fonts-dejavu-core \
      poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python, SIEMPRE con la versión fijada:
RUN pip install --no-cache-dir paddlepaddle==3.3.1 paddleocr==3.7.0

# Los pesos del modelo se descargan en la primera ejecución; se dejan YA dentro de la imagen
# para que la prueba no dependa de la red ni del momento en que la ejecutes.
RUN python3 -c "from paddleocr import PaddleOCR; PaddleOCR(lang='es', use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, enable_mkldnn=False)"

WORKDIR /trabajo
