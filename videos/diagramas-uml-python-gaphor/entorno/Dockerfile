# Entorno de pruebas del vídeo «Genera diagramas UML desde tu código Python con Gaphor» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-diagramas-uml-python-gaphor:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM debian:13

# 1. Bibliotecas gráficas que Gaphor necesita en tiempo de ejecución
#    (GTK 4, GtkSource 5 y libadwaita) + herramientas del sistema.
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      python3-dev \
      build-essential \
      pkg-config \
      meson \
      ninja-build \
      cmake \
      libcairo2-dev \
      libgirepository-2.0-dev \
      gobject-introspection \
      gir1.2-gtk-4.0 \
      gir1.2-gtksource-5 \
      gir1.2-adw-1 \
      file \
    && rm -rf /var/lib/apt/lists/*

# 2. Gaphor con la versión fijada, en el Python del sistema: así `python3 modelo.py`
#    funciona igual en una shell normal y en una shell de login (un venv se cae del
#    PATH con `bash -lc`). PyGObject y pycairo se compilan: por eso las cabeceras
#    de arriba (sin ellas, pip falla y el fallo parece otra cosa).
RUN python3 -m pip install --break-system-packages --no-cache-dir gaphor==3.3.2

ENV PYTHONPATH=""

WORKDIR /trabajo
