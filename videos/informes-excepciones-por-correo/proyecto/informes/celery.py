"""La cola de tareas del proyecto.

SQL Explorer manda el informe por correo DESDE UNA TAREA en segundo plano: la
vista del botón de correo encola `explorer.tasks.execute_query`. En el vídeo no
hay un servidor de colas levantado, así que la tarea se ejecuta en el acto
(`task_always_eager`): es la misma tarea de la herramienta, sin worker de por medio.
"""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informes.settings")

app = Celery("informes")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
