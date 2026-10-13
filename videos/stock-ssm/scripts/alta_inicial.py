"""Crea los grupos y los usuarios que necesita la demo.

Se ejecuta con el shell de Django, que ya tiene la aplicación cargada:

    python3 "$APP/manage.py" shell < scripts/alta_inicial.py

Es idempotente: si ya existe, no duplica nada.
"""

import os

from django.contrib.auth.models import Group, User

GRUPOS = ("managers", "shop_users")

ALTA = (
    (os.environ["DEMO_USUARIO_ALMACEN"], os.environ["DEMO_ALMACEN_CLAVE"], "managers"),
    (os.environ["DEMO_USUARIO_TIENDA"], os.environ["DEMO_TIENDA_CLAVE"], "shop_users"),
)

for nombre in GRUPOS:
    grupo, creado = Group.objects.get_or_create(name=nombre)
    print(f"grupo {nombre}: {'creado' if creado else 'ya existe'}")

for usuario, clave, grupo in ALTA:
    u, creado = User.objects.get_or_create(username=usuario)
    u.set_password(clave)
    u.is_active = True
    u.save()
    u.groups.set([Group.objects.get(name=grupo)])
    print(f"usuario {usuario}: {'creado' if creado else 'actualizado'} -> grupo {grupo}")

print("alta inicial terminada")
