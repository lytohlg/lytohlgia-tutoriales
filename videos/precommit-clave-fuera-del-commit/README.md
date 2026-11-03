# pre-commit: tu clave privada se para antes del commit

> Material del vídeo **pre-commit: tu clave privada se para antes del commit** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Tienes una clave dentro de un fichero del proyecto: la del servidor, la del correo, la del banco de
pruebas. Un día haces `git commit` con prisa, la subes, y no pasa nada visible. El problema llega
meses después: esa clave ya está en el historial, y borrarla del presente no la borra del pasado.
Rotar la clave cuesta una tarde; si el repositorio es público, cuesta una tarde y un susto.

Hoy lo resuelves de tres maneras, y las tres fallan alguna vez:

- **Con cuidado**: revisas `git status` antes de cada commit. Funciona hasta el día que tienes prisa.
- **A mano, al final**: buscas secretos cuando ya están dentro. Entonces ya es tarde: hay que rotar.
- **Con una nota en el README**: «no subas claves». Nadie lee las notas, y menos un viernes.

El coste no es el rato de configurarlo: es el commit que ya existía cuando te diste cuenta, y las
horas de rotar todo lo que esa clave abría.

## Qué vas a conseguir

Un control que corre **antes** de que el commit exista: si el trabajo lleva una clave dentro, git no
guarda nada. Y no solo eso: el control te dice **qué fichero** y **en qué línea**, arregla lo que se
puede arreglar solo (espacios al final, YAML roto, ficheros demasiado grandes), admite reglas
propias de tu proyecto en veinte líneas, y tiene un agujero conocido —se salta con `--no-verify`—
que este material también te enseña, porque esconderlo sería mentirte.

## Requisitos

**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base y los controles).


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
descarga la imagen base y los controles):
```bash
docker --context default build -t repro-precommit-clave-fuera-del-commit:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-precommit-clave-fuera-del-commit:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
contenedor no dependa de nada de fuera. Los controles (`pre-commit-hooks` v6.0.0 y `detect-secrets`
v1.5.0) ya vienen descargados dentro de la imagen, en `/opt/pc-cache`: la demo no necesita red ni
esperar a GitHub. Este material no pide credenciales de nadie.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd precommit-clave-fuera-del-commit
   ```
2. Ejecuta la demo (dentro del contenedor del paso 2, o en tu máquina si ya tienes git y
   `pip install pre-commit==4.7.0`):
   ```bash
   bash demo.sh
   ```
3. Para usarlo en un proyecto tuyo, copia `scripts/pre-commit-config.yaml` a la raíz como
   `.pre-commit-config.yaml`, ejecuta `pre-commit install` y sigue con tu trabajo normal. La
   primera vez que hagas `git commit` verás los controles en marcha.

No hace falta `.env`: el fichero de entorno que aparece en el vídeo lo crea la propia demo, con
valores de mentira, y lo borra al final del arreglo.

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
  Va **sin** `set -e` a propósito: varias órdenes tienen que fallar, y ese fallo es el producto.
- **`scripts/app.py`** — el código «normal» del escenario: un generador de informe de ventas que lee
  un CSV. No tiene nada que ver con secretos; está ahí para que el repositorio se parezca a uno tuyo.
- **`scripts/comprobar_regla.py`** — el hook propio del hito 4, veinte líneas. Recibe los ficheros
  que le pasa pre-commit, busca la palabra `PENDIENTE` línea a línea y termina con código de error
  si la encuentra: eso es lo que para el commit. Es el ejemplo de que el mecanismo es tuyo, no solo
  de los controles oficiales.
- **`scripts/pre-commit-config.yaml`** — el fichero de configuración completo que se ve en el vídeo:
  cinco controles de `pre-commit-hooks` v6.0.0 (espacios, fin de fichero, YAML, tamaño máximo,
  claves privadas) y `detect-secrets` v1.5.0.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial
  con la versión fijada (nada de `latest`, para que mañana funcione igual), instala `git`, `openssl`
  y `pre-commit==4.7.0`, y deja los controles descargados en `/opt/pc-cache`. No copia claves ni tus
  datos.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en cuatro pasos: (1) comprueba que Docker
  responde; (2) construye la imagen de `entorno/Dockerfile`; (3) copia la carpeta a un directorio
  temporal dentro del contenedor y ejecuta ahí la demo, con la carpeta original montada en solo
  lectura; (4) compara la salida con la esperada y te dice si cuadra. Si algo falla, para y te dice
  en qué paso. No escribe nada fuera del contenedor.
- **`.env.example`** — la lista de claves que el material esperaría, con valores de mentira y el
  nombre exacto de cada variable. Se copia a `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado
VERIFICADO: dos controles paran el commit · la clave no entra · el YAML y el binario se arreglan · hook propio de 20 líneas · --no-verify lo salta

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves. La clave que aparece en el
vídeo es **desechable** y la genera `openssl` dentro del contenedor en cada ejecución; no existe
ninguna clave real en este repositorio.

## Lo que este material NO demuestra
Que nadie pueda saltarse el control en su propio ordenador. `pre-commit` se ejecuta en tu máquina,
así que `git commit --no-verify` lo salta — y el vídeo lo enseña, con el commit y la clave dentro
del historial. La barrera que no se puede saltar no es esta: vive en el servidor, en la integración
continua, y se monta aparte.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- **`detect-secrets` no marca tu fichero**: solo marca lo que parece un secreto (claves, tokens,
  contraseñas asignadas). Un texto que «lo parece» pero no lo es, no lo detecta — y eso es correcto.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
