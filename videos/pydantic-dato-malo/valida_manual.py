"""Validador manual, escrito a mano. Es el que casi todos tenemos en producción.

Valida cliente, importe, formato de fecha, estado y (si viene) el email.
Si una fila pasa, se guarda tal cual.
"""
import csv
import re
import sys

FECHA = re.compile(r"^(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})$")
ESTADOS = {"pagado", "pendiente", "cancelado"}


def validar(fila):
    errores = []
    if not fila.get("cliente", "").strip():
        errores.append("cliente vacío")
    try:
        fila["importe"] = float(fila["importe"].replace(",", "."))
    except (KeyError, ValueError):
        errores.append("importe no numérico")
    if not FECHA.match(fila.get("fecha", "")):
        errores.append("fecha con formato raro")
    if fila.get("estado", "").lower() not in ESTADOS:
        errores.append("estado desconocido")
    if fila.get("email") and "@" not in fila["email"]:
        errores.append("email inválido")
    return errores


def main(ruta):
    buenos, rechazados, total = [], [], 0.0
    with open(ruta, newline="", encoding="utf-8") as fh:
        for n, fila in enumerate(csv.DictReader(fh), start=1):
            errores = validar(fila)
            if errores:
                rechazados.append((n, errores))
            else:
                buenos.append(fila)
                total += fila["importe"]
    with open("pedidos_limpios.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "cliente", "email", "importe", "fecha", "estado"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(buenos)
    print(f"filas leídas:      {len(buenos) + len(rechazados)}")
    print(f"pedidos válidos:   {len(buenos)}")
    print(f"pedidos rechazados:{len(rechazados)}")
    for n, errores in rechazados:
        print(f"  fila {n}: {', '.join(errores)}")
    print(f"TOTAL: {total:.2f} EUR")
    print("guardado en pedidos_limpios.csv")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "datos/pedidos.csv")
