"""Modelo de la tienda: lo que el código sí dice."""
from dataclasses import dataclass
from datetime import date


@dataclass
class Cliente:
    nombre: str
    email: str


@dataclass
class Producto:
    sku: str
    precio: float


@dataclass
class Pedido:
    fecha: date
    total: float


class PedidoUrgente(Pedido):
    horas_limite: int


@dataclass
class LineaPedido:
    cantidad: int
