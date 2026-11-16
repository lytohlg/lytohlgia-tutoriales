"""Stock del almacén.

Funciones que ya usa el programa principal.
"""
from __future__ import annotations


def stock_restante(total: int, vendidos: int) -> int:
    return total - vendidos


def buscar_precio(catalogo: dict[str, float], referencia: str) -> float | None:
    """Devuelve el precio, o None si la referencia no está en el catálogo."""
    return catalogo.get(referencia)
