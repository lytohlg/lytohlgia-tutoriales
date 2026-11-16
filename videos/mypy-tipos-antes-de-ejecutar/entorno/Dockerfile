FROM python:3.12-slim

# patch: el material aplica un diff de verdad, no una edición fingida.
RUN apt-get update \
 && apt-get install -y --no-install-recommends patch \
 && rm -rf /var/lib/apt/lists/*

# mypy instalado en la imagen, y las ruedas descargadas para poder instalarlo SIN RED.
RUN pip install --no-cache-dir mypy \
 && mkdir -p /opt/wheels \
 && pip download --no-cache-dir -d /opt/wheels mypy mypy_extensions typing_extensions pathspec

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /trabajo
