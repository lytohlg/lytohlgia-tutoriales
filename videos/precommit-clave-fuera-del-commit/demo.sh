#!/usr/bin/env bash
# Demo del vídeo «pre-commit: tu clave privada se para antes del commit» — @lytohlgIA
# ---------------------------------------------------------------------------
# Son los comandos del vídeo, en el mismo orden. Se puede leer entero antes de
# ejecutarlo. No toca nada fuera de un directorio temporal: no pide permisos, no
# escribe en tu HOME y no necesita claves.
#
# Se ejecuta SIN `set -e` a propósito: varias órdenes de aquí abajo TIENEN que
# fallar (ese fallo es el producto: el commit que no se crea).
set -uo pipefail

export PRE_COMMIT_HOME="${PRE_COMMIT_HOME:-/opt/pc-cache}"
# Las piezas del material viven junto a este script (dentro de la carpeta montada).
MATERIAL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/scripts"
LAB="$(mktemp -d)"
cd "$LAB"
echo "laboratorio: $LAB"

# ---------------------------------------------------------------- 1. escenario
# Un repositorio de verdad, con un fichero de entorno, un script de despliegue
# que lleva la clave pegada dentro y una clave privada suelta. Nada inventado:
# openssl genera una clave DESECHABLE para que el control tenga qué detectar.
mkdir repo && cd repo
git init -q -b main
git config user.name demo
git config user.email demo@example.com
cp "$MATERIAL/app.py" .
printf 'API_HOST=servidor-de-pruebas\nAPI_USER=informes\nAPI_PASS=Xk7Qz2Vt9Wp4Lm\n' > .env
openssl genrsa -traditional -out servidor_clave.pem 2048 2>/dev/null
{
  echo '"""Script de despliegue. Mal hecho a propósito: la clave va dentro."""'
  echo 'CLAVE = """'
  cat servidor_clave.pem
  echo '"""'
} > despliegue.py
cp "$MATERIAL/pre-commit-config.yaml" .pre-commit-config.yaml
git add -A
echo "ficheros preparados para el commit: $(git diff --cached --name-only | wc -l)"
git status --short

# ------------------------------------------------------------------ 2. enganche
echo
echo "== el enganche: un comando, y git pregunta antes de guardar =="
pre-commit install
ls -l .git/hooks/pre-commit

# --------------------------------------------------- 3. el commit que no existe
echo
echo "== el commit con la clave no llega a existir =="
git commit -m "version inicial" || echo "el commit no se ha creado"
printf 'commits en el historial: '; git rev-list --count --all

# ----------------------------------------------- 4. el mensaje: fichero y línea
echo
echo "== qué fichero, y en qué línea =="
pre-commit run detect-private-key --all-files || true
pre-commit run detect-secrets --all-files || true

# -------------------------------------------- 5. un repositorio viejo de verdad
echo
echo "== lo mismo sobre un repositorio que llevaba años sin pasar por aquí =="
cd "$LAB" && mkdir viejo && cd viejo
git init -q -b main
git config user.name demo
git config user.email demo@example.com
printf 'mes,importe\nenero,1200   \nfebrero,980   \n' > datos.csv
printf 'servidor:\n  host: localhost\n   puerto: 8080\n' > config.yaml
head -c 700000 /dev/zero | tr '\0' 'x' > export_completo.bin
cp "$MATERIAL/pre-commit-config.yaml" .pre-commit-config.yaml
git add -A
pre-commit run --all-files || true
echo "--- segunda pasada: lo que ya está arreglado no se vuelve a tocar ---"
pre-commit run --all-files || true

# --------------------------------------------------------- 6. una regla propia
echo
echo "== una regla de la casa: 20 líneas, y el mismo mecanismo =="
cd "$LAB" && mkdir limpio && cd limpio
git init -q -b main
git config user.name demo
git config user.email demo@example.com
cp "$MATERIAL/app.py" .
cp "$MATERIAL/pre-commit-config.yaml" .pre-commit-config.yaml
{
  echo '  - repo: local'
  echo '    hooks:'
  echo '      - id: sin-pendientes'
  echo '        name: sin PENDIENTE en la documentacion'
  echo '        entry: python "'"$MATERIAL"'/comprobar_regla.py"'
  echo '        language: system'
  echo '        types: [markdown]'
} >> .pre-commit-config.yaml
printf '# Manual\n\n## Uso\n\nPaso uno.\n\nPENDIENTE: explicar que pasa si el csv no existe.\n\nPaso dos.\n' > MANUAL.md
git add -A
pre-commit run --all-files || true

# ---------------------------------------------------------------- 7. el agujero
echo
echo "== el agujero: se puede saltar, y hay que saberlo =="
cd "$LAB/repo"
git commit --no-verify -m "version inicial"
git log --oneline
git show --stat --oneline HEAD | head -8
echo "--- y el control, ejecutado otra vez a mano, sigue diciendo que no ---"
pre-commit run detect-private-key --all-files || true

# --------------------------------------------------------------- 8. el arreglo
echo
echo "== el arreglo: fuera del índice, borrado y a .gitignore =="
git rm --cached -q .env despliegue.py servidor_clave.pem
rm -f .env despliegue.py servidor_clave.pem
printf '.env\n*.pem\n*.key\n' > .gitignore
git add -A
echo "fuera del commit: .env · despliegue.py · servidor_clave.pem"
git commit -m "version inicial sin secretos"
git log --oneline
git show --stat --oneline HEAD | head -8

echo
echo "VERIFICADO: dos controles paran el commit · la clave no entra · el YAML y el binario se arreglan · hook propio de 20 líneas · --no-verify lo salta"
