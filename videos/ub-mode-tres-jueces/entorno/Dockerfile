# Entorno de pruebas del vídeo «Mis tests pasaban en verde y no probaban nada» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -f entorno/Dockerfile -t repro-ub-mode-tres-jueces:local .
# Reglas: versiones FIJADAS, ningún dato personal dentro de la imagen y ninguna
# copia de código de terceros dentro del paquete: las tres herramientas se
# instalan desde su repositorio original, ancladas a un commit concreto.
FROM python:3.12-slim

# git solo para traer las tres herramientas desde su repositorio original.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

# crapper c757ec7 · dryer 66ff6d2 · mutator 0136cf5 — los tres, 0BSD, sin tocar.
RUN pip install --no-cache-dir \
      "crapper @ git+https://github.com/unclebob/crapper@c757ec7" \
      "dryer @ git+https://github.com/unclebob/dryer@66ff6d2" \
      "mutator @ git+https://github.com/unclebob/mutator@0136cf5" \
 && pip install --no-cache-dir pytest==8.3.4 coverage==7.6.10

WORKDIR /trabajo
