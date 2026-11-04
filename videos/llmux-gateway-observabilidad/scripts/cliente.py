#!/usr/bin/env python3
"""Cliente real (SDK de OpenAI) contra el gateway local. La clave va por argumento."""
import os
import sys

from openai import OpenAI

URL = os.environ.get("LLMUX_URL", "http://127.0.0.1:8095/v1")
CLAVE = sys.argv[1] if len(sys.argv) > 1 else ""

client = OpenAI(base_url=URL, api_key=CLAVE)
r = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "cuanto suma la factura de marzo"}],
)
print("respuesta:", r.choices[0].message.content)
print("modelo que devuelve el gateway:", r.model)
print("tokens:", r.usage.total_tokens)
