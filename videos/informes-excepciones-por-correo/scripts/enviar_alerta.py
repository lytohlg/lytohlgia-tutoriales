#!/usr/bin/env python3
"""Paso 5a — lanzar la alerta: que el informe salga por correo.

SQL Explorer NO trae un comando de consola para enviar un informe. Su disparador
es la vista `email_csv_query` (el botón de correo de su pantalla), que encola la
tarea `explorer.tasks.execute_query`: esa tarea ejecuta la consulta, publica el
informe y manda los correos.

Eso es lo que se lanza aquí, por el mismo camino (la vista, con su permiso y su
petición), y es también lo que se pondría en un cron: no hay atajo, es esto.
"""
from arranque import DESTINO_INFORME, preparar_django

preparar_django()

from django.contrib.auth.models import User                    # noqa: E402
from django.test import Client                                 # noqa: E402
from django.urls import reverse                                # noqa: E402
from explorer.models import Query                              # noqa: E402

TITULO = "Excepciones: pedidos sin servir y facturas vencidas"


def consulta_guardada():
    return Query.objects.get(title=TITULO)


def lanzar_envio(destino=DESTINO_INFORME):
    """Dispara el envío por el camino real de la herramienta. Devuelve (url, respuesta)."""
    consulta = consulta_guardada()
    cliente = Client()
    cliente.force_login(User.objects.get(username="informes"))
    url = reverse("email_csv_query", args=[consulta.id])
    respuesta = cliente.post(
        url,
        {"email": destino},
        headers={"x-requested-with": "XMLHttpRequest"},
    )
    return url, respuesta


if __name__ == "__main__":
    consulta = consulta_guardada()
    url, respuesta = lanzar_envio()

    print("alerta lanzada: el informe se manda por correo")
    print(f"  consulta   {consulta.title}")
    print(f"  ruta       {url.lstrip('/')}   <- el boton de correo de SQL Explorer")
    print(f"  destino    {DESTINO_INFORME}")
    print(f"  respuesta  {respuesta.status_code} {respuesta.content.decode()}")
    print(f"  tarea      explorer.tasks.execute_query (la cola de la herramienta)")
