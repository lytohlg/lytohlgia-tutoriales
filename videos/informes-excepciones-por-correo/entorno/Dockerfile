# Entorno de pruebas del vídeo «SQL Explorer: el informe de excepciones te llega solo» — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material. Se construye con:
#     docker build -t sqlexplorer-demo:v1 demo
# Reglas: versiones FIJADAS (reproducible) y ningún dato personal dentro de la imagen.
#
# El material promete dos cosas que necesitan un servidor de verdad:
#   * SQL Explorer manda el informe POR CORREO -> hace falta un servidor SMTP.
#     Se usa MailHog: el binario tal cual viene en su imagen oficial
#     (mailhog/mailhog), copiado aquí para que la prueba quepa en UN contenedor.
#   * SQL Explorer publica el informe en S3 y manda el enlace -> hace falta un S3.
#     Se usa moto, que levanta un S3 local dentro del contenedor.
# Ninguno de los dos es un simulacro de la app: son servidores reales en local,
# para que la prueba no dependa de credenciales ni de servicios de pago.
FROM mailhog/mailhog:v1.0.1 AS mailhog

FROM python:3.12-slim
USER root
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      sqlite3 \
      ca-certificates \
      musl \
 && rm -rf /var/lib/apt/lists/*

# Dependencias de Python con la versión FIJADA, comprobadas durante la construcción.
RUN pip install --no-cache-dir \
      "Django==5.2.18" \
      "django-sql-explorer==5.3" \
      "celery==5.6.3" \
      "boto3==1.43.114" \
      "moto[server]==5.2.4" \
      "requests==2.34.2" \
 && python -c "import django, explorer, celery, boto3, moto, requests; print('django', django.get_version(), '| django-sql-explorer 5.3 OK | celery', celery.__version__)"

# El servidor de correo de pruebas: el binario de la imagen oficial, sin recortes.
# La imagen oficial de MailHog trae Alpine, así que su binario pide la libc de musl:
# por eso arriba se instala `musl` en esta imagen (que es Debian) y así arranca.
COPY --from=mailhog /usr/local/bin/MailHog /usr/local/bin/MailHog

WORKDIR /trabajo
CMD ["bash"]
