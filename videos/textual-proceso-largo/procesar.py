"""El trabajo de verdad: leer un extracto CSV, validar los importes y escribir un JSON.

No sabe nada de pantallas. Lo usan igual el print de siempre (lote_print.py) y el
panel de Textual (panel.py): misma función, dos formas de mirarla.
"""
import csv
import json
import pathlib

LOTE = pathlib.Path("lote")
SALIDA = pathlib.Path("salida")


def ficheros():
    """Los extractos pendientes, en orden. Se recalcula: el lote puede cambiar."""
    return sorted(LOTE.glob("*.csv"))


def procesar(ruta, salida=SALIDA):
    """Devuelve (filas, total). Lanza ValueError si un importe no es un número.

    El importe se valida con float() a propósito, sin limpiar comas: si el
    fichero trae '12,50 EUR' el error tiene que verse, no esconderse.
    """
    salida.mkdir(parents=True, exist_ok=True)
    with ruta.open(encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    total = 0.0
    for n, fila in enumerate(filas, 1):
        try:
            total += float(fila["importe"])
        except (TypeError, ValueError):
            raise ValueError(f"fila {n}: importe no válido '{fila['importe']}'") from None
    destino = salida / (ruta.stem + ".json")
    destino.write_text(
        json.dumps({"fichero": ruta.name, "filas": len(filas), "total": round(total, 2)},
                   ensure_ascii=False),
        encoding="utf-8",
    )
    return len(filas), round(total, 2)
