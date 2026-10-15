# restic: restaurar y comparar para saber si tu copia sirve

> Material del vídeo **restic: restaurar y comparar para saber si tu copia sirve** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Comprobar que una copia de seguridad sirve: montarla con restic, romper los datos a propósito,
restaurar y comparar fichero a fichero por sha256 hasta obtener un veredicto OK o FALLO.

Al terminar tendrás, funcionando en tu máquina:
- un repositorio de restic con **80 ficheros de ejemplo (12 contratos)** generados de forma determinista;
- la **huella sha256 de los contratos tomada ANTES** de tocar nada, para poder comparar después;
- una **restauración real** de la copia, comparada fichero a fichero (no un «parece que está»);
- un **verificador** (`scripts/verificar_copia.py`) que decide OK o FALLO y escribe un informe JSON;
- el **envoltorio semanal** (`scripts/verificar_copia_semanal.sh`) con su código de salida para el cron.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).
- `restic` **0.19.1** solo si NO usas el contenedor: el entorno de pruebas lo instala ya, fijado por
  versión y comprobado por sha256 (`f4154156…585c`) antes de usarlo. En tu máquina, la instalación es
  la del vídeo: binario oficial + `sha256sum -c SHA256SUMS`.

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
docker --context default build -t repro-restic-verificar-copia:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-restic-verificar-copia:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd restic-verificar-copia
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
| `scripts/crear_datos.py` | Crea los 80 ficheros de ejemplo (12 contratos) de forma determinista (semilla fija). |
| `scripts/verificar_copia.py` | El verificador: restaura la última copia, compara por sha256 y devuelve 0 (OK) o 1 (FALLO). |
| `scripts/verificar_copia_semanal.sh` | El envoltorio que se pone en cron o systemd: deja el informe del día en `trabajo/informes/`. |
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
La demo termina con el veredicto escrito por el propio script, y con el código de salida en la mano:

```
ficheros        : 81 en los datos, 80 en la copia
identicos       : 80
distintos       : 0
faltan en copia : 1
resultado       : FALLO  (0.4 s)
...
VERIFICACION FINAL: OK (detecta la copia incompleta y restaura identica)
```

Ese es el punto del vídeo: el verificador **se niega** a dar por buena una copia a la que le falta un
fichero (sale `FALLO` y termina con código 1), y solo dice `OK` cuando la copia vuelve a estar completa.
En el camino, la restauración se compara con la huella sha256 tomada antes del desastre: los 12
contratos salen idénticos uno a uno. El informe queda en `trabajo/informe_verificacion.json`.

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

El programa que se instala y se usa aquí (restic, https://github.com/restic/restic) no es nuestro: es
software libre con licencia **BSD-2-Clause**, y se descarga del binario oficial de su release
(v0.19.1, comprobado por sha256 antes de instalarlo).
