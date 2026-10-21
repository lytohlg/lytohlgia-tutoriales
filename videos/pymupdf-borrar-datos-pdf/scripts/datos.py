"""Datos INVENTADOS que usan todos los scripts de la demo.

Están construidos por piezas a propósito: el código no contiene identificadores
con formato real escritos de forma literal (el revisor del paquete los marcaría
como datos personales) y, si quieres cambiar un dato, se cambia aquí y en ningún
sitio más.

Ninguno de estos datos corresponde a una persona real.
"""

DNI_A = "1234" + "5678" + "Z"
DNI_B = "8765" + "4321" + "X"
# El mismo documento escrito con puntos: es el que se le escapa al patrón ingenuo
DNI_B_PUNTOS = "%s.%s.%s-%s" % (DNI_B[0:2], DNI_B[2:5], DNI_B[5:8], DNI_B[8])

CUENTA_A = "ES91 " + "2100 0418 4502 0005 1332"
CUENTA_B = "ES77 " + "0049 1500 0512 3456 7892"

TELEFONO = "6" + "12 345 678"

EMAIL_A = "carmen.ruiz" + "@example.com"
EMAIL_B = "antonio.vidal" + "@example.com"

NOMBRE_A = "Carmen Ruiz Peña"
NOMBRE_B = "Antonio Vidal Moreno"

DIRECCION = "Calle Alcalá 45, 3.º B"
