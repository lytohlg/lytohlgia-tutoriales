#!/usr/bin/env python3
"""manage.py del proyecto de la demo.

Aquí SQL Explorer no es una librería de consola: es una APP de Django, y por eso
todo pasa por un proyecto Django normal (este). Se usa desde la carpeta de la demo:

    python3 proyecto/manage.py migrate
    python3 proyecto/manage.py shell
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informes.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
