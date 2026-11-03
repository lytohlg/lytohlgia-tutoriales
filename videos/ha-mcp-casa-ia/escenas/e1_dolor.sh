#!/bin/sh
# El "antes": controlar la casa a pelo, con curl contra la API REST de Home Assistant.
set -e
[ -f .env ] || python3 preparar_entorno.py > /dev/null
URL=$(grep '^HOMEASSISTANT_URL=' .env | cut -d= -f2-)
TOKEN=$(grep '^HOMEASSISTANT_TOKEN=' .env | cut -d= -f2-)
# La entidad se elige en caliente: el servidor de demo es compartido y sus nombres cambian.
LUZ=$(python3 escenas/elegir_entidad.py 2>/dev/null)
DOM=$(echo "$LUZ" | cut -d. -f1)
AUTH="Authorization: Bearer $TOKEN"

echo '$ curl -s -H "Authorization: Bearer $TOKEN" $URL/api/states | wc -c'
curl -s -H "$AUTH" "$URL/api/states" | wc -c
echo '   -> bytes de JSON con TODA la casa'
sleep 2.4

echo
echo '$ curl -s -H "Authorization: Bearer $TOKEN" $URL/api/states | head -c 200'
curl -s -H "$AUTH" "$URL/api/states" | head -c 200
echo
sleep 2.4

echo
echo '$ curl -s -X POST -H "Authorization: Bearer $TOKEN" \'
echo '       -H "Content-Type: application/json" \'
echo "       -d '{\"entity_id\":\"$LUZ\"}' \\"
echo '       $URL/api/services/$DOM/turn_on'
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" \
     -d "{\"entity_id\":\"$LUZ\"}" \
     "$URL/api/services/$DOM/turn_on" | head -c 200
echo
echo '   -> la entidad obedece: la API funciona'
sleep 2.4

# devolverla a como estaba
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" \
     -d "{\"entity_id\":\"$LUZ\"}" \
     "$URL/api/services/$DOM/turn_off" > /dev/null

echo
echo '   Pero esto lo tiene que saber TU IA: la URL, el token, el endpoint,'
echo '   el nombre exacto de la entidad y la forma del JSON.'
sleep 2.0
echo '   Y cada cliente (Claude, ChatGPT, Cursor, n8n...) lo aprende por su cuenta.'
sleep 3
