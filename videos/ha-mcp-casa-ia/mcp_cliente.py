#!/usr/bin/env python3
"""Cliente MCP mínimo: habla JSON-RPC 2.0 con ha-mcp por stdin/stdout.

- initialize  -> quién es el servidor
- tools/list  -> qué herramientas expone
- tools/call  -> ejecuta una de verdad contra Home Assistant
"""
import json, os, shutil, subprocess, sys, time

DEMO_URL = os.environ.get("HOMEASSISTANT_URL", "https://ha-mcp-demo-server.qc-h.net")
DEMO_TOKEN = os.environ.get("HOMEASSISTANT_TOKEN", "")

if not DEMO_TOKEN:
    # Sin variables de entorno, se leen del .env que está al lado del script.
    _env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(_env):
        # No hay .env: lo prepara preparar_entorno.py (demo público del proyecto)
        subprocess.run([sys.executable,
                        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "preparar_entorno.py")],
                       capture_output=True)
    try:
        with open(_env) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k == "HOMEASSISTANT_URL":
                    DEMO_URL = v.strip()
                elif k == "HOMEASSISTANT_TOKEN":
                    DEMO_TOKEN = v.strip()
    except FileNotFoundError:
        raise SystemExit(f"falta {_env} (o las variables HOMEASSISTANT_URL/TOKEN)")


def _bin():
    for p in (os.environ.get("HA_MCP_BIN"), shutil.which("ha-mcp"),
              "/opt/hamcp-venv/bin/ha-mcp"):
        if p and os.path.exists(p):
            return p
    raise SystemExit("no encuentro el ejecutable ha-mcp (instala con: pip install ha-mcp)")


env = dict(os.environ)
env["HOMEASSISTANT_URL"] = DEMO_URL
env["HOMEASSISTANT_TOKEN"] = DEMO_TOKEN
env.pop("PYTHONPATH", None)

proc = subprocess.Popen([_bin()], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, env=env, text=True, bufsize=1)
_id = [0]


def rpc(method, params=None, timeout=180):
    """Manda una petición JSON-RPC y espera la respuesta con el mismo id."""
    _id[0] += 1
    mid = _id[0]
    msg = {"jsonrpc": "2.0", "id": mid, "method": method}
    if params is not None:
        msg["params"] = params
    assert proc.stdin and proc.stdout
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    t0 = time.time()
    while time.time() - t0 < timeout:
        line = proc.stdout.readline()
        if not line:
            return None
        line = line.strip()
        if not line:
            continue
        try:
            m = json.loads(line)
        except json.JSONDecodeError:
            continue
        if m.get("id") == mid:
            return m
    return None


def call(name, **args):
    r = rpc("tools/call", {"name": name, "arguments": args})
    if r is None:
        return "SIN RESPUESTA"
    res = r.get("result", {})
    parts = [c.get("text", "") for c in res.get("content", []) if c.get("type") == "text"]
    return "\n".join(parts)
