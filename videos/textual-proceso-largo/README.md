# Textual: ve qué falla en un proceso largo sin leer 240 líneas

> Material del vídeo **Textual: ve qué falla en un proceso largo sin leer 240 líneas** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Tienes una carpeta con cientos de ficheros que hay que procesar: extractos de facturación, PDF de
proveedores, lo que sea. Le pones un `print()` por fichero, lo lanzas y vuelves media hora después a
mirar la terminal.

Y ahí está el problema: **la pantalla tiene 240 líneas y no hay forma de saber, de un vistazo, qué ha
fallado**. Tienes que subir con la rueda buscando la palabra «error» entre mensajes que ya no
importan. Cuando el proceso termina, la información que te importaba se ha ido con el scroll.

## Qué vas a conseguir

Ver el estado de un proceso largo —cuántos van, cuántos fallan y **cuáles**— en una sola pantalla que
se redibuja sola, sin renunciar a la verdad de lo que está pasando: cada línea que ves es un fichero
que se ha procesado de verdad, y los fallos que aparecen son los fallos reales, con el dato exacto que
no se pudo leer.

La herramienta es [Textual](https://github.com/Textualize/textual), una librería de Python para hacer
interfaces de terminal. Aquí se usa para una sola cosa: una tabla que crece, una barra de progreso y
una lista de fallos que no se mueve de su sitio.

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
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada
  (Textual 8.2.8).
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de las claves que necesite el material. Este no necesita ninguna.

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno (basta con `docker compose up`).

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base):
```bash
docker --context default build -t repro-textual-proceso-largo:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-textual-proceso-largo:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno.

**Detalles de nuestra ejecución, por si tu caso es distinto:** el `--context default` fuerza el motor
Docker local — útil si tienes configurado además uno remoto; si en tu equipo solo hay uno, déjalo
igual (funciona) o quítalo. Ejecutamos con el usuario `1000:1000` para no correr como root y con
`HOME=/tmp` para que el contenedor no dependa de nada de fuera.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd textual-proceso-largo
   ```
2. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```
3. Para verlo en tu propia terminal, sin contenedor y con el ratón funcionando:
   ```bash
   pip install textual==8.2.8
   python generar_lote.py 240
   python panel.py
   ```

## La pantalla, si la quieres en tu terminal

`panel.py` es lo que se ve en el vídeo. Necesita una terminal de verdad: si lo lanzas con la salida
redirigida a un fichero (`python panel.py > out.txt`) Textual no arranca, porque no hay pantalla que
redibujar. En los contenedores de arriba se ejecuta con `script -qec "..." /dev/null`, que le da una
terminal prestada; es lo que hace `demo.sh` para que puedas verla sin abrir una ventana.

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `generar_lote.py` | Crea los 240 extractos de prueba y rompe a propósito el importe de tres de ellos. |
| `procesar.py` | Convierte un CSV en JSON. Valida el importe con `float()` **sin limpiar comas**, a propósito: un dato mal escrito tiene que verse, no arreglarse solo. |
| `lote_print.py` | La versión de siempre: recorre la carpeta y escribe una línea por fichero. |
| `panel.py` | La versión con Textual: tabla que crece, barra de progreso y lista de fallos que no se mueve. |
| `uno.py` | Procesa un solo fichero y deja salir el error completo, para ver qué pasa con el roto. |
| `comprobar.py` | Verifica que la demo dejó lo que promete (240 ficheros, 238 JSON, el importe corregido). |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo, en
  ese orden. Si el vídeo hace algo que no está aquí, el material está mal.
- **`generar_lote.py`** — con una semilla fija, para que tus 240 ficheros salgan iguales que los del
  vídeo. Tres de ellos llevan el importe escrito a la española (`842,90 EUR`) y los demás no.
- **`procesar.py`** — lee el CSV, suma la columna `importe`, cuenta filas y escribe un JSON. Si un
  importe no se puede convertir a número, lanza un error con la fila y el valor: no lo ignora.
- **`panel.py`** — un `App` de Textual con cuatro zonas (cabecera, tabla, fallos, pie). Cada fichero
  procesado añade su fila y actualiza la barra; si falla, se apunta en la lista de la derecha. El
  bloque que captura el error está dentro del bucle: un fichero roto se apunta y el proceso sigue.
- **`pruebas/pruebas.sh`** — construye la imagen de `entorno/Dockerfile`, copia la carpeta a `/tmp`
  dentro del contenedor, ejecuta `demo.sh` con el original montado en solo lectura y comprueba el
  resultado. Si algo falla, para y dice en qué paso. No escribe nada fuera del contenedor.

## Resultado esperado

Al final de la demo:
```
VERIFICADO: 240 ficheros generados · 238 JSON · 2 fallos a la vista
```
Antes de corregir el dato: 237 JSON y 3 fallos. Después de corregirlo: 238 JSON y 2 fallos
(`extracto_118.csv` y `extracto_203.csv` siguen rotos, y por eso no dejan JSON).

## Lo que esto no demuestra

- **No es más rápido.** La pantalla no acelera el proceso: los 240 ficheros tardan lo mismo. Lo que
  cambia es lo que ves mientras ocurre.
- **No hay concurrencia.** El proceso es secuencial y `panel.py` no usa hilos ni procesos: si el
  fichero tarda, la pantalla espera.
- **No hay reintentos.** Un fichero roto se apunta y se sigue; no se vuelve a intentar solo.
- **No hay persistencia del estado.** Si cierras la pantalla, el estado se va con ella; lo que queda
  son los JSON de `salida/`.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **El panel no arranca y dice que no hay terminal**: estás redirigiendo la salida. Lánzalo en una
  terminal normal, o con `script -qec "python panel.py" /dev/null`.
- **La tabla sale cortada**: la pantalla es pequeña. `COLUMNS=100 LINES=32 python panel.py` o agranda
  la ventana.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
