# InvenTree: controla el stock de tus componentes con Python

> Material del vídeo **InvenTree: controla el stock de tus componentes con Python** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Un almacén de componentes que **no se actualiza a mano**: el stock es la suma de los movimientos, así
que «¿qué falta?» se responde con una consulta (GET http://127.0.0.1:8000/api/part/?low_stock=true) y
el parte de reposición sale en un CSV. En el vídeo se ve el antes y el después: 3 referencias bajo
mínimo, el técnico gasta 3 ESP32 y 60 conectores, y la misma consulta devuelve 4.

## El problema, en una frase
La cantidad de cada pieza la escribe alguien a mano cuando se acuerda, y la fecha de la última
actualización suele ser de hace semanas. Compras lo que ya tienes, paras un montaje por una pieza que
ya no está y cada persona tiene su copia de la hoja.

## Cómo está montado
Cuatro palabras, que son todo el modelo de datos:

- **Pieza** — la referencia del catálogo (`RES-10K`), con su **mínimo** de existencias.
- **Unidad de stock** — un montón concreto de esa pieza (7 ESP32 en el cajón B).
- **Ubicación** — dónde está ese montón (cajón, estante, taller).
- **Lote** — de qué compra salió ese montón.

La cantidad total **no se guarda**: es la suma de las unidades. Por eso no se queda desactualizada, y
por eso el stock no se edita: se mueve (entradas, salidas y traslados).

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`). No hay que instalar nada más: todo lo que usan los
  scripts viene en la librería estándar.

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base y crear el esquema de
la base de datos); las siguientes ejecuciones tardan segundos.

## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (los tres van en esta carpeta, no hay más):
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada.
- `pruebas/pruebas.sh` — ejecuta la demo en esa máquina y comprueba que da los números del vídeo.
  Es la prueba que pasó el material antes de publicarse.
- `.env.example` — plantilla de las variables del material. Se copia a `.env` (que **no**
  se sube nunca al repositorio).

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno (basta con `docker compose up`).

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base):
```bash
docker --context default build -t repro-inventree-stock-minimos:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-inventree-stock-minimos:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o comprobar el resultado de una vez**, dentro del mismo contenedor: `pruebas.sh` ejecuta la
demo completa y verifica que salen 3 referencias antes, 4 después y el CSV con su cabecera.
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
   cd inventree-stock-minimos
   ```
2. Prepara las variables de entorno (los valores de ejemplo ya valen para probar; nunca escribas
   claves reales dentro de un script):
   ```bash
   cp .env.example .env
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```
   La primera vez tarda 2-3 minutos: crea el esquema de la base, el usuario `admin`, el token de API
   y siembra el almacén de ejemplo. Deja dos copias de la base en `_snap/` (el estado inicial y el
   estado después del consumo) para que las siguientes ejecuciones arranquen en segundos.

Si prefieres ir paso a paso, las órdenes sueltas del vídeo funcionan igual: `bash demo.sh 4` ejecuta
solo el paso 4, y `./scripts/arrancar.sh _snap/00_inicial.sqlite3` arranca InvenTree sobre el estado
inicial (la primera vez, si esa copia no existe, la prepara solo).

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base clavada por digest y directorio de trabajo. |
| `pruebas/pruebas.sh` | Ejecuta `bash demo.sh` en limpio y comprueba los números del vídeo. |
| `.env.example` | Plantilla de las variables del material (se copia a `.env`, que nunca se sube). |
| `.gitignore` | Lo que genera la propia demo (`_snap/`, la base, el token, `salida/`): no se versiona. |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `paquete.json` | Ficha interna de producción: familia, herramienta, fecha de estreno y salida esperada. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |
| `scripts/preparar_almacen.sh` | Prepara el almacén desde cero: esquema, usuario, token, datos y copia de la base. Se lanza sola la primera vez. |
| `scripts/arrancar.sh` | Arranca InvenTree dentro del contenedor y espera a que la API conteste; restaura la copia de la base que se le pase. |
| `scripts/env.sh` | Exporta `INVENTREE_URL` y `INVENTREE_TOKEN` para los scripts (el token se lee de `.token`). |
| `scripts/estado.py` | Versión de la API, número de piezas, ubicaciones, unidades de stock y piezas contadas. |
| `scripts/revisar_stock.py` | Pide GET http://127.0.0.1:8000/api/part/?low_stock=true y pinta qué está bajo el mínimo y cuánto falta. |
| `scripts/donde.py` | Pide GET http://127.0.0.1:8000/api/stock/?part=… y muestra cada unidad con su ubicación y su lote. |
| `scripts/historial.py` | Pide GET http://127.0.0.1:8000/api/stock/track/?part=…: qué pasó con la pieza, quién y cuándo. |
| `scripts/consumo.py` | Registra una retirada de stock con POST http://127.0.0.1:8000/api/stock/remove/, con cantidad y nota. |
| `scripts/lista_compra.py` | Genera `salida/lista_compra.csv` con lo que hay que pedir de cada referencia. |
| `scripts/sembrar.py` | Carga piezas, categorías, ubicaciones y unidades por la API; es idempotente por `IPN`. |
| `scripts/_token.py` | Crea (o reutiliza) el token de API del usuario `admin` y lo guarda en `.token`. |
| `scripts/_restore.py` | Restaura la base SQLite de la demo desde una copia de `_snap/` antes de arrancar. |
| `scripts/_guardar.py` | Hace una copia consistente de la base (incluye el WAL) para poder repetir la demo. |
| `scripts/_ping.py` | Comprueba que la API responde y devuelve su versión; lo usa `arrancar.sh`. |
| `datos/hoja_stock.csv` | La hoja de cálculo de ejemplo del problema: la que el vídeo sustituye. |

`_snap/` no viene en la carpeta: lo genera la demo la primera vez. Contiene `00_inicial.sqlite3`
(almacén cargado, sin ningún consumo: el punto de partida) y `10_tras_consumo.sqlite3` (después de
gastar 3 ESP32 y 60 conectores: el estado final del vídeo). Son ficheros binarios de trabajo, por eso
no se publican.

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial
  clavada por digest (para que mañana funcione igual) y anula el `ENTRYPOINT` de esa imagen: aquí la
  aplicación no la arranca el guion de la imagen, la arranca `scripts/arrancar.sh`. Sin eso, el
  contenedor intentaba ejecutar `./init.sh` desde otro directorio y fallaba antes de empezar.
- **`pruebas/pruebas.sh`** — la prueba de verdad: ejecuta `bash demo.sh` completo y comprueba, sobre
  su salida real, que antes del consumo hay 3 referencias bajo mínimo, que después hay 4 y que el
  parte es un CSV con cabecera. Si algo no cuadra, para y dice qué no cuadró.
- **`.env.example`** — la lista de variables que el material espera, con valores de mentira y el
  nombre exacto de cada una. Se copia a `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado
Salida real de `bash demo.sh` en el entorno de pruebas (recortada a lo esencial):

```
### 1 · arrancar InvenTree con el almacén de ejemplo
InvenTree listo · API en http://127.0.0.1:8000/api/
InvenTree 1.5.7 · API v530
piezas en catálogo : 6
ubicaciones        : 5
unidades de stock  : 7
piezas contadas    : 799

### 2 · qué está por debajo del mínimo
REFERENCIA   DISPONIBLE  MÍNIMO  FALTAN  PIEZA
COND-470             38      50      12  Condensador electrolítico 470uF 16V
JST-XH4              85     100      15  Conector JST-XH de 4 pines
USB-C-1M              3       5       2  Cable USB-C de 1 metro
3 referencia(s) por debajo del mínimo

### 4 · el técnico gasta 3 ESP32 y 60 conectores
ESP32-WROOM: 3 uds consumidas
JST-XH4: 60 uds consumidas

### 5 · la misma pregunta, después del consumo
ESP32-WROOM           8      10       2  Módulo ESP32-WROOM-32
4 referencia(s) por debajo del mínimo

### 6 · el parte de reposición en CSV
--- salida/lista_compra.csv ---
referencia,pieza,disponible,minimo,pedir
COND-470,Condensador electrolítico 470uF 16V,38,50,12
ESP32-WROOM,Módulo ESP32-WROOM-32,8,10,2
JST-XH4,Conector JST-XH de 4 pines,25,100,75
USB-C-1M,Cable USB-C de 1 metro,3,5,2

RESULTADO: 3 referencias antes del consumo y 4 después; el parte está en salida/lista_compra.csv
```

Los números exactos de versión dependen de la imagen de InvenTree; el resto (3 referencias antes, 4
después, las cantidades del CSV) es lo que comprueba `pruebas/pruebas.sh`.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves. El único «token» que aparece es
el de la API del InvenTree de pruebas, que se genera solo en tu base local y no sirve fuera de ella.

## Solución de problemas
- **La primera ejecución tarda 2-3 minutos y parece colgada**: está aplicando el esquema de InvenTree
  y sembrando los datos. Es normal; las siguientes arrancan en segundos.
- **`./init.sh: No such file or directory`**: tu imagen no lleva anulado el `ENTRYPOINT` de la imagen
  oficial (lo hace `entorno/Dockerfile`). Vuelve a construir el entorno del paso 1.
- **`Address already in use` en el puerto 8000**: ya tienes un InvenTree (u otro servidor) escuchando
  ahí. Para el que tengas o cambia el puerto en `scripts/arrancar.sh` y en `.env`.
- **«InvenTree NO arrancó»**: mira las últimas líneas de `/tmp/gunicorn.log` dentro del contenedor;
  ahí está el error real de la aplicación.
- **Quieres empezar de cero otra vez**: borra `_snap/`, `database.sqlite3*` y `.token`; la próxima
  ejecución vuelve a preparar el almacén.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
