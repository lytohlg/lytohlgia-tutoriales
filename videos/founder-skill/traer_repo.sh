#!/usr/bin/env bash
# Trae el repositorio público del autor, en la MISMA revisión que se usó en el vídeo.
# El vídeo no copia su código: lo clona, y por eso se puede comprobar qué revisión era.
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REVISION="fd9385b"
DESTINO="$AQUI/repo"

if [ -d "$DESTINO/.git" ]; then
  echo "Ya está el repositorio en $DESTINO"
else
  echo "Clonando Jakeschincariol/founder-skill en la revisión $REVISION ..."
  git clone -q https://github.com/Jakeschincariol/founder-skill.git "$DESTINO"
  git -C "$DESTINO" checkout -q "$REVISION"
fi

echo -n "Revisión en uso: "
git -C "$DESTINO" rev-parse --short HEAD
git -C "$DESTINO" log -1 --date=short --format='Fecha: %ad — %s'
