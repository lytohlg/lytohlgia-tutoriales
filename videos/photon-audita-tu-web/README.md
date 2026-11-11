# Photon: lo que tu web expone sin que lo sepas

> Material del vídeo **Photon: lo que tu web expone sin que lo sepas** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Publicas una web y crees que solo se ve lo que está en el menú. Pero una web enseña bastante más:
el correo de quien la hizo en un comentario, un PDF con la tarifa de 2026, un panel interno enlazado
desde el pie, una cadena larga en un fichero de JavaScript que parece una clave.

No lo ves porque nadie te lo enseña junto. Y no hace falta ser un atacante para encontrarlo: basta
con un programa que recorra los enlaces y apunte lo que va encontrando. Eso es lo que hace Photon.

**A quién le duele:** a quien mantiene la web de una empresa pequeña, a quien acaba de heredar un
proyecto, a quien va a publicar y quiere revisar antes. El coste de no mirarlo: un correo que empieza
a recibir spam, un documento interno indexado en Google, una credencial que hay que rotar con prisa.

## Qué vas a conseguir

Ejecutar un crawler de reconocimiento contra **tu** web (o contra un sitio de prueba, como aquí) y
obtener en un minuto un informe legible: correos, ficheros descargables, endpoints y cadenas de alta
entropía que hay publicados sin querer. Y, de paso, aprender por qué la versión actual de la
herramienta **te devuelve un informe vacío sin avisar** y cómo se arregla.

## La herramienta

**Photon** es un crawler escrito en Python, pensado para reconocimiento de un sitio: parte de una URL,
sigue los enlaces hasta la profundidad que le digas y clasifica lo que encuentra —páginas internas,
ficheros, correos, endpoints dentro del JavaScript, cadenas de alta entropía—. Guarda el resultado en
ficheros de texto y lo exporta a JSON.

- Repositorio: <https://github.com/s0md3v/Photon> · licencia GPL-3.0 · versión usada: 1.3.2
- Cuándo usarlo: para auditar **tu** web antes de publicarla, o una web sobre la que tengas permiso
  por escrito.
- Ventaja: un solo comando, sin claves, sin cuenta, y el informe es texto plano que puedes leer.
- Límite importante: **no ejecuta JavaScript** y **no inicia sesión**. Solo ve lo que hay en el HTML y
  en los ficheros enlazados que puede descargar sin autenticarse. Lo que aparece solo tras ejecutar
  el JS de la página, Photon no lo ve.

## Requisitos

**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base).

## Entorno de pruebas

Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos porque descarga la imagen
base y clona el repositorio en un commit exacto):
```bash
docker --context default build -t repro-photon-audita-tu-web:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script trabaja sobre una copia en `/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$PWD:/trabajo:ro" repro-photon-audita-tu-web:local \
  bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace lo anterior y
además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así:** el contenedor no lleva nada tuyo dentro, la carpeta entra montada como solo-lectura
y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu máquina: lo que falla en
limpio es un fallo real, no un resto de tu entorno.

## Pasos

