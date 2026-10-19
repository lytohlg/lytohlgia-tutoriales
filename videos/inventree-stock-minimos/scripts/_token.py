#!/usr/bin/env python3
"""Crea (o reutiliza) el token de API del usuario admin y lo guarda en .token."""
import os
import sys

import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InvenTree.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from users.models import ApiToken  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
usuario = get_user_model().objects.get(username="admin")
token, _ = ApiToken.objects.get_or_create(user=usuario, name="video")
with open(os.path.join(BASE, ".token"), "w") as f:
    f.write(token.key + "\n")
print("token de API listo para admin (guardado en .token)")
