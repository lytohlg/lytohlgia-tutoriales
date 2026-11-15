# Entorno de prueba del vídeo «Alembic: cambia tu base de datos sin perder datos (tutorial Python)» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-alembic-migraciones:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Dependencias de Python, SIEMPRE con la versión fijada:
RUN pip install --no-cache-dir \
      alembic==1.20.1 \
      sqlalchemy==2.1.8

WORKDIR /trabajo
