# Entorno de pruebas del vídeo «pre-commit: tu clave privada se para antes del commit» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-precommit-clave-fuera-del-commit:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PRE_COMMIT_HOME=/opt/pc-cache

# git: pre-commit engancha sus controles en .git/hooks.
# openssl: la demo genera una clave privada DESECHABLE para que el control tenga algo que detectar.
RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends git openssl \
 && rm -rf /var/lib/apt/lists/*

# Versión fijada: la misma que se ve en el vídeo.
RUN pip install --no-cache-dir -q pre-commit==4.7.0

# Los controles se descargan UNA vez, aquí: así la demo no depende de la red ni del reloj,
# y se comporta igual en tu equipo que en el nuestro. Las versiones son las del vídeo.
RUN git init -q /opt/warm \
 && cd /opt/warm \
 && printf 'repos:\n  - repo: https://github.com/pre-commit/pre-commit-hooks\n    rev: v6.0.0\n    hooks:\n      - id: trailing-whitespace\n      - id: end-of-file-fixer\n      - id: check-yaml\n      - id: check-added-large-files\n      - id: detect-private-key\n  - repo: https://github.com/Yelp/detect-secrets\n    rev: v1.5.0\n    hooks:\n      - id: detect-secrets\n' > .pre-commit-config.yaml \
 && pre-commit install-hooks >/dev/null 2>&1 \
 && test -d "$PRE_COMMIT_HOME" \
 && chmod -R 0777 "$PRE_COMMIT_HOME" \
 && rm -rf /opt/warm

WORKDIR /trabajo
