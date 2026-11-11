#!/usr/bin/env python3
"""Resume el export JSON de Photon contando lo que hay en cada bloque."""
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
print(
    "intel:", len(d.get("intel", [])),
    "| endpoints:", len(d.get("endpoints", [])),
    "| files:", len(d.get("files", [])),
    "| keys:", len(d.get("keys", [])),
)
