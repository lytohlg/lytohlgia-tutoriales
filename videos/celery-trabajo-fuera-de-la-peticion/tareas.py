"""Las tareas que la web manda a la cola.

El trabajador (worker) importa este fichero: aquí vive el trabajo pesado.
Nada de este fichero corre dentro de la petición del usuario.
"""
import os
import time

from celery import Celery

BROKER = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")

app = Celery("tareas", broker=BROKER, backend=BROKER)
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    # Con una sola plaza se ve en el registro que las tareas van de una en una.
    worker_concurrency=1,
    # Cuánto espera Redis a que el trabajador confirme antes de devolver la tarea a la cola.
    broker_transport_options={"visibility_timeout": 60},
)


@app.task(bind=True, autoretry_for=(ConnectionError,), retry_backoff=2,
          retry_jitter=False, max_retries=2)
def informe(self, cliente: str) -> dict:
    """El trabajo pesado: ocho segundos de verdad (aquí, esperando)."""
    time.sleep(8)
    return {"cliente": cliente, "lineas": 1200, "hecho": True}


@app.task(bind=True, autoretry_for=(ConnectionError,), retry_backoff=2,
          retry_jitter=False, max_retries=2)
def cobro(self, cliente: str) -> dict:
    """Falla siempre: sirve para ver los reintentos con espera creciente."""
    time.sleep(2)
    raise ConnectionError(f"la pasarela de {cliente} no responde")
