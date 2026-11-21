"""Sigue una tarea hasta que termina e imprime cada cambio de estado con su hora real.

Uso: python estado.py <identificador-de-tarea>
"""
import sys
import time

from celery.result import AsyncResult

from tareas import app as app_celery

ident = sys.argv[1] if len(sys.argv) > 1 else ""
if not ident:
    print("uso: python estado.py <id de tarea>")
    raise SystemExit(2)

t0 = time.perf_counter()
visto = None
while time.perf_counter() - t0 < 90:
    r = AsyncResult(ident, app=app_celery)
    estado = r.state
    if estado != visto:
        print(f"{time.perf_counter() - t0:5.1f}s  {estado}", flush=True)
        visto = estado
    if estado in ("SUCCESS", "FAILURE"):
        print(f"resultado: {r.result}", flush=True)
        print(f"total: {time.perf_counter() - t0:.1f}s", flush=True)
        break
    time.sleep(0.5)
else:
    print("sin terminar en 90 s", flush=True)
    raise SystemExit(1)
