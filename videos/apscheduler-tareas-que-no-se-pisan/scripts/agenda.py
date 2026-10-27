import datetime
import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

TZ = os.environ.get("APS_TZ", "Europe/Madrid")
DB = os.path.abspath(os.environ.get("AGENDA_DB", "agenda.sqlite"))


def enviar_resumen():
    print("resumen enviado", flush=True)


def aviso():
    print("AVISO DISPARADO por el proceso nuevo", flush=True)


tienda = SQLAlchemyJobStore(url="sqlite:///" + DB)
plan = BackgroundScheduler(timezone=TZ, jobstores={"default": tienda})
plan.add_job(enviar_resumen, CronTrigger(hour=8, minute=0, timezone=TZ), id="resumen_diario")
plan.add_job(aviso, "date",
             run_date=datetime.datetime.now() + datetime.timedelta(seconds=8),
             misfire_grace_time=300, id="aviso")
plan.start(paused=True)
for tarea in plan.get_jobs():
    print("guardada:", tarea.id, "| proxima:", tarea.next_run_time, flush=True)
plan.shutdown(wait=False)
print("proceso terminado, agenda en disco", flush=True)
