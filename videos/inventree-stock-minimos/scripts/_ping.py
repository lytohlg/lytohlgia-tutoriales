#!/usr/bin/env python3
"""Espera a que la API de InvenTree responda e imprime su versión."""
import json
import time
import urllib.request

for intento in range(30):
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/api/", timeout=3) as r:
            info = json.loads(r.read().decode())
        print(f"API viva · InvenTree {info['version']} · API v{info['apiVersion']}")
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("la API no respondió")
