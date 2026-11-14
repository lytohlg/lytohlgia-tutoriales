"""El print() de siempre: el mismo trabajo, contado en líneas que se van.

Uso: python3 lote_print.py [--pausa 0.02]
"""
import argparse
import time

import procesar

ap = argparse.ArgumentParser()
ap.add_argument("--pausa", type=float, default=0.02)
args = ap.parse_args()

pendientes = procesar.ficheros()
total = len(pendientes)
ok = err = 0
inicio = time.time()

for i, ruta in enumerate(pendientes, 1):
    try:
        filas, importe = procesar.procesar(ruta)
        ok += 1
        print(f"[{i:03d}/{total}] {ruta.name}: {filas} filas, {importe} EUR")
    except Exception as e:                      # noqa: BLE001 — cualquier fallo cuenta
        err += 1
        print(f"[{i:03d}/{total}] {ruta.name}: ERROR {e}")
    time.sleep(args.pausa)

print(f"FIN en {time.time() - inicio:.1f}s · {ok} correctos · {err} con error")
print(f"JSON escritos en {procesar.SALIDA}/")
