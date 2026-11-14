#!/usr/bin/env bash
# Los comandos del vídeo, en el mismo orden y con el mismo resultado esperado.
#   bash demo.sh        -> 0 si los tres casos dan lo que dice el vídeo
set -uo pipefail
cd "$(dirname "$0")"

echo "== 1/3  formulario bueno: el script debe leer la confirmación =="
python verificar.py; ok=$?
echo "   -> salida=$ok"

echo
echo "== 2/3  formulario con el id cambiado: debe fallar =="
python verificar.py --pagina formulario_roto.html; roto=$?
echo "   -> salida=$roto"

echo
echo "== 3/3  formulario bueno, otro texto esperado: debe fallar =="
python verificar.py --esperado "Mensaje enviado"; otro=$?
echo "   -> salida=$otro"

echo
if [ "$ok" -ne 0 ] || [ "$roto" -ne 1 ] || [ "$otro" -ne 1 ]; then
  echo "FALLO: los códigos de salida no son 0 / 1 / 1 (son $ok / $roto / $otro)"
  exit 1
fi
echo "OK: 0 / 1 / 1"
