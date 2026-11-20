# Genera diagramas UML desde tu código Python con Gaphor

> Material del vídeo **Genera diagramas UML desde tu código Python con Gaphor** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

El problema que resuelve: un diagrama de clases dibujado a mano dura hasta que el código cambia.
A partir de ahí miente, y nadie lo actualiza porque actualizarlo es una tarde arrastrando cajas.
Este material hace lo contrario: el diagrama es **la salida de un script**, así que se vuelve a
generar en un comando cada vez que el código cambia.

## Qué vas a conseguir
Dos scripts de Python que construyen un modelo UML real con [Gaphor](https://gaphor.org) y lo
exportan a PNG y SVG **sin abrir ninguna ventana**:

1. `modelo.py` describe el modelo a mano (5 clases, 3 asociaciones, 1 herencia) y exporta el diagrama.
2. `desde_codigo.py` lee una carpeta de código con `ast`, saca las clases, sus atributos anotados y
   las herencias, y construye el mismo tipo de modelo. Si añades una clase al código y relanzas el
   script, el diagrama sale con una clase más: no hay que tocar el script.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.11 o superior si quieres ejecutarlo fuera del contenedor (`python3 --version`).
- Gaphor 3.3.2 (lo instala el entorno) y las bibliotecas gráficas de GTK 4, GtkSource 5 y
  libadwaita: Gaphor es una aplicación de escritorio y las necesita aunque solo exportes.

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 2 GB de disco libre para la imagen del contenedor (compila PyGObject).

**Tiempo estimado**: 10-15 minutos la primera vez (la imagen compila pycairo y PyGObject).

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
docker --context default build -t repro-diagramas-uml-python-gaphor:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-diagramas-uml-python-gaphor:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd diagramas-uml-python-gaphor
   ```
2. (Opcional) Prepara tus variables de entorno: este material no necesita ninguna, pero el patrón
   es el de siempre — nunca escribas claves dentro de un script.
   ```bash
   cp .env.example .env
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `modelo.py` | Construye a mano un modelo UML de pedidos (5 clases, 3 asociaciones, 1 herencia), guarda `pedidos.gaphor` y exporta `salida/Pedidos/Pedidos.png`. |
| `desde_codigo.py` | Lee una carpeta de código con `ast` y construye el modelo solo: clases, atributos anotados y herencias. Exporta PNG y SVG. Uso: `python3 desde_codigo.py tienda`. |
| `tienda/` | Código de ejemplo que lee `desde_codigo.py` (5 clases). |
| `tienda/modelos.py` | Las cinco dataclasses del ejemplo (`Cliente`, `Producto`, `Pedido`, `PedidoUrgente`, `LineaPedido`) con sus anotaciones de tipo: es la entrada que `desde_codigo.py` convierte en diagrama. |
| `tienda_v2/` | El mismo código con una clase más (`Devolucion`): sirve para ver que el diagrama cambia sin tocar el script. |
| `tienda_v2/modelos.py` | Copia exacta de `tienda/modelos.py`: la base sobre la que se añade la clase nueva. |
| `tienda_v2/devoluciones.py` | La clase añadida al final (`Devolucion`): la prueba de que relanzar el mismo script produce un diagrama distinto. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (aquí, ninguna). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal.
- **`modelo.py`** — crea una `ElementFactory`, crea las clases (`Cliente`, `Producto`, `Pedido`,
  `LineaPedido`, `PedidoUrgente`), les añade atributos, declara tres asociaciones con
  `create_association` y una herencia con `create_generalization`, coloca cada clase en el diagrama
  con `drop` y une las líneas con `connect`. Guarda el modelo con `storage.save` y exporta con
  `export_all(..., save_png, "png")`. La CLI `gaphor export` no se usa: en un contenedor sin
  escritorio falla al cargar plugins, y el camino fiable es la API.
- **`desde_codigo.py`** — recorre los `*.py` de la carpeta que le pases, los parsea con `ast`, y por
  cada `ClassDef` construye una clase del modelo con sus anotaciones de tipo y sus bases. Lo que
  **no** hace: inventar asociaciones. El código no las declara, así que la salida pone
  `asociaciones: 0` y el diagrama sale sin líneas horizontales.
- **`entorno/Dockerfile`** — construye la máquina de pruebas: Debian 13, las bibliotecas gráficas
  de GTK 4 / GtkSource 5 / libadwaita, herramientas de compilación y `gaphor==3.3.2` en un venv.
- **`pruebas/pruebas.sh`** — la prueba de verdad: construye la imagen, copia la carpeta a un
  directorio temporal dentro del contenedor y ejecuta ahí la demo, con la carpeta original montada
  en solo lectura. Si algo falla, para y dice en qué paso.

## Resultado esperado
Salida real de la demo (los identificadores y las fechas cambian en cada ejecución, porque el modelo
genera ids nuevos; el resto es igual):

```
== 1. Un modelo UML escrito en Python: se guarda y se exporta ==
modelo guardado: 5 clases, 3 asociaciones, 1 generalizaciones
exportado: salida/Pedidos/Pedidos.png
-rw-r--r-- 1 1000 1000  12345 ... salida/Pedidos/Pedidos.png

== 2. El modelo es texto y la imagen es una imagen ==
<?xml version="1.0" encoding="utf-8"?>
<gaphor xmlns="https://gaphor.org/model" ... gaphor-version="3.3.2">
<model>
<UML:Class id="...">
...
salida/Pedidos/Pedidos.png: PNG image data, 803 x 309, 8-bit/color RGBA, non-interlaced

== 3. Del código existente al diagrama (ast) ==
leídas 5 clases del código
herencias dentro del paquete: 1
atributos totales: 11
asociaciones: 0 (el código no las declara; no se inventan)
exportado: salida_tienda/Tienda/Tienda.png y .svg

== 4. Añadimos una clase y volvemos a lanzar el mismo script ==
class Devolucion:
    ...
leídas 6 clases del código
...
exportado: salida_tienda_v2/Tienda_v2/Tienda_v2.png y .svg
```

## Límites (lo que este material NO hace)
- Las cajas del PNG salen **con el nombre**: los compartimentos con atributos no los pinta la API de
  export. Para eso hay que trabajar en el editor.
- La **posición** de cada caja la decides tú en el script. Si la colocas mal, el diagrama sale feo
  aunque el modelo sea correcto.
- Sin entorno gráfico no hay aplicación, solo modelo y export.
- **No infiere asociaciones** que el código no declara. Un diagrama generado desde `ast` es un mapa
  de clases y herencias, no un diagrama de relaciones completo.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **`pip install gaphor` falla compilando `pycairo` / `PyGObject`**: faltan cabeceras y compilador.
  Instala `build-essential`, `pkg-config`, `libcairo2-dev`, `libgirepository-2.0-dev` y `python3-dev`
  (es justo lo que hace `entorno/Dockerfile`).
- **La app arranca a medias o no arranca**: falta `gir1.2-gtksource-5` o `gir1.2-adw-1`.
- **El export no escribe ningún fichero y no dice por qué**: el diagrama no pertenece a un paquete.
  Un `Diagram` tiene que colgar de un `UML.Package` (`paquete.ownedDiagram = diagrama`).
- **`TypeError: Value should be of type UML:Diagram`**: `Diagram` importado de
  `gaphor.core.modeling`; hay que importarlo de `gaphor.UML`.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
