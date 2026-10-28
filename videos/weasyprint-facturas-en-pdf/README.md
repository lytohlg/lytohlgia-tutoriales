# WeasyPrint: facturas en PDF desde HTML y CSS, sin maquetar a mano

> Material del vídeo **WeasyPrint: facturas en PDF desde HTML y CSS, sin maquetar a mano** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Cada mes hay que sacar la misma factura, el mismo informe, el mismo presupuesto. Y cada mes alguien
la rehace a mano: se abre el documento del mes pasado, se cambian los importes, se mueve la tabla
porque ahora tiene seis líneas en vez de cuatro, y se reza para que el total no se quede huérfano al
final de una página y la firma no se vaya sola a la siguiente.

Cuando el PDF lo genera una aplicación, el problema es el mismo con otro nombre: el diseño está
metido en el código, en medio de la lógica, y cualquier cambio de maquetación obliga a tocar el
programa.

El coste no es el rato: es el PDF que sale mal el día de la entrega, y la tarde que se va en mover
una tabla que debería colocarse sola.

## Qué vas a conseguir

Un PDF de tres páginas generado desde un fichero HTML y una hoja de estilos, con:

- la **cabecera repetida en todas las páginas** sin escribirla tres veces,
- la **numeración «Página 1 de 3»** calculada sola,
- la **cabecera de la tabla repetida** en cada página, para que nadie lea importes sin saber qué
  columna es cuál,
- y el **mismo HTML sirviendo para otro cliente** con solo cambiar el fichero de datos.

Salida esperada al terminar la demo:

```
VERIFICADO: 3 páginas · cabecera 3/3 · numeración 3/3 · cabecera de tabla 3/3 (sin la regla, 1/3) · filas partidas 0 · otro cliente en 1 página · sin JavaScript · fuente pedida Arial Black -> embebida DejaVu-Sans
```

## Requisitos

**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.13 o superior si prefieres ejecutarlo fuera del contenedor (`python3 --version`).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- La prueba se hizo en un servidor con 2 CPU y 6 GB de RAM, Docker 26.1.5 sobre Python 3.13.17.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base, las librerías del
sistema que necesita WeasyPrint y la fuente).

## Entorno de pruebas

Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

La imagen es `python:3.13-slim` más las librerías del sistema que WeasyPrint necesita (Pango,
Fontconfig y una fuente real) y `poppler-utils` para verificar el PDF (`pdfinfo`, `pdftotext`,
`pdffonts`). La versión de WeasyPrint está fijada: `weasyprint==70.0`.

Dentro del contenedor esta carpeta se monta en **solo lectura** y se copia a una carpeta temporal: la
prueba no puede tocar tu copia del material.

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos porque descarga la imagen
base):
```bash
docker build -t repro-weasyprint-facturas-en-pdf:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en solo
lectura:
```bash
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" \
  repro-weasyprint-facturas-en-pdf:local \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace lo anterior y
además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así:** el contenedor no lleva nada tuyo dentro, la carpeta entra montada como solo-lectura
y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu máquina: lo que falla en
limpio es un fallo real, no un resto de tu entorno. El contenedor **sí tiene red** (la necesita para
construirse, no para ejecutar la demo); lo que no tiene son tus datos.

## Pasos

