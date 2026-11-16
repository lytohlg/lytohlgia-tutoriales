"""Cuentas de una línea de factura."""
from __future__ import annotations

from stock import buscar_precio


def total_linea(catalogo: dict[str, float], referencia: str, unidades: int) -> float:
    precio = buscar_precio(catalogo, referencia)
    return precio * unidades
