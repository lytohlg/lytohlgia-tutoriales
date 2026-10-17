#!/usr/bin/env python3
"""Paso 6 — estado: qué hace de verdad la herramienta si se lanza otra vez.

Dos cosas que se pueden comprobar, y ninguna inventada:

  * SQL Explorer guarda HISTÓRICO de cada ejecución de la consulta
    (`explorer_querylog`): cuándo, cuánto tardó y si salió bien.
  * Lo que NO lleva es control de duplicados: si se vuelve a lanzar el envío, el
    informe sale otra vez. El que decide la frecuencia es quien lo programa
    (un cron, o celery beat llamando a su tarea). La herramienta trae el enganche
    periódico `explorer.tasks.snapshot_queries` para sus snapshots.
"""
from arranque import preparar_django

preparar_django()

from explorer.models import Query, QueryLog                    # noqa: E402
from leer_correo import correos                                # noqa: E402
from enviar_alerta import TITULO, lanzar_envio                 # noqa: E402

consulta = Query.objects.get(title=TITULO)

print("historico de la consulta (tabla explorer_querylog, de la herramienta)")
for n, registro in enumerate(QueryLog.objects.filter(query=consulta).order_by("id"), start=1):
    print(f"  #{n}  {registro.run_at:%Y-%m-%d %H:%M:%S}  "
          f"{'ok' if registro.success else 'fallo'}  {registro.duration or 0:.0f} ms")
print()

antes = len(correos())
print(f"correos en el buzon antes de la segunda pasada: {antes}")
lanzar_envio()
despues = len(correos())
print(f"correos en el buzon despues de la segunda pasada: {despues}")
print()
print(f"la herramienta ha vuelto a mandar el informe ({despues - antes} correos):")
print("  no lleva control de duplicados; la frecuencia la pone quien la programa.")
print("  su enganche periodico propio es explorer.tasks.snapshot_queries (celery beat).")
