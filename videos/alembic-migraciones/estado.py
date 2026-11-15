"""Estado real de la base de datos, leído de la base (no del modelo).

Esto es lo que ve cualquiera que abra la base: qué columnas tiene la tabla
y cuántas filas hay dentro. Sirve para comprobar, sin creernos nada, que
una migración cambió la estructura y NO se llevó por delante los datos.
"""
from sqlalchemy import create_engine, inspect, text

motor = create_engine("sqlite:///tienda.db")
insp = inspect(motor)

if "clientes" not in insp.get_table_names():
    print("La tabla clientes NO existe")
else:
    columnas = [c["name"] for c in insp.get_columns("clientes")]
    print("Columnas de clientes:", ", ".join(columnas))
    with motor.connect() as con:
        print("Filas:", con.execute(text("SELECT count(*) FROM clientes")).scalar())
        for fila in con.execute(text("SELECT * FROM clientes")):
            print("  ", tuple(fila))
