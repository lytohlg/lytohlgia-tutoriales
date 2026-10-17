#!/usr/bin/env python3
"""Paso 2 — la siembra: se llenan pedidos y facturas con datos realistas.

Crea (de cero, siempre igual) la base SQLite `empresa.db` con las dos tablas del
negocio. Las fechas se ponen relativas a HOY: así la demo tiene siempre las mismas
excepciones, se ejecute el día que se ejecute.
"""
import sqlite3
from datetime import date, timedelta

from arranque import RAIZ, preparar_django

preparar_django()

HOY = date.today()


def dia(desplazamiento):
    return (HOY + timedelta(days=desplazamiento)).isoformat()


# Pedidos: (id, cliente, fecha_entrega, estado, importe)
PEDIDOS = [
    (1001, "Ferreteria Vega",   dia(-12), "pendiente", 1284.50),
    (1002, "Talleres Rios",     dia(-6),  "pendiente", 640.00),
    (1003, "Suministros Norte", dia(-2),  "pendiente", 298.75),
    (1004, "Ferreteria Vega",   dia(3),   "pendiente", 410.20),
    (1005, "Obras Pinar",       dia(-1),  "servido",   1550.00),
    (1006, "Suministros Norte", dia(9),   "servido",   233.10),
    (1007, "Talleres Rios",     dia(-20), "servido",   980.00),
]

# Facturas: (id, cliente, vencimiento, importe, cobrada)
FACTURAS = [
    ("F-2026-0441", "Ferreteria Vega",   dia(-9),  1284.50, 0),
    ("F-2026-0455", "Talleres Rios",     dia(-3),  640.00,  0),
    ("F-2026-0460", "Obras Pinar",       dia(5),   1550.00, 0),
    ("F-2026-0402", "Suministros Norte", dia(-15), 233.10,  1),
    ("F-2026-0450", "Ferreteria Vega",   dia(12),  410.20,  0),
]

con = sqlite3.connect(RAIZ / "empresa.db")
con.execute("DROP TABLE IF EXISTS pedidos")
con.execute("DROP TABLE IF EXISTS facturas")
con.execute("""CREATE TABLE pedidos (
    id            INTEGER PRIMARY KEY,
    cliente       TEXT NOT NULL,
    fecha_entrega TEXT NOT NULL,
    estado        TEXT NOT NULL,
    importe       REAL NOT NULL)""")
con.execute("""CREATE TABLE facturas (
    id          TEXT PRIMARY KEY,
    cliente     TEXT NOT NULL,
    vencimiento TEXT NOT NULL,
    importe     REAL NOT NULL,
    cobrada     INTEGER NOT NULL)""")
con.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?)", PEDIDOS)
con.executemany("INSERT INTO facturas VALUES (?,?,?,?,?)", FACTURAS)
con.commit()
con.close()

print("empresa.db sembrada (fechas relativas a hoy)")
print(f"  pedidos    {len(PEDIDOS)} filas")
print(f"  facturas   {len(FACTURAS)} filas")
print(f"  total      {len(PEDIDOS) + len(FACTURAS)} filas")
