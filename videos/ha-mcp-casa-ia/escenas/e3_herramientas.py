#!/usr/bin/env python3
"""Escena 3 — LAS HERRAMIENTAS: qué expone el servidor."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_cliente import rpc

P = 2.2

r = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "demo", "version": "1.0"}})
print("servidor :", r["result"]["serverInfo"])
print("protocolo:", r["result"]["protocolVersion"])
time.sleep(P)

r = rpc("tools/list", {})
tools = r["result"]["tools"]
print(f"\nherramientas: {len(tools)}")
time.sleep(P)

fam = {}
for t in tools:
    partes = t["name"].split("_")
    k = partes[1] if len(partes) >= 3 else "otros"
    fam[k] = fam.get(k, 0) + 1
for k, v in sorted(fam.items(), key=lambda x: -x[1])[:8]:
    print(f"   {k:<10} {v:>3}")
time.sleep(P)

print("\nlas que uso en este vídeo:")
for n in ("ha_search", "ha_get_state", "ha_call_service", "ha_get_history", "ha_eval_template"):
    t = next((x for x in tools if x["name"] == n), None)
    if t:
        props = list((t.get("inputSchema") or {}).get("properties", {}).keys())
        print(f"   {n:<18} {', '.join(props[:5])}")
        time.sleep(1.4)
time.sleep(3)
