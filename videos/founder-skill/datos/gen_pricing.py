#!/usr/bin/env python3
"""Genera un CSV de respuestas de ejemplo (Van Westendorp) para la demo.

Datos SINTETICOS y declarados como tales: simulan 40 respuestas de clientes a las
cuatro preguntas de precio. Sirven para probar la herramienta; en el video se dice
explicitamente que son de ejemplo y que los reales los pone el negocio.
"""
import csv
import random

random.seed(11)
filas = []
for _ in range(40):
    too_cheap = round(random.uniform(2.0, 4.2), 2)
    cheap = round(too_cheap + random.uniform(0.6, 1.4), 2)
    expensive = round(random.uniform(6.4, 8.4), 2)
    too_expensive = round(expensive + random.uniform(1.2, 3.0), 2)
    filas.append({
        "too_cheap": too_cheap,
        "cheap": cheap,
        "expensive": expensive,
        "too_expensive": too_expensive,
    })

with open("pricing.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["too_cheap", "cheap", "expensive", "too_expensive"])
    w.writeheader()
    w.writerows(filas)
print("pricing.csv:", len(filas), "respuestas")
