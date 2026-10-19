# Entorno de pruebas del vídeo «InvenTree: controla el stock de tus componentes con Python» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-inventree-stock-minimos:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
#
# La aplicación que se demuestra es software de terceros (InvenTree, MIT). Se usa la imagen
# oficial clavada por digest para que el entorno siga siendo el mismo aunque el proyecto
# publique versiones nuevas. No se copia nada del paquete dentro: `demo.sh` corre desde la
# carpeta montada en solo-lectura y trabaja sobre una copia en /tmp.
FROM inventree/inventree@sha256:4aefd6e2bb0e77ff33ae28865a6645ef9aac020924479eda8bda470820fcc2e3

# La imagen oficial trae `ENTRYPOINT ["/bin/bash", "./init.sh"]`: un guion relativo al directorio
# de la aplicación que migra y lanza gunicorn por su cuenta. Aquí el contenedor no se usa así
# (el paquete se copia a /tmp/repro y la aplicación la arranca `scripts/arrancar.sh`), y con
# ese ENTRYPOINT puesto cualquier orden se interpretaba como argumentos de ./init.sh: lo que
# se veía era «./init.sh: No such file or directory» y la demo no llegaba a ejecutarse.
# Se anula para que el contenedor ejecute exactamente lo que dice el paquete.
ENTRYPOINT []

# InvenTree toma su configuración del entorno; la demo usa SQLite dentro del directorio de
# trabajo (ninguna base de datos externa). `scripts/arrancar.sh` vuelve a exportar estas
# variables apuntando a la copia de /tmp, así que aquí sólo van los valores por defecto.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    INVENTREE_DB_ENGINE=sqlite3 \
    INVENTREE_SITE_URL=http://127.0.0.1:8000 \
    INVENTREE_SECRET_KEY=clave-de-entorno-de-pruebas

# La imagen base ya trae las dependencias, pero instaladas en el directorio personal del usuario
# administrador (modo 0700): funcionan si el proceso corre como tal y son invisibles para cualquier
# otro usuario. El contenedor de la demo corre sin privilegios, así que aquí se mueven a la ruta de
# paquetes del sistema, que sí es legible para todos. Sin red y sin cambiar ninguna versión.
RUN sitio="$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')" \
    && usuario="$(python3 -c 'import site; print(site.getusersitepackages())')" \
    && mv "$usuario"/* "$sitio"/ \
    && python3 -c "import django; print('Django', django.get_version())"

# Directorio de trabajo de la demo (el contenedor se lanza con -w /tmp y copia ahí el paquete).
WORKDIR /trabajo
