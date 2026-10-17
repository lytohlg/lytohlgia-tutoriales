#!/usr/bin/env python3
"""Paso 4 — ejecutar la consulta guardada con el motor de SQL Explorer.

No se lanza un SELECT suelto contra sqlite3: se le pide a la herramienta que
ejecute SU consulta (`Query.execute_with_logging`), que es lo que hace cuando le
das al botón de ejecutar en su pantalla. Además queda apuntada en su histórico.
"""
from arranque import preparar_django

preparar_django()

from django.contrib.auth.models import User                    # noqa: E402
from explorer.models import Query                              # noqa: E402

consulta = Query.objects.get(title="Excepciones: pedidos sin servir y facturas vencidas")
usuario = User.objects.get(username="informes")

resultado, registro = consulta.execute_with_logging(usuario)

print(f"consulta: {consulta.title}  (id {consulta.id})")
print(f"excepciones encontradas: {len(resultado.data)}")
print()

cabeceras = resultado.header_strings
filas = []
for fila in resultado.data:
    filas.append([f"{v:.2f}" if isinstance(v, float) else str(v) for v in fila])

anchos = [max(len(cabeceras[i]), *(len(f[i]) for f in filas))
          for i in range(len(cabeceras))]
print("  ".join(c.upper().ljust(anchos[i]) for i, c in enumerate(cabeceras)))
for fila in filas:
    print("  ".join(fila[i].ljust(anchos[i]) for i in range(len(cabeceras))))

print()
print(f"la herramienta lo ha apuntado en su historico (explorer_querylog): "
      f"ejecucion #{registro.id}, {registro.duration:.0f} ms, "
      f"correcta={'si' if registro.success else 'no'}")
