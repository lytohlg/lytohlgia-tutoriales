"""El modelo: la forma que queremos que tenga la tabla. Nada más.

Cambiar este fichero NO cambia la base de datos. Ese es justo el problema
que resuelve Alembic: aquí se declara el destino, y las migraciones son el
camino para llegar a él sin perder lo que ya había dentro.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String)
