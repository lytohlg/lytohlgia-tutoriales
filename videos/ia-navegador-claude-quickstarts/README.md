# Tu IA no puede navegar: 6 llamadas de Claude Quickstarts, una por una

> Material del vídeo **Tu IA no puede navegar: 6 llamadas de Claude Quickstarts, una por una** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Le pides a tu asistente de IA que entre en una página, lea una tabla y pulse un botón. Te contesta
con un párrafo. No puede: solo tiene una salida, texto. Para que haga algo en una web hace falta un
programa que abra el navegador, lea lo que hay, decida qué pulsar y vuelva a leer el resultado.

Este material enseña ese programa por dentro, con el ejemplo oficial de Anthropic
([`anthropics/claude-quickstarts`](https://github.com/anthropics/claude-quickstarts), licencia MIT):
qué llamadas hace un agente, qué le devuelve el navegador y qué se rechaza. Y lo ejecuta **sin clave
de API y sin modelo**, porque el ejercicio del repositorio manda las llamadas que mandaría un modelo
y enseña las respuestas tal cual llegan.

## Qué vas a conseguir

Ver, llamada por llamada, cómo un agente de IA usa un navegador de verdad: qué pide, qué le devuelve
el navegador y qué se rechaza. Sin clave de API.

## Requisitos

**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).
- Chromium (la imagen del contenedor ya lo trae; si ejecutas fuera de Docker, instálalo).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base).

## Entorno de pruebas

Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (los tres van en esta carpeta, no hay más):
- `entorno/Dockerfile` — describe la máquina: imagen base (Python 3.12), Chromium y las dos
  dependencias de Python con la versión fijada.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de las claves que necesite el material. Este no necesita ninguna; el
  fichero queda como recordatorio de que las claves nunca van dentro de un script.

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta.

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos porque descarga la imagen
base e instala Chromium):
```bash
docker --context default build -t repro-ia-navegador-claude-quickstarts:local entorno
```

**Paso 2 — ejecutar la demo dentro**, con esta carpeta montada en **solo lectura** (el script no
puede tocar tus ficheros originales: trabaja sobre una copia en `/tmp`):
```bash
docker --context default run --rm --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-ia-navegador-claude-quickstarts:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno.

**Un detalle que importa:** dentro del contenedor se ejecuta como root, y Chromium no arranca su
propio sandbox como root. El driver del repositorio lo sabe y añade `--no-sandbox` en ese caso
(está en `cdp_browser.py`, con el comentario que lo explica). Si lo ejecutas en tu máquina con tu
usuario normal, el sandbox de Chromium se queda activado.

## Pasos

1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd ia-navegador-claude-quickstarts
   ```
2. Construye el entorno (paso 1 de arriba).
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero

| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `exercise.py` | El ejercicio **oficial** del repositorio: sirve una página local y manda las seis llamadas que mandaría un modelo, sin modelo y sin clave. No lo he tocado. |
| `cdp_browser.py` | El **driver oficial**: arranca Chromium, habla con él por CDP e implementa las cinco herramientas (abrir, leer, pulsar, extraer texto, esperar). Es el fichero que explica de dónde salen los `ref_N`. No lo he tocado. |
| `run.py` | El **bucle con modelo**: construye el driver, se lo pasa al `tool_runner` del SDK y deja que el modelo decida. Necesita una clave; sin ella falla con un error de autenticación, y eso también se ve. No lo he tocado. |
| `requirements.txt` | Las dependencias del repositorio (`anthropic`, `websockets`). |
| `mipagina.py` | Mi página de prueba: un formulario real (correo, plan, botón) y un enlace, servido en local, para ver los `ref_N` de campos de formulario y una navegación de verdad. |
| `fuera_del_driver.py` | Comprueba qué pasa cuando se pide una herramienta que el driver **no** implementa. |
| `chromium-sin-sandbox.sh` | Lanzador de Chromium para cuando la demo se ejecuta **sin ser root** dentro de un contenedor: añade `--no-sandbox` porque ahí no se puede montar el sandbox. `demo.sh` lo usa solo en ese caso. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base, Chromium y versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de claves (este material no usa ninguna). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso

- **`exercise.py`** — abre un servidor local con una página diminuta (`h1`, un botón, un enlace) y
  lanza el driver con una política que solo admite esa página. Después manda, una a una, las llamadas
  que mandaría un modelo: `navigate`, `read_page`, `left_click`, `get_page_text` y dos que deben
  fallar (una dirección fuera de la página y una espera de 31 segundos). Imprime lo que devuelve cada
  una. **Cuatro responden y dos se rechazan; el script comprueba que así sea y falla si no.**
- **`cdp_browser.py`** — el driver. Arranca Chromium con un perfil temporal (`--user-data-dir` en un
  directorio que se borra al cerrar), se conecta a su puerto de depuración y traduce cada herramienta
  a una orden del protocolo CDP. `read_page` ejecuta un pequeño script dentro de la página que numera
  encabezados, enlaces, botones y campos de formulario como `ref_1`, `ref_2`… y `left_click` resuelve
  ese `ref` a coordenadas reales antes de pulsar.
- **`run.py`** — el bucle con modelo. `tools=[browser]` le dice al SDK que el modelo puede llamar a
  las herramientas del driver; el `tool_runner` se encarga de ir y venir (el modelo pide, el driver
  ejecuta, el resultado vuelve al modelo) hasta que termina. Con `ALLOWED_DOMAINS` se limita a qué
  hosts puede ir, y `HEADLESS=0` sirve para ver el navegador en pantalla.
- **`mipagina.py`** — igual que el ejercicio, pero contra una página mía con formulario, para ver que
  los `ref_N` los genera el driver (no el modelo) y que un clic en un `ref` navega de verdad.
- **`fuera_del_driver.py`** — pide una herramienta que el driver no implementa (`take_screenshot`) y
  enseña la respuesta del SDK: `unknown browser toolset member`. Es la prueba de que el SDK solo
  ofrece lo que tú implementas.
- **`demo.sh`** — la lista de órdenes que se ejecutan en el vídeo, en ese orden. Si el vídeo hace algo
  que no está aquí, el material está mal. Se puede leer entero antes de ejecutarlo.
- **`pruebas/pruebas.sh`** — la prueba de verdad: construye la imagen, copia la carpeta dentro del
  contenedor y ejecuta la demo, y después **comprueba** lo que el vídeo afirma: cuatro llamadas
  respondidas, dos rechazadas, los `ref_N` del formulario, el bloqueo por política y la negativa a
  usar una herramienta no implementada. Si algo no cuadra, para y lo dice.

## Resultado esperado

6 llamadas, 4 respondidas y 2 rechazadas. Y, con `run.py`, el error de autenticación que demuestra
que sin clave no hay modelo: el bucle se corta antes de empezar.

## Coste y credenciales

Nada: todo lo que hace este material es gratis y no necesita claves. `run.py` es el único que pide
una clave (`ANTHROPIC_API_KEY`) y en la demo se ejecuta **sin** ella, a propósito, para ver qué pasa.

## Solución de problemas

- **«No usable sandbox»**: estás ejecutando Chromium como root sin `--no-sandbox`. El driver lo añade
  solo cuando detecta root; si ejecutas fuera del contenedor, hazlo con tu usuario normal.
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia

MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio. Los ficheros `exercise.py`, `cdp_browser.py`, `run.py` y `requirements.txt` vienen de
[`anthropics/claude-quickstarts`](https://github.com/anthropics/claude-quickstarts), también MIT, y
se incluyen sin cambios.
