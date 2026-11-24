#!/usr/bin/env python3
"""Los tres jueces de ub-mode en un solo comando.

crapper -> complejidad ciclomatica y CRAP (con la cobertura de pytest)
dryer   -> duplicacion estructural
mutator -> tests que no matan sus propios bugs

Uso:  python gate.py [--umbral-crap 10]
Salida: tabla + veredicto. exit 0 si pasa, 1 si no.
"""
import re
import subprocess
import sys

UMBRAL = 10.0
if "--umbral-crap" in sys.argv:
    UMBRAL = float(sys.argv[sys.argv.index("--umbral-crap") + 1])


def corre(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


corre("python -m coverage run --source=src -m pytest tests -q")
corre("python -m coverage lcov -o target/coverage/python/lcov.info")
madurez = corre("python -m crapper --root . --source-root src "
                "--use-existing-coverage")
duplicacion = corre("python -m dryer --root . --source-root src")
mutacion = corre("python -m mutator --root . --source-root src "
                 "--use-existing-coverage --mutate-all "
                 "--test-command 'python -m pytest tests -q'")

filas = re.findall(
    r"^(\w+)\s+(\w+)\s+(\d+)\s+([\d.]+)%\s+([\d.]+)$", madurez, re.M)

print(f"{'funcion':24}{'CC':>4}{'cob%':>8}{'CRAP':>8}  juez")
fallos = 0
for nombre, _ns, cc, cob, valor in sorted(filas, key=lambda f: -float(f[4])):
    malo = float(valor) >= UMBRAL
    fallos += malo
    print(f"{nombre:24}{cc:>4}{cob:>8}{valor:>8}  {'FALLA' if malo else 'OK'}")

dups = duplicacion.count("DUPLICATE")
total = re.search(r"^Total\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", mutacion, re.M)
# columnas del mutator: Killed  Survived  Uncovered  Sites
matados, sobreviven, sin_cubrir, sitios = (
    (int(total.group(1)), int(total.group(2)), int(total.group(3)), int(total.group(4)))
    if total else (0, 0, 0, 0))

print(f"\nduplicados: {dups} bloque(s)")
fallos += dups > 0
print(f"mutantes:   {matados} matado{'s' if matados != 1 else ''} / "
      f"{sobreviven} sobreviven / {sin_cubrir} sin cubrir ({sitios} sitios)")
fallos += sobreviven > 0

print("\nVEREDICTO:", "PASA" if fallos == 0 else f"RECHAZADO ({fallos} fallos)")
sys.exit(0 if fallos == 0 else 1)
