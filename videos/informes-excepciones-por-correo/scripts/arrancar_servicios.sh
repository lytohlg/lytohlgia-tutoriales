#!/bin/bash
# Levanta los DOS servidores de prueba que necesita la demo, dentro del contenedor:
#
#   * MailHog  (imagen oficial mailhog/mailhog): SMTP real en 127.0.0.1:1025 y una
#     API en 127.0.0.1:8025 para LEER los correos que han llegado.
#   * moto     : un S3 local en 127.0.0.1:5000, que es donde SQL Explorer publica
#     el informe (la herramienta manda el enlace por correo) y se crea el bucket.
#
# Los dos son servidores REALES, en local: la demo no depende de credenciales ni
# de servicios de pago, y el correo que se lee es el que se envió de verdad.
set -uo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ESPERAR=200   # 200 x 0.25 s = hasta 50 s

puerto_abierto() { python3 "$AQUI/servicios.py" puerto "$1"; }

esperar() {
  for _ in $(seq 1 $ESPERAR); do
    puerto_abierto "$1" && return 0
    sleep 0.25
  done
  return 1
}

# ---------------------------------------------------------------- MailHog (correo)
if puerto_abierto 8025; then
  echo "el correo de pruebas ya estaba levantado"
else
  nohup /usr/local/bin/MailHog -storage=memory \
    -smtp-bind-addr 127.0.0.1:1025 \
    -ui-bind-addr 127.0.0.1:8025 \
    -api-bind-addr 127.0.0.1:8025 > /tmp/mailhog.log 2>&1 &
  if ! esperar 8025; then
    echo "ERROR: el correo de pruebas no ha arrancado"
    tail -n 20 /tmp/mailhog.log
    exit 1
  fi
fi

# ---------------------------------------------------------------- moto (S3 local)
if puerto_abierto 5000; then
  echo "el s3 local ya estaba levantado"
else
  nohup python3 -m moto.server -p 5000 -H 127.0.0.1 > /tmp/s3.log 2>&1 &
  if ! esperar 5000; then
    echo "ERROR: el s3 local no ha arrancado"
    tail -n 20 /tmp/s3.log
    exit 1
  fi
fi

# El bucket donde la herramienta deja el informe, y el buzón a cero para que los
# recuentos de correos sean los de esta ejecución.
python3 "$AQUI/servicios.py" s3
python3 "$AQUI/servicios.py" vaciar

echo "servidores de prueba listos: correo SMTP 127.0.0.1:1025 (API 8025) | s3 127.0.0.1:5000 (bucket informes)"
