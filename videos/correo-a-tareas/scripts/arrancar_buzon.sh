#!/bin/bash
# Levanta el SERVIDOR DE CORREO DE PRUEBAS (GreenMail) dentro del contenedor.
# Trae SMTP (3025) e IMAP (3143) reales: los correos se envian y se leen de verdad,
# no se escriben a mano en ninguna carpeta.
# El servidor de pruebas trae la autenticacion desactivada a proposito: el usuario y
# la contrasena que uses en el login crean/abren ese buzon.
set -uo pipefail

puerto_abierto() {
  (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null && { exec 3<&-; return 0; }
  return 1
}

if puerto_abierto 3143; then
  echo "el buzon ya estaba levantado"
  exit 0
fi

# El servidor de pruebas viene dentro de la imagen con su propio jar: lo localizamos
# en vez de fijar la ruta de una maquina concreta (asi el script vale en cualquier
# contenedor). Los parametros de arranque son los que ya trae la imagen.
JAR_BUZON="$(find / -maxdepth 3 -name 'greenmail-standalone.jar' 2>/dev/null | head -1)"
if [ -z "$JAR_BUZON" ]; then
  echo "ERROR: no encuentro greenmail-standalone.jar en la imagen"
  exit 1
fi

nohup java $JAVA_OPTS $GREENMAIL_OPTS -jar "$JAR_BUZON" > /tmp/greenmail.log 2>&1 &

for _ in $(seq 1 80); do
  if puerto_abierto 3143; then
    echo "buzon de pruebas listo: SMTP 3025 / IMAP 3143"
    exit 0
  fi
  sleep 0.25
done

echo "ERROR: el buzon de pruebas no ha arrancado"
tail -n 20 /tmp/greenmail.log
exit 1
