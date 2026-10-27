import datetime
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler

TZ = os.environ.get("APS_TZ", "Europe/Madrid")
DB = os.environ.get("AGENDA_DB", "agenda.sqlite")


def enviar_resumen():
    print("resumen enviado", flush=True)


def parar():
    plan.shutdown(wait=False)


plan = BackgroundScheduler(timezone=TZ)
plan.add_job(enviar_resumen, "date",
             run_date=datetime.datetime.now() - datetime.timedelta(minutes=5),  # su hora fue hace 5 min
             misfire_grace_time=60,                                            # solo vale hasta 60 s tarde
             id="resumen_vencido")
plan.start()
print("programado: tarea con hora de hace 5 min y gracia de 60 s", flush=True)
time.sleep(3)
parar()
print("fin", flush=True)
