#!/usr/bin/env bash
# Demo del vídeo «invoice2data: extrae datos de facturas PDF a CSV con Python» — @lytohlgIA
# Son los comandos del vídeo, en el mismo orden. Rutas RELATIVAS y valores en
# variables de entorno: nada hardcodeado.
#
#   bash demo.sh        -> todos los pasos, en orden
#   bash demo.sh 2 5    -> solo los pasos 2 y 5
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$RAIZ"

[ -f .env ] || cp .env.example .env
set -a
. ./.env
set +a

ENTRADA="${I2D_ENTRADA:-entrada}"
PLANTILLAS="${I2D_PLANTILLAS:-plantillas}"
CORREGIDAS="${I2D_CORREGIDAS:-plantillas_corregidas}"
MOTOR="${I2D_MOTOR:-pdfminer}"
SALIDA="${I2D_SALIDA:-salida}"
TODAS="${I2D_TODAS:-todas}"
NUEVO="${I2D_NUEVO:-vega}"
ARCHIVO="${I2D_ARCHIVO:-procesadas}"
BORRADOR="${I2D_BORRADOR:-borrador_vega.yml}"
PY="${PYTHON:-python3}"
GENERADOR="${I2D_GENERADOR:-hacer_facturas.py}"

cabecera() { printf '\n### %s\n' "$1"; }

paso_0() { # las cuatro facturas de prueba (ficticias: las escribe un script de este material)
  cabecera "0. Las cuatro facturas de prueba"
  "$PY" "$GENERADOR"
  printf -- '-- lo que hay en la bandeja de entrada --\n'
  ls -1 "$ENTRADA"
}

paso_1() { # tres facturas del mismo proveedor, con la plantilla que ya existe
  cabecera "1. Las tres del mismo proveedor, con su plantilla"
  invoice2data -i "$MOTOR" -t "$PLANTILLAS" -f csv -o "$SALIDA" "$ENTRADA"/F-2026-*.pdf
  cat "$SALIDA.csv"
}

paso_2() { # el proveedor que no conozco: sin plantilla no hay tabla
  cabecera "2. El proveedor que la herramienta no conoce"
  set +e
  invoice2data -i "$MOTOR" -t "$PLANTILLAS" -f json -o "$NUEVO" "$ENTRADA"/TV-2026-1188_vega.pdf
  rc=$?
  set -e
  printf 'codigo de salida: %s\n' "$rc"
  cat "$NUEVO.json"
}

paso_3() { # el borrador de plantilla que escribe la propia herramienta
  cabecera "3. El borrador automático de la plantilla que falta"
  printf 'y\n' | invoice2data -i "$MOTOR" --new-template "$ENTRADA/TV-2026-1188_vega.pdf" \
    --template-out "$BORRADOR"
  cat "$BORRADOR"
}

paso_4() { # la plantilla corregida a mano, ya en su sitio
  cabecera "4. La plantilla corregida, ya en su carpeta"
  cp "$CORREGIDAS/vega.yml" "$PLANTILLAS/vega.yml"
  ls -1 "$PLANTILLAS"
}

paso_5() { # leer las cuatro de una pasada y archivar los originales
  cabecera "5. Leer las cuatro de una pasada y archivar los originales"
  mkdir -p "$ARCHIVO"
  set +e
  invoice2data -i "$MOTOR" -t "$PLANTILLAS" -f csv -o "$TODAS" --move "$ARCHIVO" \
    --filename-format '{date} {invoice_number} {desc}.pdf' "$ENTRADA"/*.pdf
  rc=$?
  set -e
  printf 'codigo de salida: %s\n' "$rc"
  cat "$TODAS.csv"
  printf -- '-- lo que ha quedado archivado --\n'
  ls -1 "$ARCHIVO"
}

paso_6() { # comprobación final
  cabecera "6. Comprobación final: la bandeja queda vacía"
  printf 'facturas que siguen en %s: ' "$ENTRADA"
  ls -1 "$ENTRADA" | wc -l || true
}

todo() {
  echo "== invoice2data: de cuatro PDF a una tabla =="
  paso_0
  paso_1
  paso_2
  paso_3
  paso_4
  paso_5
  paso_6
  printf '\n== demo terminada ==\n'
}

case "${1:-todo}" in
  todo) todo ;;
  "")
    echo "uso: bash demo.sh [todo|0|1|2|3|4|5|6] [mas pasos]" >&2; exit 1 ;;
  *)
    for p in "$@"; do
      case "$p" in
        0|1|2|3|4|5|6) "paso_$p" ;;
        *) echo "paso desconocido: $p (uso: todo|0..6)" >&2; exit 1 ;;
      esac
    done ;;
esac
