"""Genera el lote de la demo: 240 extractos CSV, tres de ellos con el importe mal escrito.

Uso:  python3 generar_lote.py [n] [--rotos 41,118,203]
El lote es reproducible: la misma semilla da el mismo lote, así que la demo
se puede repetir tal cual desde el paquete didáctico.
"""
import argparse
import csv
import pathlib
import random

CONCEPTOS = [
    "cuota mantenimiento", "licencia anual", "transporte", "material oficina",
    "horas soporte", "hosting", "formacion", "asesoria", "seguro", "dominio",
]
DESTINO = pathlib.Path("lote")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", nargs="?", type=int, default=240)
    ap.add_argument("--rotos", default="41,118,203")
    ap.add_argument("--salida", default=str(DESTINO))
    args = ap.parse_args()

    rotos = {int(x) for x in args.rotos.split(",") if x.strip()}
    destino = pathlib.Path(args.salida)
    destino.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(20261114)

    for i in range(1, args.n + 1):
        ruta = destino / f"extracto_{i:03d}.csv"
        filas = rnd.randint(3, 8)
        with ruta.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["fecha", "concepto", "importe"])
            for k in range(filas):
                dia = rnd.randint(1, 28)
                concepto = rnd.choice(CONCEPTOS)
                importe = round(rnd.uniform(12, 980), 2)
                if i in rotos and k == 1:
                    # El fallo real: coma decimal y símbolo, tal como lo pega
                    # la hoja de cálculo al exportar en español.
                    w.writerow([f"2026-10-{dia:02d}", concepto, f"{importe:.2f}".replace(".", ",") + " EUR"])
                else:
                    w.writerow([f"2026-10-{dia:02d}", concepto, f"{importe:.2f}"])
    print(f"{args.n} ficheros en {destino}/ · con el importe roto: {sorted(rotos)}")


if __name__ == "__main__":
    main()
