#!/usr/bin/env python3
"""Deja tres correos en el buzon de pruebas: se envian DE VERDAD por SMTP
al servidor de correo local (GreenMail), no se escriben a mano en ninguna carpeta.
Uso: python3 sembrar.py [--vacio]
"""
import smtplib
import sys
from email.message import EmailMessage
from email.utils import formatdate

HOST, PORT = "127.0.0.1", 3025          # SMTP del buzon de pruebas
DESTINO = "compras@example.com"          # buzon de pruebas (usuario del servidor local)

FACTURA_CSV = (
    "concepto;importe;vencimiento\n"
    "Tornilleria M8;148,20;30/10/2026\n"
    "Cable apantallado 25m;96,50;30/10/2026\n"
)

CORREOS = [
    {
        "id": "<demo-4471@example.com>",
        "de": "facturacion@example.com",
        "asunto": "Factura 2026-4471 - vence el 30/10/2026",
        "texto": (
            "Buenos dias,\n\n"
            "Adjuntamos la factura 2026-4471 correspondiente al pedido de octubre.\n"
            "El pago vence el 30/10/2026.\n\n"
            "Un saludo,\nSuministros Norte\n"
        ),
        "adjunto": ("factura_2026-4471.csv", FACTURA_CSV),
    },
    {
        "id": "<demo-88a@example.org>",
        "de": "pedidos@example.org",
        "asunto": "Presupuesto 88-A - necesitamos respuesta antes del 22/10/2026",
        "texto": (
            "Hola,\n\n"
            "Te paso el presupuesto 88-A de las estanterias del almacen 2.\n"
            "Necesitamos respuesta antes del 22/10/2026 para reservar el material.\n\n"
            "Gracias,\nFerreteria Vega\n"
        ),
        "adjunto": None,
    },
    {
        "id": "<demo-ofertas-19@example.net>",
        "de": "newsletter@example.net",
        "asunto": "Ofertas de la semana: tornilleria y abrasivos",
        "texto": (
            "Ofertas de la semana.\n\n"
            "Tornilleria -15%, abrasivos -10%. Solo hasta el domingo.\n"
        ),
        "adjunto": None,
    },
]


def enviar(cfg):
    m = EmailMessage()
    m["From"] = cfg["de"]
    m["To"] = DESTINO
    m["Subject"] = cfg["asunto"]
    m["Date"] = formatdate(localtime=True)
    m["Message-ID"] = cfg["id"]
    m.set_content(cfg["texto"])
    if cfg.get("adjunto"):
        nombre, contenido = cfg["adjunto"]
        m.add_attachment(contenido.encode("utf-8"), maintype="text",
                         subtype="csv", filename=nombre)
    with smtplib.SMTP(HOST, PORT, timeout=15) as s:
        s.send_message(m)


def main():
    if "--vacio" in sys.argv:
        CORREOS.clear()
    for cfg in CORREOS:
        enviar(cfg)
        print(f"  enviado  {cfg['de']:44s}  {cfg['asunto'][:46]}")
    print(f"\n{len(CORREOS)} correos entregados en el buzon {DESTINO} "
          f"(SMTP {HOST}:{PORT})")


if __name__ == "__main__":
    main()
