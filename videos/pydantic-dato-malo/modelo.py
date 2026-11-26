"""El mismo validador, pero declarado: un modelo de pydantic (v2).

Lo que hace la clase, sin una sola línea de comprobación a mano:
  - tipos: id entero, importe Decimal, fecha date
  - obligatorios: todos los campos lo son salvo que se declare lo contrario
  - restricciones: importe > 0 y <= 5000, cliente de 2 caracteres o más
  - dominios cerrados: estado sólo admite tres valores
  - formato: email de verdad, no «tiene una arroba»
  - columnas de más: extra="forbid" las denuncia en vez de ignorarlas
"""
import csv
import sys
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError


class Pedido(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: int = Field(gt=0)
    cliente: str = Field(min_length=2)
    email: EmailStr
    importe: Decimal = Field(gt=0, le=5000, decimal_places=2)
    fecha: date
    estado: Literal["pagado", "pendiente", "cancelado"]


def main(ruta):
    validos, errores = [], []
    with open(ruta, newline="", encoding="utf-8") as fh:
        for n, fila in enumerate(csv.DictReader(fh), start=1):
            try:
                validos.append((n, Pedido.model_validate(fila)))
            except ValidationError as exc:
                errores.append((n, exc))

    print(f"pedidos válidos:    {len(validos)}")
    print(f"pedidos con fallos: {len(errores)}")
    for n, exc in errores:
        print(f"\n  fila {n}:")
        for e in exc.errors():
            campo = ".".join(str(x) for x in e["loc"])
            recibido = e["input"]
            if isinstance(recibido, dict):
                recibido = "(la fila entera)"
            print(f"    {campo:<8} {e['msg']}  (recibido: {recibido!r})")

    if validos:
        total = sum((p.importe for _, p in validos), Decimal("0"))
        print(f"\nTOTAL de los válidos: {total} EUR")
        print("primer válido, ya convertido:", validos[0][1].model_dump(mode="json"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "datos/pedidos.csv")
