# Automatiza 300 fotos de producto con Pillow en minutos

> Material del vídeo **Automatiza 300 fotos de producto con Pillow en minutos** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
### El problema (empieza por aquí)

Llega la carpeta del proveedor con **300 fotos**. Cada una de un tamaño, cada una con el nombre que le
apetece, algunas guardadas de lado y dos que no abren. Para subirlas a la tienda hay que abrirlas,
recortarlas, pegarles el logo y guardarlas **una por una**: una tarde entera, y siempre se cuela una
sin logo o con el nombre repetido.

**Pillow** es la librería de imágenes de Python (`python-pillow/Pillow`, licencia MIT-CMU). No es un
programa con botones: es código que abres desde tu script, así que hace lo mismo con 3 fotos que con
3.000, y deja un registro de lo que hizo con cada una.

Al terminar tendrás: una carpeta con las **298 fotos utilizables iguales** (1200x1200, con marca de
agua, JPEG ligero), un `registro.csv` con **qué entró, qué salió y por qué falló** lo que falló, y un
script que vuelve a hacerlo en 25 segundos la próxima vez que llegue mercancía.

## A quién le duele
A quien publica fotos de producto o de catálogo y repite ese trabajo **cada vez que llega mercancía**.
No es un problema de diseño: es trabajo repetitivo que se paga en horas y en errores.

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
docker --context default build -t repro-pillow-300-fotos-iguales:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-pillow-300-fotos-iguales:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd pillow-300-fotos-iguales
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
  nombre exacto de cada variable. Se copia a `.env`. Este material no necesita ninguna.
- **`lote.py`** — el script que se enseña. Recorre la carpeta de entrada y con cada foto: lee el
  giro que pide el EXIF (`ImageOps.exif_transpose`), aplana la transparencia sobre blanco, la
  recorta a 1200x1200 sin deformarla (`ImageOps.fit`), le pega `datos/marca.png` con máscara, la
  guarda en JPEG calidad 82 y apunta una fila en `registro.csv`. Si una foto no se puede abrir,
  anota `DANADA` + el tipo de error y **sigue con la siguiente**. Con `--sin-giro` desactiva solo
  el giro EXIF, para poder comparar los dos resultados.
- **`lote_ingenuo.py`** — la versión de cinco minutos: abrir, `resize` a cuadrado y guardar, sin
  red de errores. Es la que se rompe en la cuarta foto (`cannot write mode RGBA as JPEG`); está
  aquí para que el fallo se pueda reproducir, no para usarla.
- **`medir.py`** — radiografía de la carpeta de entrada: cuántos ficheros, cuánto pesan, cuántos
  tamaños distintos, qué formatos, cuántas traen etiqueta EXIF de giro y cuántas están ilegibles.
  Se ejecuta antes de escribir código: es el mapa del problema.
- **`comprobar.py`** — la prueba numérica de la salida, sin mirar las fotos a ojo: que todas midan
  lo mismo, que se reabran y se decodifiquen enteras, y en qué borde quedó la franja marcada de
  cada foto (con el giro bien aplicado, arriba; sin él, a la izquierda en las giradas).
- **`verificar_marca.py`** — prueba A/B de la marca de agua: procesa la misma foto dos veces, con
  marca y sin marca, resta las dos imágenes con `ImageChops.difference` y exige que **todos** los
  píxeles cambiados caigan dentro del rectángulo donde se pegó la marca.
- **`calidad.py`** — mide el compromiso del JPEG sobre una foto: la guarda a calidad 70, 82 y 95 y
  muestra cuánto ocupa cada versión y cuánto se separa de la imagen sin comprimir.
- **`datos/generar_fotos.py`** — genera las 300 fotos del proveedor con semilla fija (`SEED = 7`):
  18 tamaños, varios formatos, nombres feos, 41 con etiqueta EXIF de giro, 20 con transparencia y
  2 truncadas a propósito. No hace falta ningún fichero externo.
- **`datos/marca.py`** — dibuja la marca de agua (`datos/marca.png`) con transparencia: placa
  blanca redondeada y bloques de color. Sin imágenes externas ni recursos privados.

## Resultado esperado
Salida real del lote completo dentro del contenedor (`bash demo.sh`, recortada a lo esencial):

```
300 fotos leídas · 298 escritas en salida/ · 2 dañadas (ver registro.csv)
41 giradas por EXIF corregidas · 20 con transparencia aplanadas
peso: 170.8 MB → 32.2 MB (81% menos) · tiempo: 28 s

fotos: 298 · peso total: 32.2 MB · media: 108 kB
tamaños distintos: 1 (1200x1200 en las 298)
se reabren y decodifican enteras: 298/298
franja marcada (el 'arriba' real) en: arriba 298/298
```

Y las tres cosas que se demuestran por el camino:

- La versión ingenua (`lote_ingenuo.py`) se cae en la **cuarta** foto: `cannot write mode RGBA as JPEG`.
- Sin el giro EXIF (`lote.py --sin-giro`) el marcador de "arriba" acaba en el borde **izquierdo** en
  **41 de las 298** fotos: las giradas salen de lado.
- La marca de agua se comprueba por diferencia de píxeles entre la misma foto con y sin:
  **15.152 píxeles cambiados**, todos dentro del rectángulo esperado.

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
