#!/usr/bin/env python3
"""Escena 4 — EL DETALLE: qué viaja por el tubo (JSON-RPC 2.0)."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_cliente import call, rpc
from elegir_entidad import elegir

P = 2.4

ENTIDAD = elegir()           # la misma entidad real que usa la escena 2
DOM = ENTIDAD.split(".")[0]
OBJ = ENTIDAD.split(".", 1)[1].replace("_", " ")

rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "demo", "version": "1.0"}})
rpc("tools/list", {})

peticion = {"jsonrpc": "2.0", "id": 7, "method": "tools/call",
            "params": {"name": "ha_search",
                       "arguments": {"query": OBJ, "domain_filter": DOM}}}
print("ENVÍA el cliente:")
print(json.dumps(peticion, ensure_ascii=False))
time.sleep(P)

resp = call("ha_search", query=OBJ, domain_filter=DOM, limit=3)
print("\nRESPONDE el servidor:")
corte = resp.find('"entity_total_matches"')
print(resp[:corte + 26] + ' …}' if corte > 0 else resp[:400])
time.sleep(P)

print("\nENTIDAD ENCONTRADA:")
d = json.loads(resp)
for e in d.get("entities", [])[:1]:
    print(f"   {e['entity_id']}   {e['state']}   {e.get('friendly_name')}")
time.sleep(P)

e = json.loads(call("ha_get_state", entity_id=ENTIDAD))["data"]
print("\nATRIBUTOS QUE LA IA NECESITA PARA DECIDIR:")
for k in ("state", "entity_id", "last_changed"):
    print(f"   {k:<14} {str(e.get(k))[:60]}")
at = e.get("attributes") or {}
for k in list(at)[:4]:
    print(f"   {k:<14} {str(at[k])[:60]}")
time.sleep(3)
