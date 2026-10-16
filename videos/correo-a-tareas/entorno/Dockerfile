# Entorno de pruebas del vídeo «imap_tools: convierte correos en tareas con Python» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t repro-correo-a-tareas:local entorno
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
#
# La base es el servidor de correo de pruebas GreenMail (SMTP e IMAP reales): la
# promesa del material es leer correo de verdad, así que hace falta un servidor al
# que conectarse. No hay cuentas de correo reales ni claves dentro de la imagen.
FROM greenmail/standalone:2.1.1

USER root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      sqlite3 \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Dependencia de Python con la versión FIJADA, comprobada durante la construcción.
RUN pip3 install --no-cache-dir imap-tools==1.16.0 \
 && python3 -c "import imap_tools; print('imap_tools', imap_tools.__version__)"

WORKDIR /trabajo

# Fuera el entrypoint del servidor de correo: en la demo manda demo.sh.
ENTRYPOINT []
CMD ["bash"]
