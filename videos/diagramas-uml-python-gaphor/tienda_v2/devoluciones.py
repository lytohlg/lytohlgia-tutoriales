"""Lo que añadimos después: la clase que antes no existía."""
from dataclasses import dataclass
from datetime import date


@dataclass
class Devolucion:
    pedido: int
    motivo: str
    fecha: date
