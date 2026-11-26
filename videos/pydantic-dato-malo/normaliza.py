"""Dos reglas que el contrato de pydantic NO trae de fábrica y se añaden aquí:

  1. Coma decimal: «12,50» llega así desde Excel en español. Pydantic, con Decimal,
     lo rechaza. Se normaliza ANTES de validar (mode="before").
  2. Regla de negocio: un pedido pagado no puede quedar sin fecha de pago... aquí,
     más simple y comprobable: el estado se admite en mayúsculas y se guarda en minúsculas.

El resto sigue siendo declarativo: no se reescribe ninguna de las comprobaciones.
"""
import csv
import sys
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError, field_validator


class Pedido(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: int = Field(gt=0)
    cliente: str = Field(min_length=2)
    email: EmailStr
    importe: Decimal = Field(gt=0, le=5000, decimal_places=2)
    fecha: date
    estado: Literal["pagado", "pendiente", "cancelado"]

    @field_validator("importe", mode="before")
    @classmethod
    def coma_decimal(cls, v):
        if isinstance(v, str) and "," in v:
            return v.replace(".", "").replace(",", ".")
        return v

    @field_validator("estado", mode="before")
    @classmethod
    def estado_en_minusculas(cls, v):
        return v.strip().lower() if isinstance(v, str) else v


def main(ruta):
    validos, errores = [], []
    with open(ruta, newline="", encoding="utf-8") as fh:
        for n, fila in enumerate(csv.DictReader(fh), start=1):
            try:
                validos.append((n, Pedido.model_validate(fila)))
            except ValidationError as exc:
                errores.append((n, exc))

    print(f"válidos: {len(validos)} · con fallos: {len(errores)}")
    for n, exc in errores:
        for e in exc.errors():
            campo = ".".join(str(x) for x in e["loc"])
            print(f"  fila {n}  {campo:<8} {e['msg']}")
    for n, p in validos:
        print(f"  fila {n}  id={p.id} importe={p.importe} ({type(p.importe).__name__}) "
              f"fecha={p.fecha} ({type(p.fecha).__name__}) estado={p.estado!r}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "datos/pedidos.csv")
