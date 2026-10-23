# python-docx: rellena contratos de Word sin dejar marcadores

> Material del vídeo **python-docx: rellena contratos de Word sin dejar marcadores** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema
Tienes una plantilla de Word y doce clientes. Así que copias el documento, cambias el nombre, el CIF y
el importe, guardas con otro nombre… doce veces. Y a la novena te dejas el nombre del cliente anterior
en un párrafo, o el importe de otro, y el contrato sale con datos que no son. Cuando llega la
reclamación ya está firmado.

Este material hace ese trabajo con un programa: lee una lista de clientes y escribe un `.docx` por
cliente desde la plantilla. Y, sobre todo, **comprueba lo que ha escrito**: si a un documento le queda
un marcador dentro o a un cliente le falta un dato, ese contrato no se emite.

## Qué vas a conseguir
Doce contratos de Word generados desde una plantilla en un solo comando, con una verificación que
relee los doce y demuestra que no queda ningún marcador y que el importe de cada uno es el suyo.

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
docker --context default build -t repro-docx-contratos-por-cliente:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" docx-demo:1 bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd docx-contratos-por-cliente
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
| `scripts/` | Los programas: crear la plantilla, listar marcadores, rellenar, verificar y medir los límites. También los dos CSV de ejemplo (datos inventados). |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `scripts/crear_plantilla.py` | Crea el `.docx` de ejemplo (un contrato con 5 marcadores, una tabla y un campo de fecha de Word). Es el punto de partida: sin plantilla no hay nada que rellenar. |
| `scripts/marcadores.py` | Lista los marcadores `{{...}}` de la plantilla buscando en párrafos **y** en celdas de tabla. Sirve para saber qué huecos hay antes de tocar nada. |
| `scripts/sustituir_xml.py` | El atajo: abrir el `.docx` como ZIP y cambiar el XML. Se incluye a propósito para demostrar que no funciona cuando Word ha partido un marcador. |
| `scripts/rellenar.py` | El camino bueno: lee el CSV y escribe un `.docx` por cliente sustituyendo sobre el texto del párrafo. Si a un cliente le falta un dato, no emite su contrato. |
| `scripts/verificar.py` | Relee los documentos generados y comprueba nombre, CIF e importe contra el CSV, que no queda ningún marcador, y que el formato es el de la plantilla. Es la prueba, no la confianza. |
| `scripts/limites.py` | Mide los límites en el momento: `.doc` antiguo, exportación a PDF, campos de Word y negritas dentro de un párrafo con marcador. |
| `scripts/clientes.csv` | Doce clientes de ejemplo (inventados) con nombre, CIF, importe, concepto y fecha. |
| `scripts/clientes_con_hueco.csv` | Los mismos doce más uno al que le falta el CIF: demuestra que el programa se detiene en vez de emitir un contrato a medias. |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `WINDOWS.md` | Cómo se ejecuta esto en Windows con PowerShell, y qué **no** está verificado (se probó en Linux/Docker). Incluye el aviso del CSV guardado desde Excel. |
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
```
VERIFICADO: 12 documentos, 0 marcadores, nombre y CIF e importe comprobados uno a uno, XML releido con unzip
```
Y el cliente al que le falta el CIF aparece como `DETENIDO: falta cif -> no se emite`: no se escribe
ningún fichero a medias.

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
