#!/usr/bin/env bash
# Demo del vídeo «imap_tools: convierte correos en tareas con Python» — @lytohlgIA
# Son los comandos del vídeo, en el mismo orden. Rutas RELATIVAS y sin claves:
# el buzón es un servidor de correo de pruebas local (GreenMail), no tu correo.
set -euo pipefail

echo "== correo entrante -> tarea con vencimiento (imap_tools + SQLite) =="

echo
echo "-- 1. levantar el buzón de correo de pruebas (SMTP 3025 / IMAP 3143)"
bash scripts/arrancar_buzon.sh

echo
echo "-- 2. llegan tres correos: se envían de verdad por SMTP"
python3 scripts/sembrar.py

echo
echo "-- 3. leer la bandeja por IMAP con imap_tools"
python3 scripts/listar_buzon.py

echo
echo "-- 4. el adjunto de la factura, bajado del propio correo"
python3 scripts/listar_buzon.py --adjuntos

echo
echo "-- 5. reglas: cada correo con regla se convierte en una tarea"
python3 scripts/reglas.py --no-mover

echo
echo "-- 6. la misma pasada otra vez: ni una tarea duplicada"
python3 scripts/reglas.py --no-mover

echo
echo "-- 7. los correos ya convertidos se mueven a Procesados"
python3 scripts/reglas.py

echo
echo "-- 8. qué toca esta semana"
python3 scripts/tareas.py --semana
