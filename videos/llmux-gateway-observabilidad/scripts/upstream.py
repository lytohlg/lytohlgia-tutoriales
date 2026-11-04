#!/usr/bin/env python3
"""Upstream falso: imita OpenAI y Ollama para que la demo sea reproducible sin claves.

Imprime en stdout, por cada peticion, la linea que interesa al video:
  >> POST <ruta> model=gpt-4o-mini X-Team=research auth=<lo que llega>
Asi se ve EXACTAMENTE que manda el gateway hacia el proveedor.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE = "/v1"

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9000


def log(msg):
    print(msg, flush=True)


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def _json(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        auth = self.headers.get("Authorization", "-")
        log(f">> GET {self.path} auth={auth}")
        self._json({"object": "list", "data": [
            {"id": "gpt-4o-mini", "object": "model"},
            {"id": "text-embedding-3-small", "object": "model"},
        ]})

    def do_POST(self):
        body = self._body()
        auth = self.headers.get("Authorization", "-")
        team = self.headers.get("X-Team", "-")
        if self.path.startswith(BASE + "/chat/completions"):
            modelo = body.get("model", "?")
            log(f">> POST {self.path} model={modelo} X-Team={team} auth={auth}")
            if body.get("stream"):
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                for trozo in ("La factura de marzo", " suma 1.240 euros", " y vence el dia 15."):
                    ev = {"choices": [{"delta": {"content": trozo}}]}
                    payload = f"data: {json.dumps(ev, ensure_ascii=False)}\n\n".encode()
                    self.wfile.write(b"%x\r\n%s\r\n" % (len(payload), payload))
                    self.wfile.flush()
                done = b"data: [DONE]\n\n"
                self.wfile.write(b"%x\r\n%s\r\n" % (len(done), done))
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
                return
            self._json({
                "id": "chatcmpl-demo",
                "object": "chat.completion",
                "model": modelo,
                "choices": [{"index": 0, "finish_reason": "stop",
                             "message": {"role": "assistant",
                                         "content": "La factura de marzo suma 1.240 euros y vence el dia 15."}}],
                "usage": {"prompt_tokens": 24, "completion_tokens": 18, "total_tokens": 42},
            })
            return
        if self.path.startswith("/v1/embeddings"):
            log(f">> POST {self.path} auth={auth}")
            self._json({"object": "list", "data": [{"index": 0, "embedding": [0.1, 0.2, 0.3]}],
                        "model": body.get("model", "?")})
            return
        if self.path.startswith("/api/chat"):
            modelo = body.get("model", "?")
            log(f">> POST {self.path} model={modelo} (dialecto ollama)")
            self._json({"model": modelo, "done": True,
                        "message": {"role": "assistant", "content": "respuesta en dialecto ollama"}})
            return
        log(f">> POST {self.path} (no soportado aqui)")
        self._json({"error": "not found"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    log(f"upstream falso escuchando en 127.0.0.1:{PORT}")
    HTTPServer(("127.0.0.1", PORT), H).serve_forever()