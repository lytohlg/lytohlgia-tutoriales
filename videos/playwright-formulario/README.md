# Automatiza la prueba de tu formulario web con Playwright Python

> Material del vídeo **Automatiza la prueba de tu formulario web con Playwright Python** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

**El problema que resuelve:** un formulario de contacto deja de enviar y nadie se entera. La página
carga, el botón sigue ahí, el visitante cree que ha enviado, y el fallo aparece cuando alguien se queja
por otra vía. Este material abre el formulario en un navegador de verdad, lo rellena, pulsa enviar,
espera la confirmación y comprueba el texto que ve el visitante: si no es el esperado, termina con código
de salida 1 y guarda una captura del momento exacto del fallo.

## Qué vas a conseguir
Un script que dice en siete segundos si tu formulario sigue enviando, con código de salida de verdad
(0 = envía, 1 = roto) y una captura PNG cuando algo falla. Y entender los tres fallos típicos: el `id`
renombrado, el texto de confirmación cambiado y el envío que ya no responde.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1,2 GB de disco libre (la imagen base más el navegador, que son ~700 MB).
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base y el navegador).


## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (van en esta carpeta, no hay más):
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de las claves que necesite el material. Aquí está vacía a propósito: este
  material no pide ninguna clave.

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno (basta con `docker compose up`).

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base y el navegador):
```bash
docker --context default build -t repro-playwright-formulario:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-playwright-formulario:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno. El contenedor de pruebas no
necesita red: el servidor de la web de ejemplo y las páginas van dentro del paquete y escuchan en
`127.0.0.1:8000`. Si el navegador se cierra solo, sube la memoria compartida («shm») con
`--shm-size=512m`.

**Detalles de nuestra ejecución, por si tu caso es distinto:** las órdenes de arriba son las mismas
que usamos nosotros, tal cual. El `--context default` fuerza el motor Docker local — útil si tienes
configurado además uno remoto; si en tu equipo solo hay uno, déjalo igual (funciona) o quítalo.
Ejecutamos con el usuario `1000:1000` para no correr como root y con `HOME=/tmp` para que el
contenedor no dependa de nada de fuera. El contenedor no lleva credenciales dentro: este material no
las usa.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd playwright-formulario
   ```
2. (Opcional) Mira el entorno que se va a usar, sin construir nada:
   ```bash
   cat entorno/Dockerfile
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

Para usarlo con **tu** web, se cambian tres cosas de `verificar.py`: la dirección, el texto que debe
aparecer (`--esperado`) y los campos que rellenas. La página local se elige con `--pagina`.

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden, con la comprobación de los tres códigos de salida. |
| `verificar.py` | El script del vídeo: abre el navegador, rellena el formulario, pulsa, espera, lee y captura. Devuelve 0 o 1. |
| `servidor.py` | Servidor mínimo de la web de ejemplo: sirve las páginas y recibe el POST (deja cada mensaje en `mensajes.jsonl`). |
| `sitio/formulario.html` | El formulario que funciona: es el caso que debe salir 0. |
| `sitio/formulario_roto.html` | El mismo formulario con el `id` del campo nombre cambiado a `nombre_completo`: el fallo que se detecta. |
| `requisitos.txt` | La dependencia con la versión fijada (`playwright==1.65.0`). |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (aquí: ninguna). Se copia a `.env`, que nunca se sube. |
| `.gitignore` | Lo que no se versiona: las capturas y el buzón que se generan al ejecutar, y el `.env`. |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`verificar.py`** — cinco pasos numerados que se imprimen en pantalla: (1) arranca el servidor de la
  web de ejemplo y abre la página; (2) rellena nombre, correo y mensaje; (3) pulsa «Enviar mensaje»;
  (4) espera la respuesta con un tope de cinco segundos; (5) lee el texto que ve el visitante y lo
  compara con el esperado. Guarda una captura en `capturas/` y termina con 0 si coincide, 1 si no.
  El tope de tiempo se pone en el **contexto** del navegador, no en la página: `fill()` y `click()`
  heredan el del contexto (30 s por defecto), y ahí se pierde una tarde si no se sabe.
- **`servidor.py`** — 40 líneas de `http.server`: sirve `sitio/` y responde al POST con el texto de
  confirmación. Existe para que el material no dependa de ninguna web externa.
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo, en ese
  orden, y comprueba que los códigos de salida sean 0 / 1 / 1. Si el vídeo hace algo que no está aquí, el
  material está mal.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de `python:3.12-slim`, instala
  `libatomic1` (sin ella el driver de Playwright ni arranca en slim), Playwright en la versión fijada y el
  navegador en `/opt/ms-playwright`, que es una ruta que cualquier usuario puede leer.
- **`pruebas/pruebas.sh`** — la prueba de verdad: comprueba que Docker responde, construye la imagen de
  `entorno/Dockerfile`, copia la carpeta a un directorio temporal dentro del contenedor y ejecuta ahí la
  demo con la carpeta original montada en solo lectura. Si algo falla, para y dice en qué paso.

## Resultado esperado
```
== 1/3  formulario bueno: el script debe leer la confirmación ==
[1/5] abro http://127.0.0.1:8000/formulario.html
[2/5] relleno nombre, correo y mensaje
[3/5] pulso "Enviar mensaje"
[4/5] espero la respuesta del formulario
[5/5] leo el resultado: "Gracias, Ana: hemos recibido tu mensaje"
  captura guardada: capturas/formulario.png (21 KB)
RESULTADO: OK  -> código de salida 0
   -> salida=0

== 2/3  formulario con el id cambiado: debe fallar ==
[1/5] abro http://127.0.0.1:8000/formulario_roto.html
[2/5] relleno nombre, correo y mensaje
FALLO: la página no llegó al estado esperado
  TimeoutError: Page.fill: Timeout 5000ms exceeded.
  captura guardada: capturas/formulario_roto.png (12 KB)
RESULTADO: FALLO  -> código de salida 1
   -> salida=1

== 3/3  formulario bueno, otro texto esperado: debe fallar ==
FALLO: esperaba encontrar «Mensaje enviado» y no está
RESULTADO: FALLO  -> código de salida 1
   -> salida=1

OK: 0 / 1 / 1
```
Los tiempos medidos en el contenedor de pruebas: 2 s el caso bueno y 7 s el roto (los cinco segundos del
tope más el arranque del navegador).

## Coste y credenciales
Nada: este material es gratis y no necesita claves. El único coste es la descarga del navegador
(~700 MB) la primera vez.

## Solución de problemas
- **`Executable doesn't exist at ...`**: falta el navegador. Ejecuta `playwright install chromium` o usa
  la imagen de `entorno/Dockerfile`, que ya lo trae.
- **`Page.fill: Timeout 30000ms exceeded`** (30 s en vez de 5): el tope se puso con
  `page.set_default_timeout()`, que no afecta a `fill()` ni a `click()`. Va en el contexto:
  `contexto.set_default_timeout(5000)`.
- **El driver no arranca / `libatomic1`**: en imágenes `slim` falta esa librería; está en el
  `entorno/Dockerfile`.
- **El navegador se cierra solo en Docker**: sube la memoria compartida con `--shm-size=512m`.
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Vas a comprobar una web que no es tuya**: cuidado, automatizar la web de otra persona puede ir contra
  sus términos de uso. Este material está pensado para tu propio formulario.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Qué NO demuestra
No prueba cómo se ve en un móvil real, no mide rendimiento ni accesibilidad y no sustituye a una persona
probando con mala intención. Comprueba el camino que tú escribes, con el texto que tú esperas: es una
red, no una garantía.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
