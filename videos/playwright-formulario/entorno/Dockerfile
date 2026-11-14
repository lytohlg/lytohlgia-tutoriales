# Entorno de pruebas del vídeo «Automatiza la prueba de tu formulario web con Playwright Python» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-playwright-formulario:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright

# libatomic1: sin esa librería el driver de Playwright ni siquiera arranca en slim,
# y sin driver no se puede ejecutar `playwright install`.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libatomic1 ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir playwright==1.65.0 \
 && playwright install --with-deps chromium \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /trabajo
CMD ["python", "--version"]
