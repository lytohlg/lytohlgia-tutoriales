# Entorno de pruebas del vídeo «Panda Router: elige modelo por tarea y por coste, no por moda» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-panda-router-elegir-modelo-por-tarea:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    TRANSFORMERS_VERBOSITY=error \
    PYTHONUNBUFFERED=1

# git: la demo clona el proyecto dentro del contenedor. No se copia código de terceros
# en el paquete: el material apunta al original y la procedencia queda a la vista.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python con la versión exacta de la máquina donde se grabó el vídeo.
RUN pip install --no-cache-dir \
      numpy==2.5.4 \
      scipy==1.18.1 \
      jsonschema==4.26.0 \
      onnxruntime==1.31.1 \
      transformers==5.22.2

WORKDIR /trabajo
