# Entorno de pruebas del vídeo «Plotly: tu CSV en un gráfico interactivo que se abre en el navegador» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-plotly-csv-interactivo:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM python:3.12-slim

# Sin compiladores ni paquetes de sistema: todo lo necesario viene en los wheels.
RUN pip install --no-cache-dir plotly==7.2.0 pandas==2.3.3

WORKDIR /trabajo
