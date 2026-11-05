# Airflow: un informe de ventas en cuatro pasos, sin que el ultimo corra con datos a medias

> Material del vídeo **Airflow: un informe de ventas en cuatro pasos, sin que el ultimo corra con datos a medias** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema
Un informe de ventas que se ejecuta solo a las seis de la mañana: tres o cuatro scripts encadenados
con `cron`. Un día el segundo script se encuentra una fila rota y falla; el tercero arranca igual, con
la mitad de los datos, y escribe un informe que parece bueno. Te enteras el lunes. Y no queda rastro:
el log está en un fichero que nadie abrió y no hay forma de saber en qué paso se rompió.

Este material es la versión orquestada de ese mismo informe: cuatro pasos con dependencias reales,
reintentos declarados y, sobre todo, un paso que **no se ejecuta** si el anterior falló. La demo que
acompaña al vídeo lo reproduce en un contenedor limpio, con un fichero de datos bueno y otro roto a
propósito.

## Qué vas a conseguir
Encadenar cuatro pasos de un informe (extraer, limpiar, totales, guardar) con dependencias reales, reintentos y contencion del fallo.

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
docker --context default build -t repro-airflow-informe-ventas:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-airflow-informe-ventas:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd airflow-informe-ventas
   ```
2. Prepara tus variables de entorno (nunca escribas claves dentro de un script):
   ```bash
   cp .env.example .env
   # edita .env con tu editor y rellena los valores
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `dags/informe_clientes.py` | El flujo: cuatro tareas (`extraer`, `limpiar`, `totales`, `guardar`) y las dependencias entre ellas, en una sola función de Python. |
| `entrada/ventas.csv` | Los datos buenos: 8 filas de ventas y 4 clientes. |
| `entrada/ventas_roto.csv` | Los mismos datos con una devolución sin marcar (`-45.25`): es el fichero que hace fallar el paso `limpiar`. |
| `scripts/ver.sh` | Ejecuta el flujo con `airflow dags test` y deja solo las líneas útiles del log, sin sellos de tiempo. |
| `scripts/estado.sh` | Tabla corta tarea → estado de una ejecución (`airflow tasks states-for-dag-run`). |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `paquete.json` | El manifiesto del paquete: slug, imagen, comando, fecha de estreno y salida esperada. |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de la imagen oficial de
  Airflow con la versión fijada (`2.10.5`, nada de `latest`, para que mañana funcione igual),
  quita el entrypoint que exige ejecutar como root, y deja el usuario sin privilegios y el
  directorio de trabajo preparados. No copia claves ni tus datos: eso entra después, por
  variables de entorno y solo si tú las pones.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en cuatro pasos: (1) comprueba que Docker
  responde; (2) construye la imagen de `entorno/Dockerfile`; (3) copia la carpeta a un directorio
  temporal dentro del contenedor y ejecuta ahí la demo, con la carpeta original montada en solo
  lectura; (4) compara la salida con la esperada y te dice si cuadra. Si algo falla, para y te dice
  en qué paso. No escribe nada fuera del contenedor.
- **`.env.example`** — la lista de claves que el material espera, con valores de mentira y el
  nombre exacto de cada variable. Se copia a `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado
Salida real de `bash demo.sh` en un contenedor limpio (resumida; los pasos 0 y 1 tardan unos segundos
porque crean la base de datos de estados):

```
-- 0. Base de datos de estados (la crea 'airflow db migrate') --
base de datos lista: /tmp/airflow/airflow.db
flujos registrados en la base de datos

-- 1. La herramienta y el flujo que ve --
2.10.5
dag_id           | fileloc                             | owners  | is_paused
informe_clientes | /tmp/repro/dags/informe_clientes.py | airflow | True

-- 2. Que pasos ha entendido --
extraer
guardar
limpiar
totales

-- 4. Ejecucion real, dia 1: todo en orden --
leidas 8 filas de ventas.csv
limpias 8 de 8 filas
clientes con ventas: 4
informe escrito: /tmp/repro/salida/informe.csv

-- 5. La salida --
cliente,total
ACME,2110.50
Beta SL,1025.25
Cortes,2310.00
Delta,1040.75

-- 6. El historial de ejecuciones --
run_id state
manual__2026-11-01T00:00:00+00:00 success

-- 7. Dia 2: el fichero llega con una devolucion sin marcar --
leidas 8 filas de ventas.csv
ValueError: importe no valido en Beta SL: -45.25
(el flujo ha fallado, como debia)

-- 8. Contencion: los pasos de abajo no se lanzan --
extraer   success
limpiar   failed
totales   upstream_failed
guardar   upstream_failed
el informe del dia 1 sigue intacto: el dia 2 no escribio ninguno
```

Lo importante de esa salida: en el paso 8 los dos últimos pasos no aparecen como «failed» sino como
`upstream_failed`, que en Airflow significa **no se han llegado a ejecutar porque el anterior falló**.
Y el informe del día 1 sigue con su contenido: el día roto no escribió uno nuevo.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
