# Encuentra lo que repites en tu historial de IA y tapa tus claves

> Material del vídeo **Encuentra lo que repites en tu historial de IA y tapa tus claves** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Le explicas lo mismo al asistente cada mañana. Cambias el mes, cambias dos palabras, y crees que es
otra petición. Todo eso queda guardado en tu disco, en tres sitios distintos y con tres formatos
distintos que nadie documenta: `.claude/`, `.codex/` y la base de datos de Cursor. Nadie lo lee. Y
dentro hay algo peor: las credenciales que pegaste una vez «para probar» y se quedaron escritas en
texto plano.

Este material lee ese historial, unifica las tres fuentes en una lista, **tapa las credenciales** y
cuenta lo que repites. Nada sale de tu máquina: no hay red, no hay cuenta, no hay clave.

## Qué vas a conseguir

Una lista, ordenada por fecha, con cada petición que has escrito en Claude Code, Codex y Cursor sobre
un proyecto; las credenciales detectadas sustituidas por `[REDACTED]`; y el recuento de tus
repeticiones. En la demo: 47 peticiones de tres fuentes, 1 secreto tapado y 46 clasificadas en 5
tareas, con 13 repeticiones de la misma.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base).


## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (los tres van en esta carpeta, no hay más):
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de las claves que necesite el material. Se copia a `.env` (que **no**
  se sube nunca al repositorio).

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno (basta con `docker compose up`).

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base):
```bash
docker --context default build -t repro-faq-shortcuts:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-faq-shortcuts:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno. El contenedor tiene
red (algunos materiales descargan dependencias al arrancar); lo que **no** tiene son tus datos.

**Detalles de nuestra ejecución, por si tu caso es distinto:** las órdenes de arriba son las mismas
que usamos nosotros, tal cual. El `--context default` fuerza el motor Docker local — útil si tienes
configurado además uno remoto; si en tu equipo solo hay uno, déjalo igual (funciona) o quítalo.
Ejecutamos con el usuario `1000:1000` para no correr como root y con `HOME=/tmp` para que el
contenedor no dependa de nada de fuera. El contenedor no lleva credenciales dentro: las claves, si
el material las necesita, entran por variables de entorno.

## Pasos

No hace falta ninguna clave ni ninguna cuenta: todo se ejecuta en local, sin red.

1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd faq-shortcuts
   ```
2. Comprueba que Docker responde (`docker version`). Es lo único que necesitas instalado.
3. Ejecuta la demo tal cual, que ya crea su propio historial de ejemplo:
   ```bash
   bash demo.sh
   ```
4. Y si quieres la prueba completa, en limpio y con la carpeta original en solo lectura:
   ```bash
   bash pruebas/pruebas.sh
   ```

Cuando quieras usarlo con **tu** historial de verdad, no lances `escenario.py`: apunta el extractor a
tu proyecto y deja que `HOME` sea el tuyo.

```bash
python3 repo/scripts/extract_asks.py ~/tu-proyecto | python3 contar.py
```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `escenario.py` | Crea el historial de ejemplo (los tres formatos) dentro de `entrada/`. Sin él no hay nada que leer. |
| `contar.py` | Las cinco reglas que agrupan las peticiones por tarea. 29 líneas, sin dependencias. |
| `traer_repo.sh` | Clona el repositorio original (`scripts/extract_asks.py` y sus tests) en la revisión exacta del vídeo. El material no copia el código de nadie: lo trae al ejecutar. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial
  con la versión fijada (nada de `latest`, para que mañana funcione igual), instala lo que el
  material necesita y deja el directorio de trabajo preparado. No copia claves ni tus datos: eso
  entra después, por variables de entorno y solo si tú las pones.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en cuatro pasos: (1) comprueba que Docker
  responde; (2) construye la imagen de `entorno/Dockerfile`; (3) copia la carpeta a un directorio
  temporal dentro del contenedor y ejecuta ahí la demo, con la carpeta original montada en solo
  lectura; (4) compara la salida con la esperada y te dice si cuadra. Si algo falla, para y te dice
  en qué paso. No escribe nada fuera del contenedor.
- **`.env.example`** — la lista de claves que el material espera, con valores de mentira y el
  nombre exacto de cada variable. Se copia a `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado

Salida real de `pruebas/pruebas.sh` (recortada: los avisos de origen se repiten en cada comando y
las rutas son las del contenedor):

```
== 0. escenario: historial sintético de 3 agentes ==
escenario listo: 8 ficheros en entrada/

== 2. un comando, tres formatos ==
33 prompts from claude (…/.claude/projects/… + …/.claude/history.jsonl)
8 prompts from codex (…/.codex/sessions)
6 prompts from cursor (…/.config/Cursor/User/globalStorage/state.vscdb)
1 secrets replaced with [REDACTED] (--no-redact keeps them)
2026-08-12  claude  revisa el csv de facturas de agosto y dime que filas no cuadran
2026-08-21  claude  genera el pdf de la factura 2026-101 con el logo nuevo
…
47

== 3. el secreto que estaba dentro ==
2026-10-09  claude  conecta con la api de facturacion usando [REDACTED] y prueba el envio
sk-proj-<30 caracteres de ejemplo>          <- esta es la credencial FALSA del ejemplo, en crudo
2026-10-09  claude  conecta con la api de facturacion usando sk-proj-EJEMPLO… y prueba el envio
1

== 4. contar lo que repites ==
 13  revisar el CSV de facturas
 12  generar el PDF de una factura
  8  resumen del ultimo commit
  7  correo de recordatorio
  6  clientes sin NIF
 46  peticiones clasificadas, 1 sueltas
 11  generar el PDF de una factura      <- mismo historial, --since 2026-09-01
  8  revisar el CSV de facturas
  7  correo de recordatorio
  6  resumen del ultimo commit
  4  clientes sin NIF
 36  peticiones clasificadas, 1 sueltas

== 5. los tests del repositorio (no hace falta creérselo) ==
20 tests collected in 0.27s
…test_secrets_are_redacted PASSED…
18 passed, 2 skipped
```

Los dos tests que se saltan necesitan una base de datos real de Cursor; el repositorio los salta
cuando no la encuentra en vez de fallar. La clave del ejemplo es inventada (lleva `EJEMPLO` y
`Falsa` en el nombre): sirve para ver la forma de una credencial, no es una credencial.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
Apache 2.0, la misma del repositorio original — puedes usar, modificar y distribuir este código
libremente, citando el origen. La licencia original está en `repo/LICENSE`, y `traer_repo.sh` es lo
que crea esa carpeta.
