# Entorno de pruebas del vídeo «Jinja: el mismo informe para cada cliente sin copiar y pegar» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-jinja-informes-por-cliente:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Dependencias del sistema (descomenta si hacen falta, una por línea):
# RUN apt-get update && apt-get install -y --no-install-recommends \
#       <paquete> \
#     && rm -rf /var/lib/apt/lists/*

# Dependencias de Python, SIEMPRE con la versión fijada:
RUN pip install --no-cache-dir jinja2==3.1.6

WORKDIR /trabajo
