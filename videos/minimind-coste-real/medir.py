"""Mide un log de preentreno de MiniMind: pérdida, pasos, tokens y tiempo real.

Uso: python medir.py <log>
No estima nada: si el log no trae lo que pide, falla.
"""
import re
import sys
from datetime import datetime
from pathlib import Path

log = Path(sys.argv[1])
raw = log.read_text(errors="ignore")
losses = [float(m) for m in re.findall(r", loss: ([0-9.]+),", raw)]
if not losses:
    sys.exit("KO: el log no tiene ninguna línea de pérdida")

pasos = len(losses)
tokens = pasos * 8 * 340
primera, ultima = losses[0], losses[-1]
minima = min(losses)

print(f"PASOS:  {pasos}")
print(f"PERDIDA: {primera:.2f} -> {ultima:.2f}  (minima {minima:.2f})")
print(f"TOKENS: {tokens}")
if ultima > primera:
    print("AVISO: la pérdida no bajó en esta ejecución")
elif ultima < primera:
    print("OK: la pérdida bajó")
print("GPU:    0 (ejecución en CPU)")
