# Entorno de pruebas del vídeo «Automatizacion por umbral con Home Assistant: aviso cuando el salon pasa de 30 grados» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-home-assistant-automatizacion-umbral:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM ghcr.io/home-assistant/home-assistant:2026.10.4

# El motor ya trae todo lo que usa la demo: sensor por comando y automatizaciones.
# No hay dependencias extra; si algún día hicieran falta, se fijan con su versión.

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /trabajo
CMD ["bash"]
