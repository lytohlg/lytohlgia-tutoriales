# Tu script, en un programa que corre sin Python

## Qué vas a conseguir

Un **único fichero ejecutable** de 11 MB, hecho con PyInstaller, que se abre con doble clic en una
máquina donde **Python no está instalado** y saca el mismo informe de ventas que el script original.
Y, tan importante como eso, entenderás **los tres sitios donde esto se rompe**: los datos que no
viajan dentro del ejecutable, la versión de glibc del sistema donde compilaste y el coste real de
empaquetarlo todo en un solo fichero.

## El problema (por qué existe este paquete)

Tienes un script que te resuelve el día: lee el CSV de ventas y devuelve el resumen en una tabla.
Funciona en tu portátil. Se lo mandas a quien lo necesita —administración, la tienda, un compañero
de otra sede— y no arranca: `python no se reconoce como un comando`, `ModuleNotFoundError: No module
named 'rich'`, o se cierra sin decir nada. Empieza el bucle de soporte: instala Python, marca «Add to
PATH», abre una consola, escribe `pip install ...`.

## Requisitos

- **Docker** (probado con Docker 24 o superior) en Linux, macOS o Windows.
- **2 vCPU y 2 GB de RAM** libres para el contenedor; **1 GB de disco** (la imagen base y el
  ejecutable de 11 MB).
- **Sin GPU, sin credenciales y sin red**: la imagen del entorno ya trae `pyinstaller` y `rich`, y la
  demo no descarga nada.
- No necesitas Python instalado en tu máquina: todo ocurre dentro del contenedor.

## Entorno de pruebas

La imagen se construye desde `entorno/Dockerfile` (`python:3.12-slim-bookworm` + `binutils` +
`pyinstaller==6.11.1` + `rich==13.9.4`). Es la misma que se usó para grabar el vídeo:

```bash
docker build -t pyinstaller-tu-script-sin-python:local entorno/
```

Se elige **bookworm** a propósito: es la base más vieja que soportamos, y compilar ahí es lo que hace
que el ejecutable funcione también en sistemas posteriores. Ese es uno de los fallos que se explican
más abajo.

## Pasos

```bash
docker run --rm -v "$PWD":/trabajo -w /trabajo pyinstaller-tu-script-sin-python:local bash demo.sh
```

La demo hace, en este orden, lo mismo que el vídeo:

1. ejecuta el programa **sin empaquetar** (necesita Python, aquí lo tiene);
2. lo compila con `pyinstaller --onefile --name resumen --add-data "plantilla.txt:." resumen.py`;
3. copia **solo el ejecutable** a otro directorio y lo ejecuta allí;
4. compila y ejecuta `resumen_v1.py`, la versión que **se rompe**;
5. abre el ejecutable con `pyi-archive_viewer` para ver qué lleva dentro.

Las comprobaciones automáticas del resultado:

```bash
docker run --rm -v "$PWD":/trabajo -w /trabajo pyinstaller-tu-script-sin-python:local bash pruebas/pruebas.sh
```

## Qué hace cada fichero

- `resumen.py` — el programa final. Lee el CSV, calcula total, media y mediana, y pinta la tabla con
  `rich`. Resuelve sus ficheros empaquetados con `sys._MEIPASS` (función `carpeta_datos()`).
- `resumen_v1.py` — la primera versión, la que abre `plantilla.txt` con ruta relativa. Sirve para
  reproducir el fallo: funciona en la carpeta del código y muere en cuanto el ejecutable se mueve.
- `plantilla.txt` — la cabecera del informe. Es el fichero que PyInstaller **no** mete dentro si no se
  lo dices con `--add-data`; el que provoca el `FileNotFoundError`.
- `datos/ventas.csv` — la entrada: 120 filas de ventas (fecha, cliente, concepto, importe). Los
  clientes y los importes son inventados.
- `datos/generar_ventas.py` — genera ese CSV de forma determinista (semilla fija, sin red). No hace
  falta ejecutarlo: el CSV ya está en el paquete; está aquí para que sepas de dónde salen los datos y
  puedas cambiar los importes y volver a probar.
