# Entorno de pruebas del vídeo «ha-mcp: tu IA controla tu casa sin integraciones a mano» — @lytohlgIA
# ---------------------------------------------------------------------------
# Se construye con (contexto = esta carpeta):
#     docker build -t repro-ha-mcp-casa-ia:local entorno
# Versiones FIJADAS y ningún dato personal dentro de la imagen.
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      jq \
    && rm -rf /var/lib/apt/lists/*

# El servidor MCP del vídeo, con la versión exacta que se probó.
RUN pip install --no-cache-dir ha-mcp==8.7.0

WORKDIR /trabajo
