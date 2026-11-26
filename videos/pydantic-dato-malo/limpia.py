"""El flujo real: de un CSV sucio a dos ficheros.

  pedidos_ok.csv   sale con tipos ya validados: es lo único que debería llegar a la base de datos
  informe.csv      una fila por problema, con el campo y el motivo: es la lista de trabajo
                   de quien tiene que arreglar el origen

El que decide qué hacer con un rechazo es la aplicación; pydantic solo dice qué está mal.
"""
import csv

from normaliza import Pedido
from pydantic import ValidationError

CAMPOS = ["id", "cliente", "email", "importe", "fecha", "estado"]

ok, informe = [], []
with open("datos/pedidos.csv", newline="", encoding="utf-8") as fh:
    for n, fila in enumerate(csv.DictReader(fh), start=2):  # 2 = primera fila de datos
        try:
            ok.append(Pedido.model_validate(fila))
        except ValidationError as exc:
            for e in exc.errors():
                informe.append({
                    "linea": n,
                    "campo": ".".join(str(x) for x in e["loc"]),
                    "motivo": e["msg"],
                    "valor": e["input"] if not isinstance(e["input"], dict) else "",
                })

with open("pedidos_ok.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(CAMPOS)
    for p in ok:
        w.writerow([p.id, p.cliente, p.email, p.importe, p.fecha.isoformat(), p.estado])

with open("informe.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["linea", "campo", "motivo", "valor"], lineterminator="\n")
    w.writeheader()
    w.writerows(informe)

print(f"pedidos_ok.csv: {len(ok)} filas limpias")
print(f"informe.csv:    {len(informe)} problemas para arreglar en el origen")
