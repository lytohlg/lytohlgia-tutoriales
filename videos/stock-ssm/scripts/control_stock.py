"""Control de lo que hay en el almacén, leído por el ORM de la aplicación.

    python3 scripts/control_stock.py     (con la aplicación en el PYTHONPATH, ver demo.sh)

Sirve para comprobar que la hoja de cálculo entró entera: sin la API de por medio.
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssm.settings")
django.setup()

from stock_manager.models import Item  # noqa: E402  (después de django.setup())

MINIMO = int(os.environ.get("AVISO_MINIMO", 10))
articulos = list(Item.objects.all())

print("articulos en el almacen:", len(articulos))
print("unidades totales:", sum(articulo.quantity for articulo in articulos))
bajos = sorted((a for a in articulos if a.quantity < MINIMO), key=lambda a: a.quantity)
print(f"por debajo del minimo ({MINIMO}):", len(bajos))
for articulo in bajos:
    print(f"  {articulo.sku:>9} {articulo.quantity:>4} unidades  {articulo.description}")
