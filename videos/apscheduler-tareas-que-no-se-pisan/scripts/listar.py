import os
import time

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

TZ = os.environ.get("APS_TZ", "Europe/Madrid")
DB = os.path.abspath(os.environ.get("AGENDA_DB", "agenda.sqlite"))


def enviar_resumen():
    print("resumen enviado", flush=True)


def aviso():
    print("AVISO DISPARADO por el proceso nuevo", flush=True)


tienda = SQLAlchemyJobStore(url="sqlite:///" + DB)
plan = BackgroundScheduler(timezone=TZ, jobstores={"default": tienda})
plan.start(paused=True)
for tarea in plan.get_jobs():
    print("recuperada:", tarea.id, "| proxima:", tarea.next_run_time, flush=True)
print("total en disco:", len(plan.get_jobs()), flush=True)
plan.resume()
time.sleep(12)
plan.shutdown(wait=False)
print("fin", flush=True)
