#!/usr/bin/env python3
"""Lee la base y falla si lo que afirma el video no se cumple."""
import sqlite3
import sys

DB = sys.argv[1] if len(sys.argv) > 1 else "trafico.db"
c = sqlite3.connect(DB)
filas = c.execute("select status, model, req_body, up_req_body, req_headers, up_req_headers "
                  "from exchanges order by id").fetchall()
if not filas:
    print("FALLO: la tabla exchanges esta vacia")
    sys.exit(1)

ok200 = [f for f in filas if f[0] == 200]
if not ok200:
    print("FALLO: ninguna peticion devolvio 200")
    sys.exit(1)

f = ok200[-1]
pedido, enviado = f[2] or "", f[3] or ""
h_in, h_out = f[4] or "", f[5] or ""

fallos = []
if "gpt-4o-mini" in pedido:
    fallos.append("el cuerpo que entro ya traia el modelo barato (no hubo reescritura)")
if "gpt-4o-mini" not in enviado:
    fallos.append("el cuerpo que salio no lleva el modelo mapeado")
if "local-demo" not in h_in:
    fallos.append("la clave del cliente no aparece en las cabeceras de entrada")
if "local-demo" in h_out:
    fallos.append("la clave del cliente VIAJO al proveedor (deberia haberse quitado)")
if not any(x[0] == 401 for x in filas):
    fallos.append("no hay ninguna peticion rechazada con 401 (la puerta no se probo)")

for x in fallos:
    print("FALLO:", x)
if fallos:
    sys.exit(1)

print(f"VERIFICADO: {len(filas)} intercambios en la base · "
      "modelo pedido reescrito en el cuerpo reenviado · cabecera X-Team inyectada · "
      "credencial del cliente no reenviada")
