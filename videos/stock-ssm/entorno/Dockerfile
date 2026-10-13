# Entorno de pruebas del vídeo «Avisos de stock bajo con Python: inventario real en Docker» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-stock-ssm:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Dependencias del sistema: `curl` es el que usa demo.sh para hablar con la API de la
# aplicación, igual que lo haría cualquiera desde una terminal.
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# La aplicación que vamos a vigilar es software de terceros (Simple Stock Management,
# GPL-3.0): se descarga de su repositorio público clavada en un commit concreto, para que
# esta máquina siga construyéndose igual aunque el proyecto siga avanzando.
ARG SSM_COMMIT=ce90315b6e243103487465fb2b26ac91de55e7a7
RUN curl -fsSL \
      "https://codeload.github.com/ConsciousUniverse/simple-stock-management/tar.gz/${SSM_COMMIT}" \
      -o /tmp/ssm.tar.gz \
    && mkdir -p /app \
    && tar -xzf /tmp/ssm.tar.gz -C /app --strip-components=1 \
    && rm /tmp/ssm.tar.gz

# Dependencias de Python, SIEMPRE con la versión fijada:
RUN pip install --no-cache-dir \
      Django==5.2.18 \
      djangorestframework==3.16.1 \
      django-axes[ipware]==8.3.1 \
      django-anymail[sparkpost]==15.2 \
      openpyxl==3.1.5 \
      python-dotenv==1.2.4 \
      natsort==8.4.0 \
      pytz==2026.5 \
      pandas==3.0.6

# El proyecto no trae las migraciones en el repositorio: se generan al instalar (una vez),
# como indica su README. Se hace aquí para que la demo arranque con la base de datos limpia.
RUN cd /app \
    && DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=True DJANGO_ALLOWED_HOSTS=127.0.0.1 \
       DB_NAME=db.sqlite3 AXES_FAILURE_LIMIT=5 AXES_COOLOFF_TIME=1 ALLOW_PW_CHANGE=True \
       MAIL_SERVICE_BACKEND=django.core.mail.backends.dummy.EmailBackend \
       LOG_FILE=/tmp/build.log \
       python manage.py makemigrations stock_manager --noinput \
    && chmod -R a+rX /app

WORKDIR /trabajo
