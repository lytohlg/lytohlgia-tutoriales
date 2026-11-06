#!/usr/bin/env bash
# Trae el repositorio público en la revisión que se comenta en el vídeo.
# Solo se usa fuera de Docker; la imagen del entorno ya lo trae dentro.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
git clone --quiet https://github.com/Kemerd/claude-hardware-in-the-loop.git repo
cd repo
git checkout --quiet cfc1f19403b2a8806ab8235d5606730806380ce6
git log -1 --format='%h %s'
