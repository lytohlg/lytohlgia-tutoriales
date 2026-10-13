# Avisos de stock bajo con Python: inventario real en Docker

> Material del vídeo **Avisos de stock bajo con Python: inventario real en Docker** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Montar un almacén de verdad (el proyecto *Simple Stock Management*, un ERP de inventario en Django)
dentro de Docker, cargarle tu stock y ejecutar un vigilante en Python que consulta su API y **avisa
solo de los artículos que han bajado del mínimo**, sin repetir el mismo aviso dos veces y detectando
cuándo se repone. Al terminar sabrás consultar esa API, entender por qué el aviso no se duplica y
cómo adaptarlo a tu caso.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`). Todo lo demás se instala dentro del contenedor.

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base y el proyecto).


## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (van en esta carpeta, junto al resto del material):
- `entorno/Dockerfile` — describe la máquina: imagen base `python:3.13-slim` y dependencias con la
  versión fijada. Descarga el proyecto de inventario (versión fijada por commit) dentro de la imagen.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de las claves que necesita el material. Se copia a `.env` (que **no**
  se sube nunca al repositorio).

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno (basta con `docker compose up`).

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base y el proyecto):
```bash
docker --context default build -t repro-stock-ssm:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-stock-ssm:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd stock-ssm
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

La demo va por pasos numerados y puedes ejecutar solo uno (útil para ir viendo qué pasa):
`bash demo.sh 1`, `bash demo.sh 2`... El estado (base de datos, servicio web) se conserva entre pasos
mientras estés dentro del mismo contenedor.

1. **La base de datos del almacén** — se crea el esquema del proyecto (SQLite dentro de la carpeta).
2. **Usuarios y permisos** — dos usuarios de demostración con los permisos que trae el proyecto
   (almacén y tienda).
3. **El stock que ya tienes** — se carga `entrada/stock.csv` en la base de datos.
4. **La API del almacén** — se levanta el servidor y se consulta la API con y sin sesión: sin sesión
   no da nada, con sesión devuelve los artículos paginados.
5. **Baja de stock** — la tienda pide unidades y el almacén las descuenta (es la operación real del
   proyecto, no un `UPDATE` a mano).
6. **El aviso** — el vigilante consulta la API y avisa de los artículos por debajo del mínimo.
7. **Repetir y reponer** — se ejecuta otra vez (no repite avisos) y luego se repone stock (el artículo
   sale de la lista de pendientes).
8. **Si el almacén no contesta** — se apunta a un puerto donde no hay nada y el vigilante falla
   **gritando el error**, con código de salida distinto de cero, en vez de callarse.

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `entrada/stock.csv` | El stock de ejemplo: 12 artículos con su SKU, descripción, precio y unidades. |
| `scripts/alta_inicial.py` | Crea los dos usuarios de demostración y sus permisos (se puede repetir sin duplicar). |
| `scripts/avisos_stock.py` | **El vigilante**: consulta la API y avisa de lo que baja del mínimo. |
| `scripts/control_stock.py` | Comprobación por dentro (ORM del proyecto): cuántos artículos y unidades hay. |
| `scripts/lista_corta.py` | Lista corta leída del JSON de la API, para ver la misma verdad por fuera. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
- **`entorno/Dockerfile`** — construye la máquina de pruebas: parte de `python:3.13-slim` (versión
  fijada, nada de `latest`), instala `curl` y descarga el proyecto de inventario **clavado en un
  commit** con sus dependencias fijadas. No copia claves ni tus datos: eso entra después, por
  variables de entorno y solo si tú las pones.
- **`entrada/stock.csv`** — el stock de ejemplo, con la cabecera que espera el vigilante
  (`sku`, `desc`, `unit_price`, `units_total`). Cámbialo por el tuyo y el resto funciona igual.
- **`scripts/alta_inicial.py`** — crea los grupos que el proyecto usa para los permisos y los dos
  usuarios de demostración. Es idempotente: si ya existen, los deja como están.
- **`scripts/avisos_stock.py`** — **el script del vídeo**. Lee la configuración de variables de
  entorno, pide la lista de artículos a la API, compara las unidades con el mínimo y avisa. Guarda
  en `salida/avisos_estado.json` a quién avisó ya, para no repetir el mismo aviso en cada pasada.
  Devuelve 0 si todo fue bien, 2 si la configuración está mal y 3 si no pudo hablar con el almacén.
- **`scripts/control_stock.py`** — mira la base de datos por dentro (ORM del proyecto) y cuenta
  artículos y unidades: sirve para comprobar que lo que dice la API es lo que hay de verdad.
- **`scripts/lista_corta.py`** — lee el mismo JSON de la API y lo imprime en una línea por artículo;
  es el control de que el vigilante y tú estáis mirando lo mismo.
- **`.env.example`** — la lista de claves que el material espera, con valores de mentira y el
  nombre exacto de cada variable. Se copia a `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado
Ejecutando `bash demo.sh` completo, el paso 6 imprime los avisos y el 7 los cierra:

```
### 6. El aviso
AVISO  ALM-1010  Galletas maria 800g          8 unidades (minimo 10)
AVISO  ALM-1004  Arroz redondo 1kg            6 unidades (minimo 10)
2 avisos nuevos · 0 repuestos · 10 articulos por encima del minimo · 2 pendientes de reponer

### 7. Repetir sin cambios y reponer
0 avisos nuevos · 0 repuestos · 10 articulos por encima del minimo · 2 pendientes de reponer
REPUESTO  ALM-1010  Galletas maria 800g        25 unidades (ya no se avisa)
0 avisos nuevos · 1 repuestos · 11 articulos por encima del minimo · 1 pendientes de reponer
```

La palabra que comprueba la prueba automática es **AVISO**.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves de ningún servicio. Los dos
usuarios de demostración y sus contraseñas de mentira están en `.env.example` y viven **solo dentro
del contenedor**; no hay ninguna cuenta real, ni correo, ni API de pago.

## Qué demuestra este material (y qué no)
- **Sí demuestra**: que el almacén se levanta y responde, que la carga de stock entra de verdad, que
  una bajada de stock hecha por la tienda se refleja, y que el vigilante avisa una sola vez por
  artículo, deja de avisar cuando se repone y no se calla si la API no contesta. Todo con la salida
  real de la terminal.
- **No demuestra** el envío de correo del proyecto (esa parte viene configurada como «no enviar» en
  `.env.example`: aquí el aviso se imprime en pantalla y se guarda en un fichero). El proyecto
  original trae su propio comando de importación desde Excel; aquí el stock de ejemplo se carga
  desde CSV con un script propio para que la demo no dependa de un fichero binario.
- El proyecto que se monta es software de terceros: *Simple Stock Management* (licencia GPL-3.0),
  descargado por el `entorno/Dockerfile` desde su repositorio público en la versión fijada. Lo que
  aporta este material es la automatización de avisos (`scripts/avisos_stock.py`), no el ERP.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- **El paso 4 dice «unauthorized»**: el servicio aún está arrancando; espera unos segundos y repite
  el paso (la demo espera sola hasta 10 segundos, pero en un equipo lento puede quedarse corta).
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio. El proyecto de inventario que se descarga dentro del contenedor tiene su propia licencia
(GPL-3.0) y se usa tal cual, sin modificarlo.
