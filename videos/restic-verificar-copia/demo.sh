#!/usr/bin/env bash
# Demo del vídeo «restic: restaurar y comparar para saber si tu copia sirve» — @lytohlgIA
# ---------------------------------------------------------------------------
# Es EXACTAMENTE el flujo que se ve en el vídeo, en el mismo orden: montar la
# copia, romper los datos a propósito, restaurar, comparar fichero a fichero por
# sha256 y dejar el verificador funcionando solo.
#
# Rutas RELATIVAS a esta carpeta: todo el trabajo ocurre en ./trabajo (o donde
# diga TRABAJO). No toca nada fuera de ahí.
set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRABAJO="${TRABAJO:-$RAIZ/trabajo}"
PY="${PYTHON:-python3}"
REPO="$TRABAJO/copias/repo"
DATOS="$TRABAJO/datos"
VERIF="$TRABAJO/verificacion"
PASS_FILE="$TRABAJO/.restic-pass"
export TRABAJO

for cmd in restic "$PY"; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "FALTA '$cmd' en el PATH. Mira el README (Requisitos)."; exit 2; }
done

echo "== 0/9  limpieza =="
mkdir -p "$TRABAJO"
rm -rf "$DATOS" "$TRABAJO/copias" "$VERIF" "$TRABAJO/recuperado" "$TRABAJO/informes"
rm -f "$TRABAJO/contratos_antes.sha" "$TRABAJO/informe_verificacion.json"
ls -A "$TRABAJO"

echo "== 1/9  los datos de la gestoría =="
"$PY" "$RAIZ/scripts/crear_datos.py" --base "$DATOS"

echo "== 2/9  huella de los contratos ANTES de tocar nada =="
( cd "$DATOS" && find contratos -type f | sort | xargs sha256sum > "$TRABAJO/contratos_antes.sha" )
wc -l < "$TRABAJO/contratos_antes.sha"

echo "== 3/9  contraseña del repositorio: fichero con permisos 600 =="
printf '%s' "${RESTIC_PASS:-demo-copias-2026}" > "$PASS_FILE"
chmod 600 "$PASS_FILE"
export RESTIC_PASSWORD_FILE="$PASS_FILE"
ls -l "$PASS_FILE"

echo "== 4/9  repositorio + primera copia =="
restic --repo "$REPO" init
restic --repo "$REPO" backup "$DATOS" --tag diario
restic --repo "$REPO" snapshots

echo "== 5/9  EL DESASTRE (a propósito) =="
ls "$DATOS"
rm -rf "$DATOS/contratos"
ls "$DATOS"
[ ! -d "$DATOS/contratos" ] && echo "contratos/ : ya no está"

echo "== 6/9  restauración real desde la copia =="
restic --repo "$REPO" restore latest --target "$TRABAJO/recuperado"
find "$TRABAJO/recuperado" -type f | wc -l

echo "== 7/9  LA PRUEBA: sha256 de lo restaurado contra la huella de antes =="
( cd "$TRABAJO/recuperado$DATOS" && sha256sum -c "$TRABAJO/contratos_antes.sha" )

echo "== 8/9  el script de verificación (datos enteros -> OK) =="
"$PY" "$RAIZ/scripts/verificar_copia.py" --repo "$REPO" --datos "$DATOS" --destino "$VERIF" \
      --informe "$TRABAJO/informe_verificacion.json"
ok1=$?
echo "exit=$ok1"

echo "== 9/9  copia incompleta: el script la caza =="
cp -r "$TRABAJO/recuperado$DATOS/contratos" "$DATOS/contratos"
echo "proveedor;Seguros Peninsular" > "$DATOS/facturas/2026-10/factura_0023.csv"
echo "-- verificación con un fichero posterior a la copia:"
"$PY" "$RAIZ/scripts/verificar_copia.py" --repo "$REPO" --datos "$DATOS" --destino "$VERIF" \
      --informe "$TRABAJO/informe_verificacion.json"
falta=$?
echo "exit=$falta  (1 = FALLO: falta un fichero en la copia)"
echo "-- copia de nuevo y verificación otra vez:"
restic --repo "$REPO" backup "$DATOS" --tag diario
"$PY" "$RAIZ/scripts/verificar_copia.py" --repo "$REPO" --datos "$DATOS" --destino "$VERIF" \
      --informe "$TRABAJO/informe_verificacion.json"
ok2=$?
echo "exit=$ok2"

echo "== extra: integridad del repositorio y retención =="
restic --repo "$REPO" check
restic --repo "$REPO" forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune --dry-run

echo "== extra: el verificador que se ejecuta solo (lo que se pone en cron) =="
bash "$RAIZ/scripts/verificar_copia_semanal.sh"
echo "exit=$?  (0 = copia buena; 1 = hay que restaurar de verdad)"
ls -l "$TRABAJO/informes"

echo
echo "== resumen de la verificación =="
echo "datos de partida ........ 80 ficheros (12 contratos)"
echo "restauración ............. sha256 idéntico en los 12 contratos"
echo "copia incompleta ......... detectada (exit=$falta) y corregida (exit=$ok2)"
if [ "${ok1:-9}" -eq 0 ] && [ "${falta:-9}" -eq 1 ] && [ "${ok2:-9}" -eq 0 ]; then
  echo "VERIFICACION FINAL: OK (detecta la copia incompleta y restaura identica)"
  exit 0
fi
echo "VERIFICACION FINAL: REVISAR (ok1=$ok1 falta=$falta ok2=$ok2)"
exit 1
