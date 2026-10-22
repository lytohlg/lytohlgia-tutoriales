#!/usr/bin/env bash
# Demo del vídeo «pypdf: comprueba tu expediente antes de enviarlo» — @lytohlgIA
# Son los comandos del vídeo, en el mismo orden y con los mismos números.
# Rutas RELATIVAS: todo se escribe dentro de la carpeta donde ejecutes esto.
set -euo pipefail

# La clave del ejemplo. En un trabajo real, la pones en tu entorno y NO la escribes aquí.
export EXPEDIENTE_CLAVE=demo-expediente-2026

echo "== un expediente se cae por el documento que nadie comprobó =="

echo
echo "-- 0. el índice exige 6 documentos; la carpeta trae 5"
rm -rf entrada salida
python3 scripts/sembrar_expediente.py
echo
echo "-- 1. la comprobación dice que NO, y dice por qué"
if python3 scripts/comprobar.py; then
  echo "(inesperado: dice que sí)"
else
  echo "(código de salida distinto de 0: no se une y no se entrega)"
fi

echo
echo "-- 2. un PDF que llegó roto a medias: se detecta como ilegible"
printf 'esto no es un PDF\n' > entrada/nomina_ultima.pdf
python3 scripts/comprobar.py || true

echo
echo "-- 3. llega el papel que faltaba: ahora sí"
python3 scripts/sembrar_expediente.py --completo
python3 scripts/comprobar.py

echo
echo "-- 4. unir en el orden del índice, con marcador y numerado, y cifrar"
python3 scripts/unir.py

echo
echo "-- 5. verificar SIN clave, con qpdf (herramienta ajena) y con clave"
python3 scripts/verificar.py

echo
echo "-- 6. el manifiesto: qué documento quedó en qué página"
python3 scripts/manifiesto.py

echo
echo "-- 7. el giro, antes y después, con pdfinfo (herramienta ajena)"
echo "ANTES  -- DNI original (escaneado girado):"
pdfinfo -f 1 -l 1 entrada/dni_titular.pdf | grep -i "rot"
qpdf "--password=$EXPEDIENTE_CLAVE" --decrypt salida/expediente_EXP-2026-0431.pdf salida/descifrado.pdf
echo "DESPUÉS -- hoja 2 del paquete:"
pdfinfo -f 2 -l 2 salida/descifrado.pdf | grep -i "rot"

echo
echo "-- 8. los límites, medidos"
python3 scripts/limites.py

echo
echo "== fin: el paquete sale completo, en el orden del índice, sin giros y con clave =="
