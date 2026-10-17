"""Ajustes del proyecto Django de la demo.

Lo que se cuenta aquí y lo que sale en el vídeo son lo mismo: una app Django
(SQL Explorer) con dos bases SQLite y un servidor de correo de pruebas local.
"""
import os
from pathlib import Path

# --------------------------------------------------------------------------- rutas
# parents: [0]=informes  [1]=proyecto  [2]=la carpeta de la demo (donde está demo.sh)
RAIZ = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------- básicos
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

# Clave de ejemplo. Este proyecto es para una demo local; no es para producción.
SECRET_KEY = "solo-para-la-demo-no-usar-en-produccion"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "explorer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "informes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "informes.wsgi.application"

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
USE_TZ = True
TIME_ZONE = "UTC"

# --------------------------------------------------------------------------- bases
# Dos bases SQLite, como en la vida real:
#   default  -> las tablas de la propia app (consultas guardadas, histórico...)
#   empresa  -> los datos del negocio (pedidos y facturas), SOLO para consultar
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": RAIZ / "explorer.db"},
    "empresa": {"ENGINE": "django.db.backends.sqlite3", "NAME": RAIZ / "empresa.db"},
}

# --------------------------------------------------------------------------- SQL Explorer
# La app trabaja contra la base "empresa" (los datos del negocio), no contra sus
# propias tablas: se declara la conexión y se deja como la de por defecto.
EXPLORER_CONNECTIONS = {"empresa": "empresa"}
EXPLORER_DEFAULT_CONNECTION = "empresa"
EXPLORER_ENABLE_ANONYMOUS_STATS = False  # nada de telemetría hacia fuera
EXPLORER_TASKS_ENABLED = True            # la herramienta trae tareas (celery)
EXPLORER_FROM_EMAIL = "informes@example.com"

# El informe va a S3 y al correo va el enlace de descarga (es lo que hace la
# herramienta). Aquí el S3 es local, para no depender de credenciales de nadie.
EXPLORER_S3_BUCKET = "informes"
EXPLORER_S3_ACCESS_KEY = "demo"
EXPLORER_S3_SECRET_KEY = "demo-local"
EXPLORER_S3_ENDPOINT_URL = os.environ.get("S3_LOCAL_URL", "http://127.0.0.1:5000")
EXPLORER_S3_REGION = "us-east-1"

# --------------------------------------------------------------------------- correo
# Servidor de correo de pruebas (MailHog): SMTP real, en local, sin claves.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = "informes@example.com"

# --------------------------------------------------------------------------- cola
# Sin worker: la tarea de la herramienta se ejecuta en el acto cuando se encola.
CELERY_BROKER_URL = "memory://"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