1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd weasyprint-facturas-en-pdf
   ```
2. Este material no necesita claves, pero la plantilla de entorno está para que la costumbre no se
   pierda (ver `.env.example`):
   ```bash
   cp .env.example .env
   ```
3. Ejecuta la demo:
   ```bash
   bash demo.sh
   ```
4. Si quieres repetir la prueba completa en limpio:
   ```bash
   bash pruebas/pruebas.sh
   ```

## Qué hace cada fichero

| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base, librerías del sistema y `weasyprint==70.0`. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta `bash demo.sh` en un contenedor limpio. |
| `.env.example` | Plantilla de variables de entorno (aquí no hay ninguna clave). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: el problema, los pasos, el entorno de pruebas y el resultado esperado. |
| `scripts/generar.py` | Convierte datos + plantilla + hoja de estilos en un PDF y dice cuántas páginas tiene. |
| `scripts/minimo.py` | El PDF más pequeño posible: seis líneas, sin datos ni plantilla. |
| `scripts/verificar.py` | Abre el PDF, lo pasa a texto y cuenta cabeceras, numeración, cabeceras de tabla y filas partidas. |
| `scripts/limites.py` | Mide los dos límites: no ejecuta JavaScript y sustituye la fuente si no está instalada. |
| `scripts/comprobar.py` | Comprobación final: vuelve a medir los tres PDF y falla si algo no se cumple. |
| `plantillas/factura.html` | La estructura del documento. Los huecos son `{{asi}}`. |
| `estilos/factura.css` | El aspecto y la paginación: `@page`, cabecera, pie, numeración y repetición de cabecera de tabla. |
| `estilos/sin-regla.css` | La misma hoja con una diferencia: la cabecera de la tabla deja de repetirse. |
| `datos/factura-2026-1042.json` | Los datos de la factura larga (42 líneas, 3 páginas). |
| `datos/factura-2026-1043.json` | Los datos de otra factura: mismo HTML, una página. |

### Qué hace cada script, paso a paso

- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo, en
  ese orden. Cinco bloques: generar y verificar, enseñar la cabecera y la numeración, comparar con la
  hoja sin la regla, otro cliente, y los límites. Se puede leer entero antes de ejecutarlo.
- **`scripts/generar.py`** — lee el JSON, rellena la plantilla HTML sustituyendo `{{clave}}` por su
  valor, construye las filas de la tabla y entrega todo a WeasyPrint junto con la hoja de estilos. No
  escribe ni una coordenada: dónde va cada cosa lo decide el CSS.
- **`scripts/minimo.py`** — la versión mínima, para probar que el motor funciona antes de meterse con
  plantillas: una cadena de HTML y `write_pdf`. Si esto sale, WeasyPrint está bien instalado.
- **`scripts/verificar.py`** — no se fía de que el script «haya terminado bien»: convierte el PDF a
  texto con `pdftotext -layout` y comprueba página por página que la cabecera y la numeración están
  donde deben, que la cabecera de la tabla se repite y que cada línea conserva su importe.
- **`scripts/limites.py`** — genera un PDF pequeño con un `<script>` dentro y con una fuente que no
  está instalada; después mira el resultado: el texto del script no aparece y la fuente embebida no
  es la que se pidió.
- **`scripts/comprobar.py`** — la comprobación final: vuelve a medir los tres PDF y el PDF de límites,
  y si algo no cuadra imprime los fallos y sale con error.
- **`entorno/Dockerfile`** — construye la máquina de pruebas desde una imagen base con la versión
  fijada, instala lo que WeasyPrint necesita y deja el directorio de trabajo preparado. No copia
  claves ni datos personales.
- **`pruebas/pruebas.sh`** — la prueba real: construye la imagen, ejecuta la demo en un contenedor
  limpio con la carpeta en solo lectura y comprueba que la salida contiene lo prometido.
- **`.env.example`** — la lista de variables de entorno que el material espera. Aquí está vacía de
  contenido real: el material no pide ninguna clave.

## Resultado esperado

Al final de `bash demo.sh` sale una sola línea que resume lo verificado:

```
VERIFICADO: 3 páginas · cabecera 3/3 · numeración 3/3 · cabecera de tabla 3/3 (sin la regla, 1/3) · filas partidas 0 · otro cliente en 1 página · sin JavaScript · fuente pedida Arial Black -> embebida DejaVu-Sans
```

Los números no son una promesa de marketing: los cuenta `scripts/comprobar.py` sobre el PDF, y si no
cuadran el script falla. Si no sale esa línea, algo del entorno no está como se describe arriba.

## Coste y credenciales

- **Coste**: cero. Todo corre en tu máquina, sin cuenta, sin tarjeta y sin servicios de pago.
- **Credenciales**: ninguna. No hay claves, ni tokens, ni login.
- **Datos**: ninguno real. El cliente, el NIF, la dirección y las líneas son inventados.

## Solución de problemas

- **`cannot load library 'libgobject-2.0-0'` al importar weasyprint**: faltan las librerías del
  sistema. No es un problema de `pip`: instala `libpango-1.0-0`, `libpangoft2-1.0-0`,
  `libharfbuzz-subset0` y `libfontconfig1`, y una fuente (por ejemplo `fonts-dejavu-core`).
- **`pdftotext: command not found`**: falta `poppler-utils`. Es solo para verificar; sin él la
  generación funciona, pero `verificar.py` no puede contar páginas.
- **La fuente no es la que pediste**: WeasyPrint no descarga fuentes. Si la que pides no está
  instalada en la máquina, la sustituye. Instálala como paquete o cópiala a `/usr/share/fonts`.
- **La paginación no coincide con la del vídeo**: fija la versión (`weasyprint==70.0`) y usa la misma
  fuente. Entre versiones el texto ocupa distinto y el número de páginas cambia.
- **`Permission denied` al escribir en `salida/`**: en la prueba la carpeta va montada en solo
  lectura; la demo escribe en la copia temporal, no en el original.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia

MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
