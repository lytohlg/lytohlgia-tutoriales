#!/usr/bin/env python3
"""Escena 6b — la configuración que conecta ESE servidor con TU casa."""
import time

print("lo que va en el cliente MCP (Claude Desktop, Cursor, Continue...):")
print("""
{
  "mcpServers": {
    "home-assistant": {
      "command": "uvx",
      "args": ["ha-mcp@latest"],
      "env": {
        "HOMEASSISTANT_URL": "http://homeassistant.local:8123",
        "HOMEASSISTANT_TOKEN": "<token de larga duración>"
      }
    }
  }
}""")
time.sleep(2.6)
print("las dos variables:")
print("   HOMEASSISTANT_URL   -> http://ip-de-tu-home-assistant:8123")
time.sleep(2.0)
print("   HOMEASSISTANT_TOKEN -> Perfil > Seguridad > Tokens de larga duración")
time.sleep(2.4)
print("\n(esa URL es la de casa: homeassistant.local también vale)")
time.sleep(3)
