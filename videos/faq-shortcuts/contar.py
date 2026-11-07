import collections
import sys

REGLAS = [
    ("revisar el CSV de facturas", ("csv", "cuadran")),
    ("generar el PDF de una factura", ("pdf",)),
    ("correo de recordatorio", ("correo",)),
    ("resumen del ultimo commit", ("commit",)),
    ("clientes sin NIF", ("nif",)),
]

cuenta = collections.Counter()
sin_clasificar = 0
for linea in sys.stdin:
    partes = linea.rstrip("\n").split("\t", 2)
    if len(partes) != 3:
        continue
    texto = partes[2].lower()
    for nombre, claves in REGLAS:
        if all(c in texto for c in claves):
            cuenta[nombre] += 1
            break
    else:
        sin_clasificar += 1

for nombre, n in cuenta.most_common():
    print("%3d  %s" % (n, nombre))
print("%3d  peticiones clasificadas, %d sueltas" % (sum(cuenta.values()), sin_clasificar))
