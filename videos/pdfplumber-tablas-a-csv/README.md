# pdfplumber: extrae las tablas de un PDF a CSV sin copiar

> Material del vídeo **pdfplumber: extrae las tablas de un PDF a CSV sin copiar** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

Cada mes llegan los albaranes en PDF. La información está ahí, en una tabla perfectamente legible
para un humano: referencia, descripción, cantidad, precio e importe. Y hay que pasarla a una hoja de
cálculo. Se selecciona el texto con el ratón, se pega en Excel, y las columnas se descolocan: la
descripción se parte en tres celdas, el precio se mezcla con la cantidad. Al final se copia a mano,
línea por línea, y a la novena línea ya no se lee lo que se copia.

Este paquete hace la parte mecánica y, sobre todo, la parte que casi nadie hace: **comprobar que lo
extraído es lo que el PDF dice**. Al final hay un comando que devuelve `VERIFICADO` o se niega, y una
prueba negativa que demuestra que la comprobación no es decorativa.

Los tres albaranes de ejemplo **los fabrica el propio script** con datos inventados: no hace falta el
documento de nadie para reproducir esto. Y eso también marca el límite de lo que demuestra: prueba el
método sobre tres problemas típicos (tabla con líneas, tabla sin líneas, celda de dos líneas), no
certifica que funcione con tu proveedor concreto.

## Qué vas a conseguir
- Un script que convierte **todas** las tablas de todos los PDF de una carpeta en un CSV por tabla.
- Entender por qué `extract_table()` devuelve `None` en un PDF sin líneas dibujadas, y cómo se arregla
  usando el texto como si fuera la rejilla.
- Una comprobación que recalcula cantidad × precio, suma los importes y lo compara con el total
  impreso dentro de cada PDF, además del número de líneas.
- Una prueba negativa: se toca un importe en el CSV y la comprobación lo caza.
- Los límites, medidos: filas partidas por celdas de dos líneas y PDF escaneados sin texto.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).
- `pdfplumber` 0.11.5 — la herramienta del vídeo.
- `reportlab` 4.2.5 — solo para dibujar los albaranes de ejemplo.
- Opcional: `poppler-utils` (`pdftoppm`), para fabricar el PDF escaneado del apartado de límites. Sin
  él, ese límite se salta y lo dice.
- Nada de conexión a internet, ni cuentas, ni claves de API.

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base).

## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. El vídeo y estas pruebas se grabaron sobre `python:3.12-slim` con el `Dockerfile`
que está en `entorno/Dockerfile`: instala `poppler-utils`, las fuentes DejaVu y las dos bibliotecas de
Python con la versión fijada. Hardware mínimo real: **1 GB de RAM y 1 CPU**; menos de 500 MB de disco
para la imagen. El proceso completo tarda segundos: lo más lento es instalar.

**Ficheros que forman el entorno**:
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio.

## Pasos
1. Construye la máquina de pruebas (una sola vez):
   ```bash
   docker build -t repro-pdfplumber-tablas-a-csv:local entorno
   ```
2. Ejecuta la demo dentro, con esta carpeta montada en solo lectura y una copia de trabajo en `/tmp`
   (el script no toca tus ficheros):
   ```bash
   docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
     -v "$PWD:/trabajo:ro" repro-pdfplumber-tablas-a-csv:local \
     bash -lc "mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
   ```
3. O las dos cosas de una vez con `bash pruebas/pruebas.sh`, que además comprueba la salida.

Sin Docker también vale: instala `pdfplumber==0.11.5` y `reportlab==4.2.5` con `pip` y ejecuta
`bash demo.sh` en la carpeta.

### Por partes, que es como se explica en el vídeo
```bash
python3 scripts/crear_albaranes.py                          # fabrica los 3 PDF
python3 scripts/extraer.py --pdf entrada/albaran_0310.pdf   # con líneas: la ve
python3 scripts/extraer.py --pdf entrada/albaran_0320.pdf   # sin líneas: 0 tablas
python3 scripts/extraer.py --pdf entrada/albaran_0320.pdf --estrategia text
python3 scripts/volcar.py --carpeta entrada --salida salida  # CSV, uno por tabla
python3 scripts/verificar.py --carpeta entrada               # comprobación
python3 scripts/limites.py                                   # lo que no hace
```

Y la prueba negativa, para ver que la comprobación sirve de algo:
```bash
cp -r salida salida_tocada
python3 scripts/tocar_csv.py salida_tocada/albaran_0310_tabla1.csv
python3 scripts/verificar.py --csv salida_tocada --carpeta entrada   # sale con código 1
```

## Qué hace exactamente la comprobación
Por cada albarán: fusiona las filas que son continuación de una descripción de dos líneas, recalcula
`cantidad × precio` de cada línea y lo compara con su importe, suma los importes y lo compara con el
`TOTAL ALBARAN` impreso **dentro del PDF**, y compara el número de filas con el `LINEAS` que el propio
PDF declara. Si algo no cuadra, escribe `NO CUADRA` y sale con código 1.

Aviso honesto: comparar contra el total del mismo PDF **no es una fuente independiente**. Sirve para
cazar lo que se pierde al extraer (filas, columnas, importes), no para certificar que el PDF original
es correcto. Un error en la descripción o en la referencia pasaría estas comprobaciones.

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `scripts/crear_albaranes.py` | Fabrica los tres PDF de ejemplo y calcula su total. |
| `scripts/extraer.py` | Extrae la tabla de un PDF con dos estrategias distintas. |
| `scripts/volcar.py` | Vuelca todas las tablas de una carpeta a CSV. |
| `scripts/verificar.py` | Comprueba filas, importes y total contra el PDF. |
| `scripts/tocar_csv.py` | Prueba negativa: cambia un importe del CSV. |
| `scripts/limites.py` | Mide los límites (celdas partidas, PDF escaneado). |
| `entorno/Dockerfile` | La máquina donde se prueba, con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. |
| `.env.example` | Plantilla de claves. Este material no necesita ninguna. |

## Resultado esperado
VERIFICADO: 3 albaranes, 33 lineas, 0 descuadres

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta `pdfplumber` o `reportlab`; instálalos y vuelve a empezar.
- **`0 tablas` en el PDF que sí la tiene**: no hay líneas dibujadas; usa `--estrategia text`.
- **Una fila de más**: es una descripción de dos líneas; `verificar.py` la fusiona.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Dónde está la herramienta
- Repositorio: <https://github.com/jsvine/pdfplumber> (licencia MIT).
- Documentación: <https://pdfplumber.readthedocs.io/> — el apartado `table_settings` es el que importa
  aquí.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
