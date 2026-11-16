"""Resumen de ventas del día."""
from __future__ import annotations

from stock import stock_restante


def resumen(ventas: list[int]) -> str:
    total = 0
    for v in ventas:
        total = total + v
    return total


def etiqueta(unidades: int) -> str:
    if unidades == 0:
        return "agotado"
