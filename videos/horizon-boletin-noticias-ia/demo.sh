#!/usr/bin/env bash
# Demo del vídeo «Horizon: tu radar de noticias con IA, filtrado y puntuado (Python)» — @lytohlgIA
# Lo que se ve en pantalla, en el mismo orden. Rutas relativas, todo dentro de esta carpeta.
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"

echo "== Horizon: tu radar de noticias con IA, filtrado y puntuado =="
echo
echo "1) El config: de dónde lee y con qué criterio decide"
python3 scripts/leer_config.py ejemplo/config.json
echo
echo "2) Los perfiles: el criterio está escrito en markdown, no en el código"
python3 scripts/listar_rubricas.py ejemplo/reglas tech-news
echo
echo "3) Un boletín ya generado, leído por la máquina"
python3 scripts/leer_boletin.py ejemplo/boletin-es.md
echo
echo "Listo. La ejecución completa necesita clave del modelo; aquí no se llama a nadie."
