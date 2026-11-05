# Entorno de pruebas del vídeo «Airflow: un informe de ventas en cuatro pasos» — @lytohlgIA
# ---------------------------------------------------------------------------
# Es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-airflow-informe-ventas:local entorno
# Versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
FROM apache/airflow:2.10.5-python3.11

# La imagen oficial trae un entrypoint que exige GID=0 si la ejecutas con otro
# usuario. Aquí lo quitamos para poder correr con un usuario sin privilegios
# (--user 1000:1000) tal como se prueba el material.
ENTRYPOINT []

# El home del usuario 'airflow' viene con permisos 770: un usuario ajeno (1000)
# no puede ni entrar, y el binario 'airflow' vive ahí dentro.
USER root
RUN chmod o+rx "$(getent passwd airflow | cut -d: -f6)" && \
    groupadd -g 1000 demo && \
    useradd -u 1000 -g 1000 -m -s /bin/bash demo
USER airflow

# La demo escribe aqui su base de datos de estados, para poder correr sin
# privilegios y sin tocar nada de /opt.
ENV AIRFLOW_HOME=/tmp/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__LOGGING__LOGGING_LEVEL=WARNING

# El material NO se copia dentro: se monta en /trabajo y se ejecuta desde ahi,
# para que la demo pruebe exactamente los ficheros del paquete.
WORKDIR /trabajo
