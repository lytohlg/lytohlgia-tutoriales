#!/usr/bin/env bash
# Las peticiones de la demo. Cada caso es un escenario del vídeo.
# El cuerpo va idéntico al del cliente: lo único que cambia es la cabecera.
set -u
U=http://127.0.0.1:8095/v1/chat/completions
K='Authorization: Bearer local-demo'
J='Content-Type: application/json'

case "${1:-}" in
  factura)
    curl -s -o /dev/null -w 'factura enviada: HTTP %{http_code}\n' "$U" \
      -H "$K" -H "$J" \
      -d '{"model":"gpt-4","messages":[{"role":"user","content":"cuanto suma la factura de marzo"}]}'
    ;;
  sin-clave)
    curl -s -o /dev/null -w 'sin clave: HTTP %{http_code}\n' "$U" -H "$J" \
      -d '{"model":"gpt-4","messages":[{"role":"user","content":"hola"}]}'
    ;;
  con-clave)
    curl -s -o /dev/null -w 'con clave: HTTP %{http_code}\n' "$U" -H "$K" -H "$J" \
      -d '{"model":"gpt-4","messages":[{"role":"user","content":"hola"}]}'
    ;;
  mapa)
    curl -s -o /dev/null "$U" -H "$K" -H "$J" \
      -d '{"model":"gpt-4","messages":[{"role":"user","content":"uno"}]}'
    curl -s -o /dev/null "$U" -H "$K" -H "$J" \
      -d '{"model":"gpt-4o","messages":[{"role":"user","content":"dos"}]}'
    echo "dos peticiones: gpt-4 y gpt-4o"
    ;;
  stream)
    curl -s -N "$U" -H "$K" -H "$J" \
      -d '{"model":"gpt-4","messages":[{"role":"user","content":"resume la factura"}],"stream":true}'
    ;;
  ollama)
    curl -s http://127.0.0.1:8095/api/chat -H "$K" -H "$J" \
      -d '{"model":"gpt-4","messages":[{"role":"user","content":"hola desde ollama"}]}'
    ;;
  consulta)
    curl -s -o /dev/null "$U" -H "$K" -H "$J" \
      -d '{"model":"gpt-4","messages":[{"role":"user","content":"consulta"}]}'
    echo "peticion enviada"
    ;;
  *)
    echo "uso: pide.sh {factura|sin-clave|con-clave|mapa|stream|ollama|consulta}"
    ;;
esac
