#!/usr/bin/env python3
"""Elige una entidad REAL de esta casa para la demo (luz, mejor apagada; si no, un switch).

Por qué existe: el servidor de demo que trae el paquete es compartido y se resetea, así que
los nombres de entidad cambian con el tiempo. En el vídeo se encendió
`light.wohnzimmer_beleuchtung`; si esa entidad ya no está, la prueba coge la primera luz
disponible para que el escenario siga siendo el mismo (encender algo y VERIFICAR que cambió)
sin depender de un nombre concreto.

Salida: el entity_id por stdout (y nada más). Código 1 si la casa no tiene ninguna entidad
que se pueda encender.
"""
import json
import os
import sys
import urllib.request

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _credenciales() -> tuple[str, str]:
    url = os.environ.get("HOMEASSISTANT_URL", "")
    token = os.environ.get("HOMEASSISTANT_TOKEN", "")
    if url and token:
        return url.rstrip("/"), token
    env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if not os.path.exists(env):
        raise SystemExit("falta .env (lo genera preparar_entorno.py)")
    for linea in open(env, encoding="utf-8"):
        linea = linea.strip()
        if linea.startswith("HOMEASSISTANT_URL="):
            url = linea.split("=", 1)[1].strip()
        elif linea.startswith("HOMEASSISTANT_TOKEN="):
            token = linea.split("=", 1)[1].strip()
    if not url or not token:
        raise SystemExit(".env sin HOMEASSISTANT_URL/HOMEASSISTANT_TOKEN")
    return url.rstrip("/"), token


def estados() -> list[dict]:
    url, token = _credenciales()
    recurso = "states"
    req = urllib.request.Request(f"{url}/api/{recurso}",
                                headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def elegir() -> str:
    entidades = estados()
    for dominio in ("light", "switch", "input_boolean"):
        candidatos = [e for e in entidades if e["entity_id"].startswith(dominio + ".")]
        if not candidatos:
            continue
        apagadas = [e for e in candidatos if e.get("state") in ("off", "unknown", "unavailable")]
        elegida = (apagadas or candidatos)[0]
        # Deja constancia en stderr: stdout es solo el id (lo capturan las escenas).
        print(f"entidad elegida: {elegida['entity_id']} ({dominio}, estado={elegida['state']})",
              file=sys.stderr)
        return elegida["entity_id"]
    raise SystemExit("esta casa no tiene luces ni switches que encender")


if __name__ == "__main__":
    print(elegir())
