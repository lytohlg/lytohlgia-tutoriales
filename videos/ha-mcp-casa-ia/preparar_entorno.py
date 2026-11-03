#!/usr/bin/env python3
"""Prepara el entorno de la demo: deja un .env utilizable en la carpeta de trabajo.

Orden de prioridad:
  1. Variables de entorno HOMEASSISTANT_URL / HOMEASSISTANT_TOKEN (tu casa).
  2. Un .env que ya exista en esta carpeta.
  3. El servidor de DEMO público del proyecto: la URL sale de scripts/install.sh y
     el token del propio código (src/ha_mcp/config_settings.py). Los dos están
     publicados en el repositorio, así que no se guarda ningún secreto aquí.
     Esa casa es compartida y se resetea: sirve para probar, no para producción.
"""
import os
import re
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(AQUI, ".env")
RAW = "https://raw.githubusercontent.com/homeassistant-ai/ha-mcp/master/"
FUENTES = {
    "url": "scripts/install.sh",
    "token": "src/ha_mcp/config_settings.py",
}


def _leer(path):
    with urllib.request.urlopen(RAW + path, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    url = os.environ.get("HOMEASSISTANT_URL", "").strip()
    tok = os.environ.get("HOMEASSISTANT_TOKEN", "").strip()

    if not (url and tok) and os.path.exists(ENV):
        for line in open(ENV):
            if line.startswith("HOMEASSISTANT_URL="):
                url = url or line.split("=", 1)[1].strip()
            elif line.startswith("HOMEASSISTANT_TOKEN="):
                tok = tok or line.split("=", 1)[1].strip()

    if not (url and tok):
        print("· sin .env ni variables: uso el servidor de DEMO del proyecto")
        try:
            if not url:
                m = re.search(r"https://ha-mcp-demo-server[^\s\"']*", _leer(FUENTES["url"]))
                url = m.group(0).rstrip('",;') if m else ""
            if not tok:
                t = re.search(r"eyJ[A-Za-z0-9._-]{40,}", _leer(FUENTES["token"]))
                tok = t.group(0) if t else ""
        except Exception as e:
            print("❌ no puedo leer el repositorio del proyecto:", e)
        if not (url and tok):
            print("❌ no encuentro la URL/token del demo en el repositorio del proyecto")
            print("   crea un .env con HOMEASSISTANT_URL y HOMEASSISTANT_TOKEN")
            return 1

    with open(ENV, "w") as f:
        f.write(f"HOMEASSISTANT_URL={url}\nHOMEASSISTANT_TOKEN={tok}\n")
    print(f"· entorno listo: {url}")
    print(f"· token del demo: {tok[:8]}…{tok[-4:]} ({len(tok)} caracteres, público en el repo)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