- `entorno/Dockerfile` — la imagen de pruebas (Python 3.12 en bookworm, `binutils`, `pyinstaller`,
  `rich`). Todo lo que se ejecuta arriba sale de aquí.
- `demo.sh` — la secuencia completa del vídeo, de principio a fin.
- `pruebas/pruebas.sh` — ejecuta `bash demo.sh` (el mismo comando que declara el manifiesto) y
  comprueba que la salida contiene la tabla, el error real y las piezas del ejecutable.
- `material.json` — la ficha pública de este paquete (título, fecha de estreno, si necesita
  credenciales).
- `.env.example` — vacío a propósito: este paquete **no usa variables de entorno**. Existe para que
  quede claro que no hay nada que configurar (ni claves, ni rutas, ni cuentas).

## Resultado esperado

```
== 1. El programa antes de empaquetar: lee el CSV y saca la tabla ==
INFORME DE VENTAS · cierre trimestral
filas: 120   total: 53,095.85 EUR
ticket medio: 442.47 EUR   mediana: 438.49 EUR
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ cliente          ┃       importe ┃
│ Grupo Delta      │ 10,235.42 EUR │
...
== 2. Compilar con una sola orden ==
INFO: Building EXE from EXE-00.toc completed successfully.
ejecutable: 11M  dist/resumen

== 3. La prueba de verdad: otro directorio, sin el código fuente al lado ==
INFORME DE VENTAS · cierre trimestral
== 4. La versión que se rompe: busca la plantilla 'de al lado' ==
FileNotFoundError: [Errno 2] No such file or directory: 'plantilla.txt'
== 5. Lo que lleva dentro el ejecutable ==
'libpython3.12.so.1.0'
'plantilla.txt'
```

Los importes pueden variar si regeneras el CSV; el tamaño del ejecutable (11 MB ± 1 MB) depende de la
versión de PyInstaller.

## Coste / credenciales

**Cero coste y cero credenciales.** No hay API, ni cuenta, ni servicio externo. La única descarga es
la imagen base de Python al construir el entorno la primera vez (~50 MB); después todo funciona sin
red. El paquete no contiene claves ni datos personales: los clientes del CSV son inventados.

## Solución de problemas

- **`FileNotFoundError: 'plantilla.txt'`** al ejecutar fuera de la carpeta del código: te falta
  `--add-data "plantilla.txt:."` o no estás resolviendo la ruta con `sys._MEIPASS`. Es el fallo de la
  escena 4, reproducido a propósito con `resumen_v1.py`.
- **`version 'GLIBC_2.38' not found`**: compilaste en un sistema más nuevo que el de destino. Compila
  en la imagen más vieja que vayas a soportar (`bookworm`, glibc 2.36) y vuelve a empaquetar.
- **`objdump not found` / `On Linux, objdump is required`**: falta `binutils` en la imagen donde
  compilas. Está en `entorno/Dockerfile`.
- **El ejecutable pesa 40 MB o más**: estás empaquetando dependencias grandes (numpy, pandas). Usa
  `--exclude-module` para las que no necesites, o cambia a `--onedir`.
- **Tarda en arrancar**: es `--onefile`, que se descomprime en cada ejecución (~0,3 s aquí). Con
  `--onedir` arranca casi al instante a cambio de repartir una carpeta.

## Límites, dichos claros

- **No compila para otro sistema**: en Linux produces un binario de Linux; para Windows hay que
  empaquetar en Windows.
- **No protege el código**: el bytecode viaja dentro y se puede extraer con herramientas públicas
  (`pyi-archive_viewer` es una de ellas, y viene con PyInstaller).
- **Antivirus y SmartScreen** pueden avisar la primera vez con un ejecutable sin firma.
- **glibc**: un binario hecho en una imagen moderna no arranca en una distribución más vieja.

## Alternativas

`Nuitka` (compila a C: arranca más rápido y cuesta más extraer el código, pero compila mucho más
lento), `shiv`/`zipapp` (un `.pyz`, pero necesita Python instalado) y los instaladores nativos
(`Inno Setup` en Windows), que resuelven el reparto, no el empaquetado.

## Proyecto y documentación

- Repositorio: https://github.com/pyinstaller/pyinstaller (libre, ~13.000 estrellas)
- Documentación: https://pyinstaller.org
