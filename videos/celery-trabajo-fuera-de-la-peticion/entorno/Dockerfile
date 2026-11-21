# Entorno de pruebas del vídeo «Celery: ejecuta tareas lentas sin bloquear tu web» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-celery-trabajo-fuera-de-la-peticion:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Redis de verdad dentro del contenedor: es el tercero que guarda la cola,
# y curl para medir los tiempos de respuesta desde fuera del programa.
RUN apt-get update && apt-get install -y --no-install-recommends \
      redis-server \
      curl \
      procps \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python, SIEMPRE con la versión fijada:
# OJO: el transporte de Redis de esta versión de Celery importa `packaging` y no lo
# declara (medido: sin él, la web devuelve ModuleNotFoundError al encolar).
RUN pip install --no-cache-dir celery==5.7.0 redis==7.4.1 packaging==24.1

WORKDIR /trabajo
