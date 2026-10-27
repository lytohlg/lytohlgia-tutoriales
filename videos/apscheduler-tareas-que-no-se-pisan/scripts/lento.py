import os
import time

from apscheduler.schedulers.background import BackgroundScheduler

TZ = os.environ.get("APS_TZ", "Europe/Madrid")


def tarea_lenta():
    print("empieza", time.strftime("%H:%M:%S"), flush=True)
    time.sleep(3)
    print("termina", time.strftime("%H:%M:%S"), flush=True)


def parar():
    plan.shutdown(wait=False)


plan = BackgroundScheduler(timezone=TZ)
plan.add_job(tarea_lenta, "interval", seconds=1, max_instances=1, id="lenta")
plan.start()
print("programado: tarea de 3 s, cada 1 s, max_instances=1", flush=True)
time.sleep(9)
parar()
print("planificador detenido", flush=True)
