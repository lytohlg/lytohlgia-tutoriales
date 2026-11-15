"""Tres clientes de ejemplo, insertados como los insertaría la aplicación.

Se ejecuta DESPUÉS de la primera migración: la tabla ya existe con su forma
inicial y ahora le metemos datos reales. En el momento en que cambiemos la
estructura, estas tres filas tendrán que seguir ahí.
"""
from models import Base, Cliente
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

motor = create_engine("sqlite:///tienda.db")
Base.metadata.create_all(motor)  # solo por si se ejecuta fuera de Alembic

with Session(motor) as sesion:
    if sesion.query(Cliente).count() == 0:
        sesion.add_all([
            Cliente(nombre="Panadería Luna", ciudad="Sevilla"),
            Cliente(nombre="Taller Norte", ciudad="Bilbao"),
            Cliente(nombre="Óptica Mar", ciudad="Alicante"),
        ])
        sesion.commit()

print("Datos insertados.")
