"""Servidor de pruebas: simula el proveedor que a veces entrega mal.

Rutas:
  /informe           -> 200 con un CSV correcto (30 filas)
  /informe-503       -> dos primeras peticiones: 503 con pagina de error; despues 200 (fallo transitorio)
  /informe-lento     -> declara 4000 bytes, manda 800 y se queda colgado 60 s
  /informe-truncado  -> declara 5000 bytes, manda 1200 y cierra la conexion
"""
import http.server
import socketserver
import threading
import time

CSV = "fecha;concepto;importe\n" + "".join(
    f"2026-10-{(d % 28) + 1:02d};concepto {d};{(d * 37) % 900 + 100},50\n" for d in range(1, 201)
)
CSV_B = CSV.encode()
HTML_ERR = (b"<html><head><title>503 Service Unavailable</title></head>"
            b"<body><h1>Service Unavailable</h1></body></html>")

_intentos_503 = {"n": 0}


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, fmt, *args):
        pass

    def _ok_csv(self, cuerpo=None):
        cuerpo = cuerpo if cuerpo is not None else CSV_B
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path == "/informe":
            self._ok_csv()
        elif self.path == "/informe-503":
            _intentos_503["n"] += 1
            if _intentos_503["n"] <= 2:
                self.send_response(503)
                self.send_header("Content-Type", "text/html")
                self.send_header("Retry-After", "1")
                self.send_header("Content-Length", str(len(HTML_ERR)))
                self.end_headers()
                self.wfile.write(HTML_ERR)
            else:
                self._ok_csv()
                _intentos_503["n"] = 0   # tras servir bien, el proveedor vuelve a estar sano
        elif self.path == "/informe-lento":
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Length", "4000")
            self.end_headers()
            self.wfile.write(CSV_B[:800])
            self.wfile.flush()
            time.sleep(30)
        elif self.path == "/informe-truncado":
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Length", "5000")
            self.end_headers()
            self.wfile.write(CSV_B[:1200])
            self.wfile.flush()
            # cierra sin completar lo declarado
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def arrancar(puerto=8765):
    srv = Servidor(("127.0.0.1", puerto), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


if __name__ == "__main__":
    import sys
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    s = arrancar(puerto)
    print(f"servidor de pruebas en http://127.0.0.1:{puerto}  (Ctrl+C para parar)")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        s.shutdown()
