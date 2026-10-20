FROM python:3.11-slim

# tesseract: el motor que lee las letras. tesseract-ocr-spa: el idioma español.
# poppler-utils: pdftotext (para comprobar que hay texto). ghostscript y qpdf:
# los usa ocrmypdf para reconstruir el PDF. fonts-dejavu: letra para los PDF de prueba.
RUN apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr tesseract-ocr-spa poppler-utils ghostscript qpdf \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Versiones fijas: las mismas que se ejecutan en el video.
RUN pip install --no-cache-dir ocrmypdf==16.10.4 "pikepdf<10" pillow==11.3.0 \
    && ocrmypdf --version \
    && tesseract --version | head -1

WORKDIR /work