1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd photon-audita-tu-web
   ```
2. Construye el entorno y ejecuta la demo (pasos 1 y 2 de arriba, o `bash pruebas/pruebas.sh`).

La demo hace siempre **dos pasadas**, y el orden importa:

1. genera un sitio de prueba local (datos falsos) y lo sirve en `127.0.0.1:8765`;
2. ejecuta Photon **tal como viene del repositorio** y enseña el informe que produce;
3. aplica los tres arreglos de compatibilidad con Python 3 (ver más abajo);
4. repite la pasada y enseña el informe completo;
5. resume el export JSON y **verifica el resultado**: si falta un solo correo, falla.

## Qué hace cada fichero

| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina de pruebas: `python:3.12-slim`, el repo clonado en un commit exacto y las dependencias con versión fijada. |
| `entorno/material/generar_sitio.py` | Genera el sitio de prueba (HTML, un JS y dos ficheros falsos) con datos de ejemplo. |
| `entorno/material/aplicar_parches.py` | Aplica los tres arreglos de Python 3 y muestra qué línea cambia y por qué. |
| `entorno/material/resumen_export.py` | Cuenta los bloques del `exported.json` que genera Photon. |
| `entorno/material/verificar_resultado.py` | Comprueba el informe: 5 correos, el endpoint del JS y la cadena de alta entropía. Si falta algo, sale con error. |
| `pruebas/pruebas.sh` | Construye el entorno y ejecuta la demo en limpio. Es la prueba previa a publicar. |
| `.env.example` | Plantilla de claves. Este material **no usa ninguna**; se deja por convención. |
| `material.json` | Ficha del índice del repositorio: título, fecha y si pide claves. |
| `paquete.json` | Metadatos del paquete para el publicador (estado, fecha de estreno, salida esperada). |
| `README.md` | Esto. |

### Qué hace cada script, paso a paso

- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo, en
  ese orden. Si el vídeo hace algo que no está aquí, el material está mal.
- **`entorno/Dockerfile`** — imagen base oficial con versión fijada (nada de `latest`), clon del repo
  en el commit `c8d2566` (2026-10-18), dependencias con versión fijada. No copia claves ni tus datos.
- **`pruebas/pruebas.sh`** — comprueba que Docker responde, construye la imagen, ejecuta la demo en
  una copia dentro del contenedor y compara la salida con la esperada. Si algo falla, dice en qué
  paso.

## Los tres defectos (y por qué la demo hace dos pasadas)

Photon se escribió en la época de Python 2 y arrastra tres cosas que en Python 3.11 o superior fallan
**en silencio**: el programa termina, dice «Results saved» y el informe está vacío.

1. **`photon.py`, extracción de intel.** El reemplazo de etiquetas usa
   `re.sub(r'<(script).*?</\1>(?s)', ...)`. El flag `(?s)` va al principio del patrón; al final,
   Python 3.11+ lanza `re.error`. La excepción se traga y no se extrae ni un correo.
   Arreglo: `re.sub(r'<(script).*?</\1>', ..., flags=re.S)`.
2. **`core/requester.py`, lectura de JavaScript.** Solo acepta respuestas con `content-type`
   `text/html` o `text/plain`. Un servidor normal sirve `.js` como `application/javascript`, así que
   **todo el JavaScript se descarta** y el bloque de endpoints nunca se llena.
   Arreglo: aceptar también `javascript`.
3. **`core/utils.py`, entropía.** `string.encode('utf-8').count(chr(number))` cuenta una cadena sobre
   bytes: `TypeError` en Python 3. Por eso `--keys` no devuelve nunca nada.
   Arreglo: contar sobre la cadena.

## Resultado esperado

Con los arreglos aplicados, sobre el sitio de prueba:

```
[+] Files: 1
[+] Intel: 5
[+] Internal: 9
[+] Scripts: 1
[+] External: 2
[+] Endpoints: 1
[+] Keys: 1
```

```
### intel.txt
http://127.0.0.1:8765/equipo.html:EMAIL:laura.mendez@example.com
http://127.0.0.1:8765/equipo.html:EMAIL:presupuestos@example.com
...
### endpoints.txt
(1 línea: la ruta de la API que llama el JavaScript de la página)
```

Última línea de la demo:

```
OK: 5/5 correos, endpoint del JS y la cadena de alta entropía
```

## Coste y credenciales

Nada: todo lo que hace este material es gratis y no necesita claves.

## Uso responsable

Photon sirve para auditar lo tuyo. Recorrer una web ajena sin permiso, y más aún quedarse con los
correos que aparezcan, tiene consecuencias legales en la Unión Europea (RGPD y normativa de servicios
de la sociedad de la información): un correo publicado en una web **no** es un dato libre por el
hecho de estar visible. La demo se ejecuta contra un sitio local inventado, sin tocar ningún dominio
real.

## Solución de problemas

- **«command not found»**: te falta Docker; instálalo y vuelve a empezar.
- **Error de permisos al escribir**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **El informe sale vacío**: es exactamente el defecto que explica este material; comprueba que la
  demo llegó al paso 4 (con los arreglos aplicados).
- **Falla la descarga del repo**: la imagen clona GitHub al construirse; si tu red lo bloquea, no hay
  atajo en ese paso.

## Licencia

El material de esta carpeta es MIT. Photon es GPL-3.0 y se descarga desde su repositorio: aquí no se
redistribuye su código, solo se clona y se le aplican tres líneas de arreglo, explicadas arriba.
