#!/usr/bin/env python3
"""Avisos de stock bajo sobre Simple Stock Management.

Consulta la API del almacén y avisa cuando un artículo baja del mínimo.

La regla, entera:
  1. Un artículo con menos unidades que el mínimo es un AVISO.
  2. Un aviso se da UNA sola vez. Mientras siga bajo, no vuelve a sonar.
  3. Si el artículo se repone por encima del mínimo, deja de estar en la lista.
  4. Si vuelve a bajar, vuelve a avisar: el estado no es un histórico, es «de qué
     te he avisado ya y sigue pendiente».
  5. Si la API no responde, NO se avisa de nada: se grita el error. Un fallo de red
     no puede parecerse a «todo está bien».

Uso:
    python3 scripts/avisos_stock.py [--minimo 10] [--api URL] [--estado RUTA] [--olvidar]

Devuelve 0 si pudo consultar, 2 si no pudo hablar con la API y 3 si el login falló.
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LOGIN = "/accounts/login/"


def carga_env(ruta: pathlib.Path) -> None:
    """Lee un .env sencillo (CLAVE=valor) sin pisar lo que ya venga del entorno."""
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        os.environ.setdefault(clave.strip(), valor.strip().strip("'\""))


class Cliente:
    """Cliente mínimo: sesión con cookies y login contra la vista de Django."""

    def __init__(self, api: str, usuario: str, clave: str):
        self.api = api.rstrip("/")
        self.usuario = usuario
        self.clave = clave
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies)
        )

    def _abre(self, peticion: urllib.request.Request):
        return self.opener.open(peticion, timeout=15)

    def login(self) -> None:
        pagina = self._abre(urllib.request.Request(self.api + LOGIN)).read().decode()
        csrf = self._busca_csrf(pagina)
        datos = urllib.parse.urlencode(
            {"username": self.usuario, "password": self.clave, "csrfmiddlewaretoken": csrf}
        ).encode()
        peticion = urllib.request.Request(
            self.api + LOGIN, data=datos, headers={"Referer": self.api + LOGIN}
        )
        respuesta = self._abre(peticion)
        if "csrfmiddlewaretoken" in respuesta.read().decode():
            raise PermissionError("el login no ha entrado (usuario o clave incorrectos)")

    @staticmethod
    def _busca_csrf(html: str) -> str:
        encontrado = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
        if not encontrado:
            raise RuntimeError("no encuentro el token CSRF en la página de login")
        return encontrado.group(1)

    def articulos(self) -> list[dict]:
        """Todos los artículos del almacén, página a página."""
        salida: list[dict] = []
        pagina = 1
        while True:
            url = f"{self.api}/" + "api/items/?page=%d&page_size=100" % pagina
            respuesta = self._abre(urllib.request.Request(url))
            datos = json.loads(respuesta.read().decode())
            resultados = datos.get("results", [])
            salida.extend(resultados)
            if not resultados or pagina >= int(datos.get("total_pages") or 1):
                return salida
            pagina += 1


def lee_estado(ruta: pathlib.Path) -> dict:
    if not ruta.exists():
        return {}
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def escribe_estado(ruta: pathlib.Path, estado: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(estado, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    carga_env(RAIZ / ".env")
    parser = argparse.ArgumentParser(description="Avisa cuando el stock baja del mínimo.")
    parser.add_argument("--minimo", type=int, default=int(os.environ.get("AVISO_MINIMO", 10)))
    parser.add_argument("--api", default=os.environ.get("AVISO_API", "http://127.0.0.1:8000"))
    parser.add_argument("--estado", default=str(RAIZ / "salida" / "avisos_estado.json"))
    parser.add_argument(
        "--olvidar",
        action="store_true",
        help="borra los avisos ya dados y vuelve a empezar (para repetir la demo)",
    )
    opciones = parser.parse_args()

    estado_ruta = pathlib.Path(opciones.estado)
    if opciones.olvidar and estado_ruta.exists():
        estado_ruta.unlink()

    usuario = os.environ.get("DEMO_USUARIO_ALMACEN", "almacen")
    clave = os.environ.get("DEMO_ALMACEN_CLAVE", "")

    print("== Avisos de stock ==")
    print(f"API: {opciones.api}   minimo: {opciones.minimo} unidades   estado: {estado_ruta}")

    cliente = Cliente(opciones.api, usuario, clave)
    try:
        cliente.login()
        articulos = cliente.articulos()
    except PermissionError as fallo:
        print(f"ERROR: {fallo}", file=sys.stderr)
        return 3
    except (urllib.error.URLError, OSError, ValueError, RuntimeError) as fallo:
        print(f"ERROR: no se pudo consultar la API ({opciones.api}): {fallo}", file=sys.stderr)
        print("       el almacen no ha contestado: NO hay datos de stock", file=sys.stderr)
        return 2

    estado = lee_estado(estado_ruta)
    nuevos, repuestos, sanos = [], [], 0

    for articulo in articulos:
        sku = str(articulo.get("sku", "?"))
        descripcion = str(articulo.get("description", ""))
        try:
            unidades = int(articulo.get("quantity") or 0)
        except (TypeError, ValueError):
            unidades = 0
        if unidades < opciones.minimo:
            if sku not in estado:
                nuevos.append((sku, descripcion, unidades))
            estado[sku] = {"unidades": unidades, "minimo": opciones.minimo, "descripcion": descripcion}
        else:
            sanos += 1
            if sku in estado:
                repuestos.append((sku, descripcion, unidades))
                del estado[sku]

    for sku, descripcion, unidades in nuevos:
        print(f"AVISO  {sku:<9} {descripcion:<28} {unidades} unidades (minimo {opciones.minimo})")
    for sku, descripcion, unidades in repuestos:
        print(f"REPUESTO  {sku:<9} {descripcion:<26} {unidades} unidades (ya no se avisa)")

    escribe_estado(estado_ruta, estado)
    print(
        f"\n{len(nuevos)} avisos nuevos · {len(repuestos)} repuestos · "
        f"{sanos} articulos por encima del minimo · {len(estado)} pendientes de reponer"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
