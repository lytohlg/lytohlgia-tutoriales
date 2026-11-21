# Entorno de pruebas del vídeo «Mira qué esconde tu Excel antes de analizarlo con ydata-profiling» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-perfilar-antes-de-analizar:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
# Python 3.11: el paquete exige >=3.10,<3.14.
FROM python:3.11-slim

# jq: para filtrar el resumen JSON del informe desde la terminal, sin abrir el navegador.
RUN apt-get update && apt-get install -y --no-install-recommends \
      jq \
    && rm -rf /var/lib/apt/lists/*

# El paquete se llama fg-data-profiling desde el cambio de nombre del proyecto
# (el antiguo ydata-profiling sigue en PyPI pero avisa de que ya no recibe actualizaciones).
RUN pip install --no-cache-dir \
      fg-data-profiling==4.20.0

WORKDIR /trabajo
