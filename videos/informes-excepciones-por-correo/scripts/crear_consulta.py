#!/usr/bin/env python3
"""Paso 3 — dejar GUARDADA la consulta de excepciones dentro de SQL Explorer.

No se guarda en un fichero suelto: se da de alta en la propia herramienta, en su
tabla de consultas guardadas (`explorer_query`), que es la misma que usa su
pantalla. Un SQL escrito a mano en un script no es una consulta de SQL Explorer.
"""
import sqlite3

from arranque import RAIZ, preparar_django

preparar_django()

from django.contrib.auth.models import User                    # noqa: E402
from explorer.ee.db_connections.models import DatabaseConnection  # noqa: E402
from explorer.models import Query                              # noqa: E402

TITULO = "Excepciones: pedidos sin servir y facturas vencidas"

sql = (RAIZ / "excepciones.sql").read_text(encoding="utf-8").strip()

# 1. contra que datos corre: la base "empresa" (los pedidos y las facturas).
conexion = DatabaseConnection.objects.filter(alias="empresa").first()
if conexion is None:
    conexion = DatabaseConnection.objects.create(
        alias="empresa",
        engine=DatabaseConnection.DJANGO,
        name="empresa",
        default=True,
    )

# 2. quien la crea: la herramienta guarda autor y fecha de cada consulta.
usuario, _ = User.objects.get_or_create(
    username="informes", defaults={"is_staff": True, "is_superuser": True})

# 3. la consulta guardada.
consulta, creada = Query.objects.get_or_create(
    title=TITULO,
    defaults={
        "sql": sql,
        "description": "Lo que se queda atras: pedidos sin servir y facturas vencidas.",
        "created_by_user": usuario,
        "database_connection": conexion,
    },
)
if not creada:
    consulta.sql = sql
    consulta.database_connection = conexion
    consulta.save()

# Se lee de vuelta DESDE la tabla de la herramienta: si está ahí, está guardada.
con = sqlite3.connect(RAIZ / "explorer.db")
fila = con.execute(
    "SELECT id, title, LENGTH(sql) FROM explorer_query WHERE id = ?", (consulta.id,)
).fetchone()
total = con.execute("SELECT COUNT(*) FROM explorer_query").fetchone()[0]
con.close()

print("consulta guardada dentro de SQL Explorer")
print(f"  id        {fila[0]}")
print(f"  titulo    {fila[1]}")
print(f"  conexion  {conexion.alias}  (la base de los datos)")
print(f"  tabla     explorer_query        <- la de la propia herramienta")
print(f"  estado    guardada ({total} consulta(s) en la tabla)")
