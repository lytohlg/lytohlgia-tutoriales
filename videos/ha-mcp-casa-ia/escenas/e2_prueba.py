#!/usr/bin/env python3
"""Escena 2 — LA PRUEBA: encender una luz de verdad y verificarlo."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_cliente import call, rpc

from elegir_entidad import elegir
ENTIDAD = elegir()          # una luz real de la casa; si el servidor de demo no tiene
DOM = ENTIDAD.split(".")[0] # ninguna, un switch o un input_boolean (el escenario es el mismo)
P = 2.2

r = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "demo", "version": "1.0"}})
info = r["result"]["serverInfo"]
print(f"cliente MCP  --stdio-->  {info['name']} {info['version']}")
print(f"casa: {os.environ.get('HOMEASSISTANT_URL') or 'https://ha-mcp-demo-server.qc-h.net'}")
rpc("tools/list", {})
time.sleep(P)

antes = json.loads(call("ha_get_state", entity_id=ENTIDAD))["data"]
print(f"\nANTES    {ENTIDAD}  =  {antes['state'].upper()}")
time.sleep(P)

d = json.loads(call("ha_call_service", domain=DOM, service="turn_on", entity_id=ENTIDAD))
print(f"\n> ha_call_service  domain={DOM}  service=turn_on  entity_id={ENTIDAD}")
print(f"   verified_state = {d.get('verified_state')}   ({d.get('message')})")
time.sleep(P)

despues = json.loads(call("ha_get_state", entity_id=ENTIDAD))["data"]
print(f"\nDESPUÉS  {ENTIDAD}  =  {despues['state'].upper()}")
print(f"         last_changed = {despues['last_changed'][:19]}")
print(f"\n>>> {'CAMBIO REAL EN LA CASA' if antes['state'] != despues['state'] else 'SIN CAMBIO'}")
time.sleep(P)

time.sleep(7)
h = json.loads(call("ha_get_history", entity_ids=ENTIDAD, start_time="10m",
                    minimal_response=True, order="desc", limit=2))
print("\nhistorial de Home Assistant:")
for ent in h.get("data", {}).get("entities", []):
    for s in ent.get("states", [])[:2]:
        print(f"   {s.get('last_changed','')[:19]}   {s.get('state')}")
time.sleep(P)

call("ha_call_service", domain=DOM, service="turn_off", entity_id=ENTIDAD)
print("\n(entidad devuelta a su estado inicial)")
time.sleep(3)
