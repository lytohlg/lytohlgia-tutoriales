# Plotly: tu CSV en un gráfico interactivo que se abre en el navegador

> Material del vídeo **Plotly: tu CSV en un gráfico interactivo que se abre en el navegador** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema
Cada mes mandas el informe de ventas en una captura de pantalla o en un PDF. Se lee una vez y se
archiva: no se puede filtrar, no se puede tocar, y para cambiar una cifra hay que volver a la hoja
de cálculo, filtrar otra vez y mandar otra captura. **A quién le duele**: a quien hace ese informe a
mano cada mes y lo manda a alguien que solo quería mirar dos números.

## Qué vas a conseguir
Convertir el CSV que exporta Excel (separado por `;` y con comas decimales) en **un fichero HTML
autocontenido** con gráficos de Plotly: barras, línea por mes y un informe con los dos. El fichero se
abre con doble clic en cualquier navegador, sin servidor y sin instalar nada, y al pasar el ratón por
encima de una barra te da el importe exacto. En el vídeo, ese fichero pesa 4,7 MB y contiene los datos
dentro.

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
- `entorno/Dockerfile` — describe la máquina: `python:3.12-slim` con `plotly==7.2.0` y `pandas==2.3.3`.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio.
- `.env.example` — plantilla de las claves que necesite el material. Se copia a `.env` (que **no**
  se sube nunca al repositorio). Este material no usa ninguna: el fichero está para que el patrón
  sea el mismo en todos los vídeos.

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno.

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base):
```bash
docker --context default build -t repro-plotly-csv-interactivo:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-plotly-csv-interactivo:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno.

**Detalles de nuestra ejecución:** `--context default` fuerza el motor Docker local — útil si tienes
configurado además uno remoto; si en tu equipo solo hay uno, déjalo igual o quítalo. Ejecutamos con
el usuario `1000:1000` y `HOME=/tmp`. El contenedor no lleva credenciales dentro.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd plotly-csv-interactivo
   ```
2. (Opcional) Prepara tus variables de entorno. Este material no necesita ninguna, pero el patrón
   es el mismo en todos los vídeos:
   ```bash
   cp .env.example .env
   ```
3. Ejecuta la demo. En tu máquina, con las dependencias instaladas, es:
   ```bash
   bash demo.sh
   ```
   Y dentro del contenedor del paso 2, la orden larga de arriba.

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `gen_datos.py` | Genera `datos/ventas.csv` (datos de **ejemplo**, `random.seed(11)`): 108 filas de tres tiendas en doce meses. |
| `datos/ventas.csv` | El CSV "sucio" tal como lo exporta Excel en español: separador `;`, coma decimal. |
| `carga.py` | Lee el CSV con `pandas` y comprueba que salen 108 filas y seis columnas. |
| `barras.py` | Gráfico de barras por tienda con el importe en el tooltip. |
| `linea.py` | Ventas mes a mes (el eje se declara de categorías para que el hover funcione). |
| `informe.py` | Los dos gráficos en un solo HTML: el fichero que se abre con doble clic. |
| `personaliza.py` | Cambiar columna y ruta: el mismo código con otros datos. |
| `error.py` | Pide una columna que no existe (`x="mes"`) y enseña el error real de Plotly. |
| `arreglo.py` | Crea la columna que faltaba y vuelve a dibujar. |
| `pruebas/pruebas.sh` | Construye el entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y versiones fijadas. |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `salida/` | Donde caen los HTML que generan los scripts. Va vacía en el repositorio: se llena al ejecutar `bash demo.sh`. |
| `.gitignore` | Evita subir los HTML generados en `salida/` y los `__pycache__`: son resultados, no código. |

**La trampa del CSV español** (está en el código y se ve en el vídeo): `pd.read_csv(..., sep=';',
decimal=',')`. Sin esos dos argumentos, pandas lee **una sola columna** y todos los gráficos fallan.

## Resultado esperado
Salida real de `bash demo.sh` en el contenedor (`python:3.12-slim`, plotly 7.2.0, pandas 2.3.3),
recortada a las líneas con cifras (las tablas de pandas se muestran abreviadas aquí; el comando las
imprime enteras):

```
== 0. El fichero tal cual sale de Excel (separador ; y coma decimal) ==
fecha;tienda;producto;unidades;precio_unitario;total
2026-01-01;Centro;teclado;54;19,9;1074,60
...

== 1. Abrirlo en Python: primero sale mal, y así se lee bien ==
columnas: ['fecha;tienda;producto;unidades;precio_unitario;total']
filas: 108
columnas: ['fecha', 'tienda', 'producto', 'unidades', 'precio_unitario', 'total']
2026-01-01  Centro  teclado   54   19.9  1074.60
...
total facturado: 224780.6 euros

== 2. Barras por tienda: un HTML que se abre en el navegador ==
Centro  104623.30
Norte    69840.20
Sur      50317.10
salida/barras.html: 4711 KB

== 3. La misma facturación, mes a mes y con una línea por tienda ==
puntos dibujados: 36
salida/linea.html: 4712 KB

== 4. Los dos gráficos en un solo informe ==
salida/informe.html -> 4712 KB
trazas dentro: 2

== 5. Con tus datos: cambias la columna y la ruta, nada más ==
salida/personalizado.html: 3 barras por producto

== 6. El error que te vas a encontrar: pedir una columna que no existe ==
ValueError: Value of 'x' is not the name of a column in 'data_frame'. Expected one of ['fecha', 'tienda', 'producto', 'unidades', 'precio_unitario', 'total'] but received: mes
salida/arreglado.html: 4714 KB

== 7. Lo que se abre en el navegador (ficheros generados) ==
-rw-r--r-- 1 1000 1000 4.7M arreglado.html
-rw-r--r-- 1 1000 1000 4.7M barras.html
-rw-r--r-- 1 1000 1000 4.7M informe.html
-rw-r--r-- 1 1000 1000 4.7M linea.html
-rw-r--r-- 1 1000 1000 4.7M personalizado.html
   -> doble clic en salida/informe.html: es un fichero, no hace falta servidor
```

Los tamaños en KB se midieron con este mismo código y estos mismos datos; pueden bailar unos pocos KB
según el build de Plotly, porque el HTML lleva la librería dentro.

Los datos son de **ejemplo**: los genera `gen_datos.py` con `random.seed(11)`. No son ventas reales
de nadie y puedes repetirlos tantas veces como quieras.

## Coste / credenciales
Nada: todo lo que hace este material es gratis y no necesita claves. La primera construcción
necesita red para descargar la imagen base y los paquetes de PyPI; después funciona sin conexión.

## Solución de problemas
- **«command not found: docker»**: te falta Docker; instálalo y vuelve a empezar.
- **El gráfico sale vacío o con una sola columna**: el CSV no lleva `sep=';'` y `decimal=','`.
- **`ValueError: Value of 'x' is not the name of a column...`**: pides una columna que el
  DataFrame no tiene (en el vídeo, `mes`); mira la lista que imprime el propio error.
- **El hover no aparece en la línea**: declara el eje como categorías (`update_xaxes(type="category")`).
- **Falla el build**: comprueba la conexión; una red corporativa puede bloquear PyPI.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
