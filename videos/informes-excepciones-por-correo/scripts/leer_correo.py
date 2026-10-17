#!/usr/bin/env python3
"""Paso 5b — LEER el correo que ha llegado.

Se lee por la API del servidor de correo de pruebas (MailHog), que es lo mismo
que abrir la bandeja y mirar: lo que aparece aquí es el correo que se envió de
verdad por SMTP, no un texto escrito a mano.

El informe de SQL Explorer viene como ENLACE (la herramienta publica el CSV y
manda la dirección de descarga), así que con `--informe` se sigue ese enlace y se
enseña el contenido: las excepciones.

Uso:
    python3 scripts/leer_correo.py             # buzon: asunto, de, para
    python3 scripts/leer_correo.py --informe   # ademas, descarga el informe del enlace
"""
import argparse
import json
import re
import urllib.request

MAILHOG = "http://127.0.0.1:8025"


def api(ruta):
    with urllib.request.urlopen(MAILHOG + ruta, timeout=15) as r:
        return json.load(r)


def correos():
    return api("/api/v2/messages").get("items", [])


def cabecera(mensaje, nombre):
    valores = mensaje["Content"]["Headers"].get(nombre) or [""]
    return valores[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--informe", action="store_true")
    args = ap.parse_args()

    recibidos = list(reversed(correos()))    # MailHog devuelve el más nuevo primero
    print(f"buzon de pruebas (127.0.0.1:1025): {len(recibidos)} correo(s) recibido(s)")
    print()
    for n, mensaje in enumerate(recibidos, start=1):
        print(f"[{n}] asunto : {cabecera(mensaje, 'Subject')}")
        print(f"    de     : {cabecera(mensaje, 'From')}")
        print(f"    para   : {cabecera(mensaje, 'To')}")

    if not args.informe:
        return

    # El informe es el correo de la herramienta que trae el enlace de descarga.
    informe = None
    for mensaje in recibidos:
        cuerpo = mensaje["Content"]["Body"]
        if "SQL Explorer" in cabecera(mensaje, "Subject") and "http" in cuerpo:
            informe = mensaje
            break

    print()
    if informe is None:
        print("no hay ningun correo con el enlace del informe")
        return

    cuerpo = informe["Content"]["Body"]
    enlace = re.search(r"https?://\S+", cuerpo).group(0)
    print(f"informe recibido: {cabecera(informe, 'Subject')}")
    print(f"enlace del propio correo: {enlace[:60]}...")
    with urllib.request.urlopen(enlace, timeout=15) as r:
        contenido = r.read().decode("utf-8-sig")   # el CSV de la herramienta trae BOM
    lineas = [l for l in contenido.splitlines() if l.strip()]
    print(f"informe descargado: {len(lineas) - 1} excepciones")
    print()
    for linea in lineas:
        print(f"  {linea}")


if __name__ == "__main__":
    main()
