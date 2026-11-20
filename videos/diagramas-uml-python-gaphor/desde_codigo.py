"""Del código a un diagrama: lee las clases con ast y las convierte en modelo UML.

Uso: python3 desde_codigo.py [carpeta]   (por defecto: tienda)

Lo que este script SÍ saca del código: nombre de clase, atributos anotados y herencia
entre clases del propio paquete. Lo que NO saca: asociaciones (el código no las declara).
"""
import ast
import os
import pathlib
import sys

from gaphor import UML
from gaphor.core.modeling import ElementFactory
from gaphor.UML import Diagram
from gaphor.diagram.drop import drop
from gaphor.diagram.presentation import connect
from gaphor.diagram.export import save_png, save_svg
from gaphor.plugins.diagramexport.exportall import export_all
from gaphor.UML.recipes import create_generalization
from gaphor.storage import storage

carpeta = sys.argv[1] if len(sys.argv) > 1 else "tienda"
rotulo = carpeta.capitalize()

# 1. leer el código: una clase por ClassDef, con sus anotaciones y sus bases
clases, herencias = {}, []
for fichero in sorted(pathlib.Path(carpeta).glob("*.py")):
    arbol = ast.parse(fichero.read_text(encoding="utf-8"))
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.ClassDef):
            continue
        atributos = [n.target.id for n in nodo.body
                     if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
        clases[nodo.name] = atributos
        for base in nodo.bases:
            if isinstance(base, ast.Name):
                herencias.append((base.id, nodo.name))

# 2. construir el modelo UML con esos datos
ef = ElementFactory()
elementos = {}
for nombre, atributos in clases.items():
    c = ef.create(UML.Class)
    c.name = nombre
    for a in atributos:
        p = ef.create(UML.Property)
        p.name = a
        c.ownedAttribute = p
    elementos[nombre] = c

dentro = 0
for base, hija in herencias:
    if base in elementos and hija in elementos:
        create_generalization(elementos[base], elementos[hija])
        dentro += 1

diagrama = ef.create(Diagram)
diagrama.name = rotulo
paquete = ef.create(UML.Package)
paquete.name = rotulo
paquete.ownedDiagram = diagrama
items = {}
for i, (nombre, c) in enumerate(elementos.items()):
    items[nombre] = drop(c, diagrama, x=40 + (i % 3) * 300, y=60 + (i // 3) * 240)

for generalizacion in list(ef.select(UML.Generalization)):
    linea = drop(generalizacion, diagrama, x=0, y=0)
    if linea:
        hija = generalizacion.specific.name
        base = generalizacion.general.name
        if hija in items and base in items:
            connect(linea, linea.head, items[hija])
            connect(linea, linea.tail, items[base])

with open(f"{carpeta}.gaphor", "w", encoding="utf-8") as f:
    storage.save(f, ef)

print(f"leídas {len(clases)} clases del código")
print(f"herencias dentro del paquete: {dentro}")
print("atributos totales:", sum(len(a) for a in clases.values()))
print("asociaciones: 0 (el código no las declara; no se inventan)")

salida = f"salida_{carpeta}"
os.makedirs(salida, exist_ok=True)
export_all(ef, salida, save_png, "png")
export_all(ef, salida, save_svg, "svg")
print(f"exportado: {salida}/{rotulo}/{rotulo}.png y .svg")
