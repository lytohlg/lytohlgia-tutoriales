"""Programa principal: stock y facturación."""
from __future__ import annotations

from facturas import total_linea
from informe import etiqueta, resumen
from stock import stock_restante

CATALOGO = {"A-1": 12.5, "B-2": 7.0}


def main() -> None:
    quedan = stock_restante("120", 15)
    importe = total_linea(CATALOGO, "A-1", 3)
    print("Quedan", quedan, "unidades")
    print("Importe de la línea:", importe)
    print("Resumen de ventas:", resumen([3, 1, 2]))
    print("Etiqueta:", etiqueta(0))


main()
