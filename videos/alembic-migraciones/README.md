# Alembic: cambia tu base de datos sin perder datos (tutorial Python)

> Material del vídeo **Alembic: cambia tu base de datos sin perder datos (tutorial Python)** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema (empieza por aquí)

Tienes una aplicación pequeña con su base de datos. Un día necesitas guardar el correo de cada
cliente: abres el fichero donde defines la tabla, añades la columna, guardas… y en tu portátil
funciona. Lo subes al servidor y **la aplicación revienta**: la base de datos del servidor no tiene
esa columna, porque esa base de datos se creó hace meses y nadie la ha tocado.

Entonces empieza la parte cara: entrar al servidor a mano, lanzar un `ALTER TABLE` copiado de un chat,
rezar para que no se lleve por delante las filas que había dentro, y repetirlo en cada máquina donde
vivas: tu portátil, el de tu compañero, el servidor de pruebas y el de producción. Cuatro bases de
datos, cuatro estados distintos, ninguna igual.

Eso es lo que se rompe aquí: no el código, **la estructura de la base de datos**. Y se rompe porque
cambia sin dejar rastro de cómo cambió, ni en qué orden, ni con qué se puede deshacer.

## Qué es Alembic

[Alembic](https://github.com/sqlalchemy/alembic) es la herramienta de migraciones del ecosistema
SQLAlchemy (Python). Una **migración** es un fichero con los dos caminos escritos: cómo se aplica el
cambio (`upgrade`) y cómo se deshace (`downgrade`). Alembic los numera, los encadena y guarda en la
propia base de datos cuál está aplicado.

- **Para qué sirve**: cambiar la estructura de la base de datos de forma repetible y reversible, en
  cualquier máquina, sin perder los datos que ya había.
- **Cómo funciona**: compara tu modelo (lo que quieres) con la base de datos (lo que hay) y escribe
  la diferencia como una migración. Después aplica las migraciones pendientes en orden.
- **Cuándo usarla**: en cuanto el esquema deja de caber en la cabeza de una persona o en cuanto hay
  más de una máquina con base de datos.
- **Ventajas**: el cambio queda versionado (se revisa en un *pull request*), es reversible, y
  cualquiera con el repositorio llega al mismo esquema con un comando.
- **Desventajas honestas**: hay que mantener el modelo y las migraciones en sincronía; la
  autodetección no adivina todo (renombrar una columna lo interpreta como borrar una y crear otra);
  y en bases grandes una migración puede tardar y bloquear la tabla.

## Qué vas a conseguir

Cambiar la estructura de una base de datos SQLite con migraciones versionadas de Alembic, sin perder
los datos que ya había dentro: verás la columna nueva aparecer y los tres clientes seguir en su sitio.

## Qué hay en esta carpeta

| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `models.py` | El modelo: la forma que queremos que tenga la tabla `clientes`. Cambiarlo **no** cambia la base de datos. |
| `seed.py` | Mete tres clientes de ejemplo. Sirve para tener datos dentro **antes** del cambio de estructura. |
| `estado.py` | Lee la base de datos real (no el modelo) y dice qué columnas tiene la tabla y cuántas filas hay. Es la prueba. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (aquí no hay ninguna). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: el problema, la herramienta, los pasos y el resultado esperado. |

### Qué hace cada script, paso a paso

- **`demo.sh`** — la lista de órdenes que se ejecutan en el vídeo, en ese orden: partir sin base de
  datos, `alembic init`, apuntar la configuración al modelo y a la base, generar la primera
  migración, aplicarla, meter datos, cambiar el modelo, generar la segunda migración (solo la
  diferencia), aplicarla **con datos dentro**, ver el historial, deshacer y rehacer. Si el vídeo hace
  algo que no está aquí, el material está mal.
- **`models.py`** — declara la tabla `clientes` con SQLAlchemy. Es el destino: lo que queremos que
  sea la base de datos. Alembic lee este fichero para saber qué falta.
- **`seed.py`** — inserta tres filas de ejemplo con la aplicación (no con SQL a mano). Su papel en el
  vídeo es concreto: cuando llegue la segunda migración, esos tres clientes tienen que seguir ahí.
- **`estado.py`** — abre la base de datos y pregunta por sus columnas y sus filas. Es la evidencia:
  no dice lo que el modelo promete, dice lo que la base tiene.
- **`entorno/Dockerfile`** — construye la máquina de pruebas desde una imagen oficial con la versión
  fijada (nada de `latest`) y las dependencias fijadas. No copia claves ni datos personales.
- **`pruebas/pruebas.sh`** — la prueba de verdad: comprueba que Docker responde, construye la imagen,
  copia la carpeta a un directorio temporal dentro del contenedor y ejecuta ahí la demo con la
  carpeta original montada en solo lectura, y compara la salida con la esperada.
- **`.env.example`** — la lista de claves que el material espera. Aquí no hay ninguna: este material
  no pide credenciales.

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
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en
`entorno/Dockerfile` y se construye con una orden.

**Paso 1 — construir la máquina** (una sola vez):
```bash
docker build -t repro-alembic-migraciones:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script trabaja sobre una copia en `/tmp`):
```bash
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$PWD:/trabajo:ro" repro-alembic-migraciones:local \
  bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros:
```bash
bash pruebas/pruebas.sh
```

## Pasos

1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd alembic-migraciones
   ```
2. Ejecuta la demo (dentro del contenedor del paso 2 del entorno, o en tu máquina con
   `pip install alembic sqlalchemy`):
   ```bash
   bash demo.sh
   ```
3. Mira el resultado con:
   ```bash
   python3 estado.py
   ```

Si prefieres hacerlo en tu máquina, sin contenedor: `pip install alembic sqlalchemy` y `bash demo.sh`
desde esta carpeta. El resultado es el mismo.

## Resultado esperado

Al final, la base de datos tiene la columna nueva y los mismos clientes que antes:

```
Columnas de clientes: id, nombre, ciudad, email
Filas: 3
   (1, 'Panadería Luna', 'Sevilla', None)
   (2, 'Taller Norte', 'Bilbao', None)
   (3, 'Óptica Mar', 'Alicante', None)
```

Y `alembic current` muestra la versión aplicada, para que puedas comprobar en cualquier máquina en
qué punto está.

## Límites de lo que demuestra este material

- Se prueba con **SQLite**. El flujo es el mismo en PostgreSQL o MySQL, pero ahí una migración puede
  bloquear la tabla mientras corre: eso este material **no** lo demuestra.
- La autodetección compara modelo y base; **no** adivina renombrados (los interpreta como borrar y
  crear). Ese caso hay que escribirlo a mano.
- Las migraciones de **datos** (rellenar la columna nueva con lo que había) son otro paso, que este
  material menciona pero no ejecuta.

## Coste y credenciales

Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas

- **«command not found: alembic»**: estás fuera del contenedor o sin `pip install alembic sqlalchemy`.
- **`alembic revision --autogenerate` genera una migración vacía**: casi siempre es que
  `target_metadata` en `migrations/env.py` no apunta a tu modelo.
- **Falla la descarga de la imagen**: comprueba tu conexión; si usas una red corporativa, puede
  bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia

MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
