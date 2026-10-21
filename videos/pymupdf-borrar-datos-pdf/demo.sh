#!/usr/bin/env bash
# Demo del vídeo «PyMuPDF: borra datos privados de un PDF de verdad» — @lytohlgIA
# Son los comandos del vídeo, en el mismo orden y con los mismos números.
# Rutas RELATIVAS: todo se escribe dentro de la carpeta donde ejecutes esto.
set -euo pipefail

echo "== el DNI tapado se puede leer: tapar no es borrar =="

echo
echo "-- 0. cuatro documentos con datos inventados (y la lista de lo sembrado)"
python3 scripts/sembrar_docs.py

echo
echo "-- 1. cuántos datos personales hay de verdad en la carpeta"
python3 scripts/estado.py entrada

echo
echo "-- 2. la censura falsa: un rectángulo negro ENCIMA del texto"
python3 scripts/censura_falsa.py

echo
echo "-- 3. lo mismo con OTRO programa que no es Python"
DNI="$(head -1 datos_conocidos.txt)"
pdftotext censura_falsa.pdf - | grep -n "$DNI"
echo "(el DNI sigue ahí, en la línea 3 del texto extraído)"

echo
echo "-- 4. la censura de verdad: marcar y APLICAR la redacción"
python3 scripts/censura_real.py

echo
echo "-- 5. el mismo pdftotext sobre el fichero redactado"
if pdftotext censura_real.pdf - | grep -n "$DNI"; then
  echo "(inesperado: queda texto)"
else
  echo "(nada: cero apariciones)"
fi

echo
echo "-- 6. la carpeta entera, con el patrón ingenuo (v1)"
python3 scripts/lote.py v1

echo
echo "-- 7. verificación independiente contra la lista de secretos sembrados"
python3 scripts/verificar.py salida_v1

echo
echo "-- 8. el patrón que faltaba: el DNI con puntos (v2)"
python3 scripts/lote.py v2

echo
echo "-- 9. la misma verificación, ahora sin fugas"
python3 scripts/verificar.py salida_v2

echo
echo "-- 10. la ficha del fichero: autor, asunto, productor"
python3 scripts/metadatos.py

echo
echo "-- 11. el límite de un PDF escaneado: para el script no tiene datos"
python3 scripts/limites.py

echo
echo "-- 12. el límite de los campos de formulario"
python3 scripts/formulario.py
python3 scripts/campos.py

echo
echo "== fin: los PDF de salida_v2/ no contienen ninguno de los datos sembrados =="
