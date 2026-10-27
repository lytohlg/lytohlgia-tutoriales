import os
import time

from apscheduler.schedulers.background import BackgroundScheduler

TZ = os.environ.get("APS_TZ", "Europe/Madrid")


def generar_informe():
    print("informe generado a las", time.strftime("%H:%M:%S"), flush=True)


def parar():
    plan.shutdown(wait=False)


plan = BackgroundScheduler(timezone=TZ)
plan.add_job(generar_informe, "interval", seconds=2, id="informe")
plan.start()
print("programado: informe cada 2 segundos", flush=True)
time.sleep(7)
parar()
print("planificador detenido", flush=True)
