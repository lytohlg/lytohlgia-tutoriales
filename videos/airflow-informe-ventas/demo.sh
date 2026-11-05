#!/usr/bin/env bash
# Demo del vídeo «Airflow: un informe de ventas en cuatro pasos» — @lytohlgIA
# Reproduce, en un contenedor limpio, lo mismo que se ve en pantalla:
#   un run que sale bien, el informe, y un run que falla sin arrastrar los pasos de abajo.
# Uso:  bash demo.sh
set -uo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
# El binario de Airflow vive en el home del usuario 'airflow' de la imagen; con un
# shell de login el PATH se reescribe, así que lo añadimos sin escribir rutas fijas.
BIN_AIRFLOW="$(getent passwd airflow | cut -d: -f6)/.local/bin"
case ":$PATH:" in
  *":$BIN_AIRFLOW:"*) ;;
  *) export PATH="$BIN_AIRFLOW:$PATH" ;;
esac
export AIRFLOW_HOME="${AIRFLOW_HOME:-/tmp/airflow}"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_FOLDER="$AQUI/dags"
export AIRFLOW__LOGGING__LOGGING_LEVEL=WARNING
# El flujo lee y escribe en estas dos rutas (por defecto, /work/... dentro del contenedor del vídeo):
export INFORME_ENTRADA="$AQUI/entrada/ventas.csv"
export INFORME_SALIDA="$AQUI/salida/informe.csv"

mkdir -p "$AQUI/salida"

echo "== Airflow: un informe de ventas en cuatro pasos =="
echo
echo "-- 0. Base de datos de estados (la crea 'airflow db migrate') --"
airflow db migrate >/dev/null 2>&1 && echo "base de datos lista: $AIRFLOW_HOME/airflow.db"
airflow dags reserialize >/dev/null 2>&1 && echo "flujos registrados en la base de datos"
echo
echo "-- 1. La herramienta y el flujo que ve --"
airflow version
airflow dags list

echo
echo "-- 2. Que pasos ha entendido --"
airflow tasks list informe_clientes

echo
echo "-- 3. Que entra --"
cat "$AQUI/entrada/ventas.csv"

echo
echo "-- 4. Ejecucion real, dia 1: todo en orden --"
bash "$AQUI/scripts/ver.sh" informe_clientes 2026-11-01

echo
echo "-- 5. La salida --"
cat "$AQUI/salida/informe.csv"
HUELLA_DIA1="$(md5sum "$AQUI/salida/informe.csv" | cut -d' ' -f1)"

echo
echo "-- 6. El historial de ejecuciones --"
airflow dags list-runs -d informe_clientes -o plain | awk '{print $2, $3}'

echo
echo "-- 7. Dia 2: el fichero llega con una devolucion sin marcar --"
cp "$AQUI/entrada/ventas_roto.csv" "$AQUI/entrada/ventas.csv"
SALIDA_FALLO="$(bash "$AQUI/scripts/ver.sh" informe_clientes 2026-11-02)"
printf '%s\n' "$SALIDA_FALLO"
case "$SALIDA_FALLO" in
  *ValueError*)
    echo "(el flujo ha fallado, como debia)" ;;
  *)
    echo "INESPERADO: el flujo deberia haber fallado con el importe negativo"
    exit 1 ;;
esac

echo
echo "-- 8. Contencion: los pasos de abajo no se lanzan --"
bash "$AQUI/scripts/estado.sh" 2026-11-02
HUELLA_ANTES="${HUELLA_DIA1:-}"
HUELLA_AHORA="$(md5sum "$AQUI/salida/informe.csv" | cut -d' ' -f1)"
if [ "$HUELLA_AHORA" = "$HUELLA_ANTES" ]; then
  echo "el informe del dia 1 sigue intacto: el dia 2 no escribio ninguno"
else
  echo "INESPERADO: el dia 2 ha escrito un informe nuevo"
  exit 1
fi
echo
echo "(fin de la demo)"
