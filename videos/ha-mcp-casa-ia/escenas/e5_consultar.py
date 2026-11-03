#!/usr/bin/env python3
"""Escena 5 — PREGUNTAR: la casa entera en una llamada, y cálculos dentro."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_cliente import call, rpc

P = 2.2

rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "demo", "version": "1.0"}})
rpc("tools/list", {})

d = json.loads(call("ha_get_overview"))
s = d["system_summary"]
print("ha_get_overview:")
print(f"   entidades : {s['total_entities']}")
print(f"   dominios  : {s['total_domains']}")
print(f"   servicios : {s['total_services']}")
print(f"   áreas     : {s['total_areas']}")
print(f"   versión HA: {s['version']}")
time.sleep(P)

print("\nha_eval_template — contar luces encendidas:")
print('   {{ states.light | selectattr("state","eq","on") | list | count }}')
print("   ->", json.loads(call("ha_eval_template",
      template='{{ states.light | selectattr("state","eq","on") | list | count }}'))["result"])
time.sleep(P)

print("\nha_eval_template — sensores de temperatura:")
print("   ->", json.loads(call("ha_eval_template",
      template="{{ states.sensor | selectattr('attributes.device_class','eq','temperature') | list | count }}"))["result"])
time.sleep(P)

print("\nlas temperaturas ahora:")
t = json.loads(call("ha_eval_template", template=(
    "{% for s in states.sensor if s.attributes.device_class == 'temperature' %}"
    "{{ s.name }}={{ s.state }}; {% endfor %}")))["result"]
for trozo in t.split(";"):
    if trozo.strip():
        print("   " + trozo.strip())
time.sleep(3)
