# invoice2data: extrae datos de facturas PDF a CSV con Python (instalado y probado)

> Material del vídeo **invoice2data: extrae datos de facturas PDF a CSV con Python (instalado y probado)** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Convertir una carpeta de facturas PDF en una tabla CSV, con una plantilla YAML que tú escribes, y
ver con tus ojos qué pasa cuando el formato es nuevo.

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
- `.env.example` — plantilla de las variables del material. Se copia a `.env` (que **no** se sube
  nunca al repositorio). Este material no usa claves: ahí solo hay rutas.

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno (basta con `docker compose up`).

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base):
```bash
docker --context default build -t repro-invoice2data-facturas:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-invoice2data-facturas:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd invoice2data-facturas
   ```
2. Prepara tus variables de entorno (aquí son solo rutas, pero el hábito es el mismo):
   ```bash
   cp .env.example .env
   # edita .env con tu editor si quieres cambiar dónde busca y dónde escribe
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `hacer_facturas.py` | Escribe las cuatro facturas PDF ficticias que se leen en la demo (no hay que descargar nada). |
| `plantillas/arenal.yml` | La plantilla del primer formato: dónde cortar cada campo del PDF, proveedor por proveedor. |
| `plantillas_corregidas/vega.yml` | La plantilla del proveedor nuevo, ya corregida a mano, lista para copiarla a `plantillas/`. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las variables del material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
  Se puede ejecutar entero (`bash demo.sh`) o por pasos (`bash demo.sh 2 5`).
- **`hacer_facturas.py`** — escribe a mano cuatro PDF 1.4 sin usar ninguna librería. Tres son del
  mismo proveedor con importes distintos y la cuarta es de otro proveedor con otra maqueta: así se
  ve que la plantilla es por formato, no por herramienta. Los datos son inventados. Lo único que
  cambia respecto al vídeo es la línea de contacto de las tres facturas del primer proveedor
  (teléfono y web de mentira, en lugar de un correo ficticio): los importes, fechas, números y el
  resto del texto son los mismos, y la extracción sale idéntica; la cuarta factura es byte a byte la
  misma que se leyó en el vídeo.
- **`plantillas/arenal.yml`** — la plantilla YAML del primer formato: unas palabras clave para
  reconocer al proveedor y una expresión regular por campo (fecha, número, importe, base, IVA).
- **`plantillas_corregidas/vega.yml`** — la plantilla del segundo formato, corregida después de leer
  el borrador que escribe la propia herramienta. El `demo.sh` la copia a `plantillas/` para que la
  pasada final la use.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial
  con la versión fijada (nada de `latest`, para que mañana funcione igual), instala lo que el
  material necesita y deja el directorio de trabajo preparado. No copia claves ni tus datos: eso
  entra después, por variables de entorno y solo si tú las pones.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en cuatro pasos: (1) comprueba que Docker
  responde; (2) construye la imagen de `entorno/Dockerfile`; (3) copia la carpeta a un directorio
  temporal dentro del contenedor y ejecuta ahí la demo, con la carpeta original montada en solo
  lectura; (4) compara la salida con la esperada y te dice si cuadra. Si algo falla, para y te dice
  en qué paso. No escribe nada fuera del contenedor.
- **`.env.example`** — la lista de variables que el material espera, con valores de mentira y el
  nombre exacto de cada una. Aquí no hay claves: invoice2data lee ficheros locales. Se copia a
  `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado
El paso 1 imprime la tabla con las tres facturas del primer proveedor; dentro tiene que aparecer el
número **F-2026-0417** con su fecha, su base, su IVA y su total (1.512,50 EUR, que es el importe que
el vídeo comprueba a mano para descartar una lectura torcida). El paso 2 tiene que salir con un
error de «no hay plantilla para este PDF» y un `[]` en el JSON: eso es lo correcto, no una avería.
El paso 5 vuelve a leer las cuatro con la plantilla nueva y deja la bandeja de entrada vacía.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- **El paso 2 sale con error**: es lo esperado con un proveedor desconocido; el error dice que no
  hay plantilla y el JSON queda vacío. Si además quieres la tabla, sigue con los pasos 3 y 4.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
