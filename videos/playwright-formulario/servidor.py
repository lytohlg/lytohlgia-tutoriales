#!/usr/bin/env python3
"""Servidor mínimo de la web de ejemplo: sirve /sitio y recibe el POST del formulario.

Se arranca desde el propio script de prueba (en un hilo), así el demo no necesita
una segunda terminal ni depende de nada externo.
"""
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))
SITIO = os.path.join(AQUI, "sitio")
BUZON = os.path.join(AQUI, "mensajes.jsonl")


class Manejador(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=SITIO, **kw)

    def _json(self, codigo, cuerpo):
        datos = json.dumps(cuerpo, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_POST(self):
        if self.path != "/enviar":
            self._json(404, {"ok": False, "mensaje": "no existe"})
            return
        largo = int(self.headers.get("Content-Length") or 0)
        crudo = self.rfile.read(largo).decode("utf-8", "replace")
        try:
            datos = json.loads(crudo)
        except json.JSONDecodeError:
            self._json(400, {"ok": False, "mensaje": "cuerpo no válido"})
            return
        nombre = (datos.get("nombre") or "").strip()
        if not nombre:
            self._json(400, {"ok": False, "mensaje": "falta el nombre"})
            return
        with open(BUZON, "a", encoding="utf-8") as f:
            f.write(json.dumps(datos, ensure_ascii=False) + "\n")
        self._json(200, {"ok": True, "mensaje": f"Gracias, {nombre}: hemos recibido tu mensaje"})

    def log_message(self, format, *args):  # noqa: A002 - firma que exige la librería
        pass


def arrancar(puerto=8000):
    srv = ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    import threading
    h = threading.Thread(target=srv.serve_forever, daemon=True)
    h.start()
    return srv
