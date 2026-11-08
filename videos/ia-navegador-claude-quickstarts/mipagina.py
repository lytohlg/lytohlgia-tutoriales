"""Mi página: el mismo driver del repo contra una página con formulario.

Sirve una página local, lanza CdpBrowser con una política que admite solo esa
página y envía las llamadas que mandaría un modelo. Imprime lo que vería el modelo.
"""
from __future__ import annotations

import json
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from anthropic.tools import ToolError
from anthropic.tools.browser import BetaURLContext, BetaURLPolicy
from anthropic.types.beta import BetaToolUseBlock

from cdp_browser import CdpBrowser

INICIO = b"""<!doctype html>
<title>Facturas</title>
<h1>Facturas de octubre</h1>
<p>Tienes 3 facturas pendientes de revisar.</p>
<form action="/enviar" method="post">
  <label for="email">Correo</label>
  <input id="email" name="email" type="email" placeholder="alguien@example.com">
  <label for="plan">Plan</label>
  <select id="plan" name="plan"><option>basico</option><option>pro</option></select>
  <button type="submit">Enviar</button>
</form>
<p><a href="/facturas">Ver el listado</a></p>
"""

LISTADO = b"""<!doctype html>
<title>Listado</title>
<h1>Listado de facturas</h1>
<p>F-101 120,00 EUR</p>
<p>F-102 89,50 EUR</p>
<p>F-103 240,00 EUR</p>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = LISTADO if self.path.startswith("/facturas") else INICIO
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args) -> None:
        pass


def solo(origin: str) -> BetaURLPolicy:
    def policy(_ctx: BetaURLContext, url: str) -> None:
        try:
            parts = urlsplit(url.replace("\\", "/"))
        except ValueError:
            raise ToolError(f"blocked: {url} no se puede leer") from None
        if f"{parts.scheme}://{parts.netloc}" != origin:
            raise ToolError(f"blocked: {url} no es la página de este ejercicio")

    return policy


def llamar(browser, nombre: str, entrada: dict) -> str:
    uso = BetaToolUseBlock(type="tool_use", id=f"toolu_{nombre}", name=nombre,
                           input=entrada, toolset_name="browser")
    res = browser.tool_result(uso)
    print(f"\n{nombre} {json.dumps(entrada, ensure_ascii=False)} -> "
          f"{'rechazado' if res.get('is_error') else 'respondido'}")
    salida = ""
    for bloque in res.get("content", []):
        if isinstance(bloque, dict) and bloque.get("type") == "text":
            salida += str(bloque.get("text", ""))
            print("  " + str(bloque.get("text", "")))
        elif isinstance(bloque, dict):
            print("  [" + str(bloque.get("type")) + "]")
    return salida


def main() -> None:
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    origen = f"http://localhost:{srv.server_port}"
    browser = CdpBrowser(headless=True, url_policy=solo(origen))
    with browser:
        llamar(browser, "navigate", {"url": f"{origen}/"})
        arbol = llamar(browser, "read_page", {})
        linea = next((l for l in arbol.splitlines() if "Ver el listado" in l), "")
        ref = re.search(r"ref_\d+", linea)
        print(f"\n>>> el enlace del listado es {ref.group() if ref else 'NO ENCONTRADO'}")
        llamar(browser, "left_click", {"target": {"type": "ref", "ref": ref.group()}})
        llamar(browser, "get_page_text", {})
        llamar(browser, "navigate", {"url": "https://example.com"})
    srv.shutdown()
    print("\nfin")


if __name__ == "__main__":
    main()
