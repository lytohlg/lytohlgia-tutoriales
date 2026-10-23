# Entorno de pruebas del vídeo «python-docx: rellena contratos de Word sin dejar marcadores» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-docx-contratos-por-cliente:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# unzip no es la herramienta del vídeo: sirve para leer el .docx por dentro (es un ZIP con XML)
# con algo que NO es python-docx, y así comprobar lo escrito con un segundo lector.
RUN apt-get update \
 && apt-get install -y --no-install-recommends unzip fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# La herramienta del vídeo. Versión fijada: mañana se comporta igual.
RUN pip install --no-cache-dir "python-docx==1.2.0" \
 && python3 -c "import importlib.metadata as m; print('python-docx', m.version('python-docx'))"

WORKDIR /trabajo
