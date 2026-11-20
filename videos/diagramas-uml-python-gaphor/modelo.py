"""El modelo de pedidos escrito como texto: cinco clases y sus relaciones."""
import os

from gaphor import UML
from gaphor.core.modeling import ElementFactory
from gaphor.UML import Diagram
from gaphor.diagram.drop import drop
from gaphor.diagram.presentation import connect
from gaphor.diagram.export import save_png
from gaphor.plugins.diagramexport.exportall import export_all
from gaphor.UML.recipes import create_association, create_generalization
from gaphor.storage import storage


def clase(ef, nombre, atributos):
    c = ef.create(UML.Class)
    c.name = nombre
    for a in atributos:
        p = ef.create(UML.Property)
        p.name = a
        c.ownedAttribute = p
    return c


ef = ElementFactory()

Cliente = clase(ef, "Cliente", ["nombre", "email"])
Producto = clase(ef, "Producto", ["sku", "precio"])
Pedido = clase(ef, "Pedido", ["fecha", "total"])
Linea = clase(ef, "LineaPedido", ["cantidad"])
Urgente = clase(ef, "PedidoUrgente", ["horas_limite"])

create_generalization(Pedido, Urgente)
create_association(Cliente, Pedido)
create_association(Pedido, Linea)
create_association(Linea, Producto)

diagrama = ef.create(Diagram)
diagrama.name = "Pedidos"
paquete = ef.create(UML.Package)
paquete.name = "Pedidos"
paquete.ownedDiagram = diagrama
items = {}
POS = {
    Cliente: (40, 60),
    Pedido: (380, 60),
    Linea: (720, 60),
    Producto: (720, 300),
    Urgente: (380, 300),
}
for c, (x, y) in POS.items():
    items[c] = drop(c, diagrama, x=x, y=y)

for asociacion in list(ef.select(UML.Association)):
    linea = drop(asociacion, diagrama, x=0, y=0)
    if linea:
        connect(linea, linea.head, items[asociacion.memberEnd[0].type])
        connect(linea, linea.tail, items[asociacion.memberEnd[1].type])

for generalizacion in list(ef.select(UML.Generalization)):
    linea = drop(generalizacion, diagrama, x=0, y=0)
    if linea:
        connect(linea, linea.head, items[generalizacion.specific])
        connect(linea, linea.tail, items[generalizacion.general])

with open("pedidos.gaphor", "w", encoding="utf-8") as f:
    storage.save(f, ef)

os.makedirs("salida", exist_ok=True)
export_all(ef, "salida", save_png, "png")
ruta_png = "salida/Pedidos/Pedidos.png"

print(f"modelo guardado: {len(list(ef.select(UML.Class)))} clases, "
      f"{len(list(ef.select(UML.Association)))} asociaciones, "
      f"{len(list(ef.select(UML.Generalization)))} generalizaciones")
print("exportado:", ruta_png)
