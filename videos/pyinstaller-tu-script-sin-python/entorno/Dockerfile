FROM python:3.12-slim-bookworm
# Imagen BUENA: la más vieja que el destino. Un binario compilado aquí corre en
# cualquier Debian/Ubuntu con glibc >= 2.36 (bookworm en adelante).
# binutils: PyInstaller en Linux necesita objdump para analizar los binarios.
RUN apt-get update \
    && apt-get install -y --no-install-recommends binutils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pyinstaller==6.11.1 rich==13.9.4
WORKDIR /trabajo
