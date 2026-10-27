"""Comprueba que la demo produjo la evidencia que dice producir."""
import os
import sqlite3
import sys

SAL = sys.argv[1]
DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  os.environ.get("AGENDA_DB", "agenda.sqlite"))


def leer(nombre):
    with open(os.path.join(SAL, nombre + ".txt"), encoding="utf-8") as fh:
        return fh.read()


informe = leer("informe")
lento = leer("lento")
perdido = leer("perdido")
agenda = leer("agenda")
listar = leer("listar")

fallos = []
if informe.count("informe generado") < 3:
    fallos.append("el intervalo no disparó 3 veces")
rechazos = lento.count("maximum number of running instances reached")
if rechazos < 2:
    fallos.append("max_instances no rechazó copias (encontradas %d)" % rechazos)
if "was missed by" not in perdido:
    fallos.append("la tarea vencida no se descartó")
if "guardada: resumen_diario" not in agenda or "proceso terminado" not in agenda:
    fallos.append("la agenda no se guardó en disco")
if "recuperada: resumen_diario" not in listar:
    fallos.append("el segundo proceso no recuperó la agenda")
if "AVISO DISPARADO" not in listar:
    fallos.append("el segundo proceso no ejecutó la tarea guardada")

if not os.path.exists(DB):
    fallos.append("no existe %s" % DB)
    filas = 0
else:
    con = sqlite3.connect(DB)
    filas = con.execute("select count(*) from apscheduler_jobs").fetchone()[0]
    con.close()
    if filas < 1:
        fallos.append("la tabla apscheduler_jobs está vacía")

if fallos:
    print("FALLOS:", " · ".join(fallos))
    raise SystemExit(1)

print("VERIFICADO: disparo cada 2 s · %d copias rechazadas por max_instances · tarea vencida "
      "descartada · agenda en disco con %d tarea(s) · tarea ejecutada por un proceso nuevo"
      % (rechazos, filas))
