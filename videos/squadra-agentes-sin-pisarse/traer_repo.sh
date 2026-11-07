#!/usr/bin/env bash
# Trae el repositorio público a la revisión exacta que se usó en el vídeo.
# No hay copias nuestras de su código: esto clona el original de su autor.
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"

REV="0e56ba3107d80275bd5460d29dfcc52bed28d979"
rm -rf repo
git clone -q https://github.com/dagoSte/squadra.git repo
git -C repo checkout -q "$REV"
echo "repo en la revisión $(git -C repo rev-parse --short HEAD) — $(git -C repo log -1 --format=%s)"
