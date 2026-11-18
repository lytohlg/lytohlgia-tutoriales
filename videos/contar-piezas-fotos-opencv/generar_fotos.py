#!/usr/bin/env python3
"""Genera fotos sintéticas de bandejas con un número CONOCIDO de piezas.

Motivo: para comprobar si un contador acierta hace falta saber la respuesta.
Con fotos reales no la sabemos sin contarlas a mano (que es justo lo que
queremos evitar), así que aquí dibujamos piezas de un tamaño fijo, algunas
tocándose, y anotamos cuántas hay de verdad en manifiesto.csv.

Uso:
    python3 generar_fotos.py --salida fotos
    python3 generar_fotos.py --salida dificiles --solape 0.6 --solo p10

--solape es cuánto se pisan dos piezas del mismo grupo (0.30 = un 30%).
--solo genera únicamente las fotos que le nombres (por coma).
"""
import argparse
import csv
import random
from pathlib import Path

import cv2
import numpy as np

RADIO = 26          # radio de la pieza, en píxeles
ANCHO, ALTO = 800, 600
SEMILLA = 20261118

# Plano de cada foto: grupos de piezas. tocandose=True -> se solapan un poco.
PLAN = [
    ("p01", [(5, False)]),
    ("p02", [(4, False)]),
    ("p03", [(3, False), (2, True)]),
    ("p04", [(6, False)]),
    ("p05", [(2, False), (3, True)]),
    ("p06", []),                        # bandeja vacía
    ("p07", [(4, False)]),
    ("p08", [(1, False), (2, True), (2, True)]),
    ("p09", [(3, False)]),
    ("p10", [(1, False), (4, True)]),
    ("p11", [(2, False)]),
    ("p12", [(3, False)]),
]


def centros_grupo(cx, cy, n, tocandose, rng, solape):
    """Devuelve los centros de un grupo de n piezas alrededor de (cx, cy)."""
    if n == 1:
        return [(cx, cy)]
    if not tocandose:
        # separadas: en fila, con hueco entre bordes
        paso = 2 * RADIO + 12
        x0 = cx - paso * (n - 1) / 2
        return [(x0 + i * paso, cy) for i in range(n)]
    # tocándose: fila de piezas que se pisan `solape` (0,30 = un 30%), girada al azar
    paso = (2 - solape) * RADIO
    ang = rng.uniform(0, np.pi)
    ux, uy = np.cos(ang), np.sin(ang)
    x0 = -(n - 1) * paso / 2
    return [(cx + (x0 + i * paso) * ux, cy + (x0 + i * paso) * uy) for i in range(n)]


def colocar(grupos, rng, solape):
    """Coloca los grupos sin que se pisen entre ellos (rechazo simple)."""
    posiciones = []
    for n, tocandose in grupos:
        for _ in range(500):
            cx = rng.uniform(90, ANCHO - 90)
            cy = rng.uniform(90, ALTO - 90)
            nuevos = centros_grupo(cx, cy, n, tocandose, rng, solape)
            ok = True
            for (x, y) in nuevos:
                if not (RADIO + 12 <= x <= ANCHO - RADIO - 12):
                    ok = False
                    break
                if not (RADIO + 12 <= y <= ALTO - RADIO - 12):
                    ok = False
                    break
                for (px, py) in posiciones:
                    if np.hypot(x - px, y - py) < 2 * RADIO + 26:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                posiciones.extend(nuevos)
                break
        else:
            raise SystemExit("no hay sitio para colocar el grupo: revisa el plan")
    return posiciones


def dibujar(centros, ruido):
    # bandeja: gris claro con un degradado suave y algo de ruido de sensor
    base = np.linspace(200, 222, ALTO).reshape(ALTO, 1).repeat(ANCHO, axis=1)
    img = base.astype(np.float32)
    img += ruido.normal(0, 2.5, img.shape)
    img = np.clip(img, 0, 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for (x, y) in centros:
        cv2.circle(img, (int(round(x)), int(round(y))), RADIO, (58, 62, 68), -1,
                   lineType=cv2.LINE_AA)
    # un pelín de desenfoque: así el borde no es perfecto, como en una foto
    return cv2.GaussianBlur(img, (3, 3), 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="fotos")
    ap.add_argument("--solape", type=float, default=0.30,
                    help="cuánto se pisan dos piezas que se tocan (0.30 = 30%%)")
    ap.add_argument("--solo", default=None,
                    help="genera solo estas fotos, por coma (p.ej. p10 o p03,p10)")
    args = ap.parse_args()

    rng = random.Random(SEMILLA)
    ruido = np.random.default_rng(SEMILLA + 1)
    destino = Path(args.salida)
    destino.mkdir(parents=True, exist_ok=True)

    plan = PLAN
    if args.solo:
        pedidas = [s.strip() for s in args.solo.split(",") if s.strip()]
        plan = [f for f in PLAN if f[0] in pedidas]
        if not plan:
            raise SystemExit(f"ninguna de esas fotos está en el plan: {', '.join(p[0] for p in PLAN)}")

    filas = []
    total = 0
    for nombre, grupos in plan:
        centros = colocar(grupos, rng, args.solape)
        img = dibujar(centros, ruido)
        cv2.imwrite(str(destino / f"{nombre}.png"), img)
        n = len(centros)
        total += n
        filas.append((f"{nombre}.png", n))
        print(f"{nombre}.png  {n:2d} piezas")

    with (destino / "manifiesto.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["foto", "piezas"])
        w.writerows(filas)

    print(f"\n{len(filas)} fotos · {total} piezas en total · manifiesto: {destino / 'manifiesto.csv'}")


if __name__ == "__main__":
    main()
