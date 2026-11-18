#!/usr/bin/env python3
"""Cuenta piezas en fotos de bandeja con OpenCV puro (sin modelos de IA).

Dos modos:
  · por defecto       -> umbral Otsu + contornos. Rápido, y falla cuando dos piezas
                         se tocan: las dos forman UN solo contorno.
  · --separar-tocadas -> añade transformada de distancia + watershed, que parte las
                         piezas pegadas por el centro de cada una.

Uso:
    python3 contar.py --carpeta fotos --verdad fotos/manifiesto.csv
    python3 contar.py --carpeta fotos --verdad fotos/manifiesto.csv --separar-tocadas
    python3 contar.py --carpeta fotos --salida informe.csv --marcadas marcadas/
"""
import argparse
import csv
import sys
from pathlib import Path

import cv2
import numpy as np

AREA_MIN = 400          # px²: por debajo de esto es ruido, no una pieza
AREA_MAX_FRAC = 0.25    # más de 1/4 de la foto no es una pieza: es la bandeja


def segmentar(gris):
    """Separa pieza (oscura) de bandeja (clara) sin número mágico: Otsu."""
    _, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel, iterations=1)


def area_valida(area, forma):
    """Una pieza tiene un tamaño plausible; el fondo de la bandeja no."""
    alto, ancho = forma[:2]
    return AREA_MIN <= area <= AREA_MAX_FRAC * alto * ancho


def por_contornos(binaria):
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [c for c in contornos if area_valida(cv2.contourArea(c), binaria.shape)]


def semillas(dist):
    """Un máximo local de la distancia = el centro de una pieza."""
    r = float(dist.max())
    if r < 3:
        return np.zeros(dist.shape, np.uint8)
    k = max(3, int(round(0.7 * r)))
    k += 1 - k % 2                                  # ventana impar
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    picos = (dist >= cv2.dilate(dist, kernel) - 1e-4) & (dist > 0.4 * r)
    return picos.astype(np.uint8)


def por_watershed(img, binaria):
    """Parte las piezas pegadas: siembra cada centro y deja competir al agua."""
    dist = cv2.distanceTransform(binaria, cv2.DIST_L2, 5)
    nucleos = semillas(dist)
    if not nucleos.any():
        return []
    n, etiquetas = cv2.connectedComponents(nucleos)
    marcadores = np.zeros(binaria.shape, np.int32)
    marcadores[nucleos > 0] = etiquetas[nucleos > 0] + 1   # semillas: 2..n
    # Sólo el fondo LEJOS de las piezas es cuenca conocida; lo demás queda a 0
    # (desconocido) para que el agua reparta esas zonas entre las semillas.
    lejos = cv2.dilate(binaria, np.ones((5, 5), np.uint8), iterations=3) == 0
    marcadores[lejos] = 1
    cv2.watershed(img, marcadores)                   # los bordes quedan a -1
    piezas = []
    for etiqueta in range(2, n + 1):
        mascara = (marcadores == etiqueta).astype(np.uint8)
        area = int(mascara.sum())
        if not area_valida(area, binaria.shape):
            continue
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contornos:
            piezas.append(max(contornos, key=cv2.contourArea))
    return piezas


def anotar(img, piezas, destino):
    salida = img.copy()
    orden = sorted(piezas, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
    for i, c in enumerate(orden, 1):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(salida, (x, y), (x + w, y + h), (0, 190, 255), 2)
        cv2.putText(salida, str(i), (x + 2, max(y - 6, 14)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 140, 255), 2, cv2.LINE_AA)
    cv2.imwrite(str(destino), salida)


def leer_verdad(ruta):
    verdad = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            verdad[fila["foto"]] = int(fila["piezas"])
    return verdad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carpeta", default=None, help="carpeta con las fotos")
    ap.add_argument("--foto", default=None, help="una sola foto")
    ap.add_argument("--salida", default=None, help="CSV con el recuento por foto")
    ap.add_argument("--marcadas", default=None,
                    help="carpeta donde dejar cada foto marcada con las piezas numeradas")
    ap.add_argument("--separar-tocadas", action="store_true",
                    help="parte con watershed las piezas que se tocan")
    ap.add_argument("--verdad", default=None,
                    help="manifiesto con las piezas que hay de verdad")
    args = ap.parse_args()

    if args.foto:
        rutas = [Path(args.foto)]
    elif args.carpeta:
        rutas = sorted(p for p in Path(args.carpeta).glob("*.png"))
    else:
        sys.exit("hace falta --carpeta o --foto")
    if not rutas:
        sys.exit("no hay fotos .png que contar")

    verdad = leer_verdad(args.verdad) if args.verdad else {}
    if args.marcadas:
        Path(args.marcadas).mkdir(parents=True, exist_ok=True)

    filas = []
    total_contado = total_real = 0
    aciertos = 0
    print(f"{'foto':10s} {'contadas':>8s} {'real':>6s}   estado")
    for ruta in rutas:
        img = cv2.imread(str(ruta))
        if img is None:
            print(f"{ruta.name}: no se puede leer", file=sys.stderr)
            continue
        binaria = segmentar(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        piezas = por_watershed(img, binaria) if args.separar_tocadas else por_contornos(binaria)
        contadas = len(piezas)
        if args.marcadas:
            anotar(img, piezas, Path(args.marcadas) / ruta.name)
        real = verdad.get(ruta.name)
        total_contado += contadas
        if real is None:
            estado = "-"
        else:
            total_real += real
            if contadas == real:
                aciertos += 1
                estado = "OK"
            elif contadas < real:
                estado = f"FALTAN {real - contadas}"
            else:
                estado = f"SOBRAN {contadas - real}"
        filas.append({"foto": ruta.name, "contadas": contadas,
                      "real": "" if real is None else real, "estado": estado})
        print(f"{ruta.name:10s} {contadas:8d} {('' if real is None else real):>6}   {estado}")

    if args.salida:
        with open(args.salida, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["foto", "contadas", "real", "estado"])
            w.writeheader()
            w.writerows(filas)

    print("-" * 34)
    if verdad:
        print(f"{len(filas)} fotos · contadas {total_contado} · de verdad {total_real} · "
              f"acertadas {aciertos}/{len(filas)}")
        if total_contado == total_real:
            print("TOTAL OK: el recuento cuadra con el manifiesto")
        else:
            print(f"TOTAL NO CUADRA: {total_contado} != {total_real}")
    else:
        print(f"{len(filas)} fotos · contadas {total_contado}")


if __name__ == "__main__":
    main()
