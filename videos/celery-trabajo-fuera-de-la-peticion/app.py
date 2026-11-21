"""La web: dos formas de pedir exactamente el mismo informe.

  /informe?cliente=ACME        -> hace el trabajo DENTRO de la petición (8 s de espera)
  /informe-cola?cliente=ACME   -> lo encola y contesta al instante con el identificador
  /estado?id=<id>              -> pregunta cómo va la tarea
  /cobro-cola?cliente=ACME     -> tarea que siempre falla, para ver los reintentos

Servidor de la biblioteca estándar: lo único que hay que instalar es celery y redis.
"""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from celery.result import AsyncResult

from tareas import app as app_celery
from tareas import cobro, informe


def trabajo_pesado(cliente: str) -> dict:
    """El mismo trabajo que hace la tarea, pero aquí dentro de la petición."""
    time.sleep(8)
    return {"cliente": cliente, "lineas": 1200}


class Manejador(BaseHTTPRequestHandler):
    def _json(self, codigo: int, datos: dict) -> None:
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self) -> None:  # noqa: N802 (nombre impuesto por la biblioteca)
        try:
            self._atiende()
        except Exception as exc:  # que un fallo se vea como JSON, no como conexion cortada
            import traceback
            traceback.print_exc()
            try:
                self._json(500, {"error": f"{type(exc).__name__}: {exc}"})
            except Exception:
                pass

    def _atiende(self) -> None:
        ruta = urlparse(self.path)
        q = parse_qs(ruta.query)
        cliente = (q.get("cliente") or ["ACME"])[0]

        if ruta.path == "/informe":
            t0 = time.perf_counter()
            resultado = trabajo_pesado(cliente)
            self._json(200, {
                "como": "dentro de la peticion",
                "espera_s": round(time.perf_counter() - t0, 3),
                "resultado": resultado,
            })
            return

        if ruta.path == "/informe-cola":
            t0 = time.perf_counter()
            tarea = informe.delay(cliente)
            self._json(200, {
                "como": "encolada",
                "espera_s": round(time.perf_counter() - t0, 3),
                "tarea": tarea.id,
            })
            return

        if ruta.path == "/cobro-cola":
            tarea = cobro.delay(cliente)
            self._json(200, {"tarea": tarea.id, "estado_inicial": tarea.state})
            return

        if ruta.path == "/estado":
            ident = (q.get("id") or [""])[0]
            r = AsyncResult(ident, app=app_celery)
            self._json(200, {"id": ident, "estado": r.state, "resultado": r.result
                             if r.successful() else None})
            return

        self._json(404, {"error": "ruta desconocida", "rutas": [
            "/informe", "/informe-cola", "/cobro-cola", "/estado"]})

    def log_message(self, formato: str, *args) -> None:
        """Sin ruido: los tiempos los imprime curl, que es lo que se mide."""


if __name__ == "__main__":
    print("web escuchando en http://127.0.0.1:8000", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8000), Manejador).serve_forever()
