# Entorno de pruebas del vídeo «OpenCV en Python: contar piezas en una foto y que el número cuadre» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-contar-piezas-fotos-opencv:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Dependencias de Python, SIEMPRE con la versión fijada:
RUN pip install --no-cache-dir \
        opencv-python-headless==4.10.0.84 \
        numpy==2.1.3

WORKDIR /trabajo
