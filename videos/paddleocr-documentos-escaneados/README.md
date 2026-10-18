# PaddleOCR: busca dentro de tus PDF escaneados con Python

> Material del vídeo **PaddleOCR: busca dentro de tus PDF escaneados con Python** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Encontrar un dato concreto dentro de una carpeta de facturas escaneadas —sin abrirlas una a una y
sin subir tus documentos a ningún servicio— construyendo con PaddleOCR un índice local y buscando
en él con Python.

## Requisitos
**Software**
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Nada más. Ni Python en tu sistema ni claves: todo ocurre dentro del contenedor.

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y ~3 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor con la CPU de un servidor pequeño.

**Tiempo estimado**: 15-20 minutos la primera vez (incluye construir la imagen: descarga
PaddlePaddle, PaddleOCR y los pesos de los modelos). Después, la demo tarda unos minutos.

## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (dos, no hay más):
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada
  (`paddlepaddle==3.3.1`, `paddleocr==3.7.0`). Al construirse **descarga también los pesos de los
  modelos**, así que cuando ejecutas la demo no necesita red.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta.

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos porque descarga la imagen
base, las dependencias y los modelos):
```bash
docker build -t repro-paddleocr-documentos-escaneados:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios y con esta carpeta montada en **solo lectura**
(el script no puede tocar tus ficheros originales: trabaja sobre una copia en `/tmp`):
```bash
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" \
  repro-paddleocr-documentos-escaneados:local \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno.

**Si tienes más de un motor Docker** (por ejemplo uno remoto configurado por defecto), añade
`--context default` a las órdenes de arriba.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd paddleocr-documentos-escaneados
   ```
2. Construye el entorno de pruebas y ejecuta la demo de una vez:
   ```bash
   bash pruebas/pruebas.sh
   ```
   (Si prefieres verlo paso a paso, dentro del contenedor: `bash demo.sh`. La demo **fabrica sus
   propios documentos** en la primera pasada: no necesitas traer ninguno.)

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base, dependencias fijadas y pesos descargados. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `scripts/generar_corpus.py` | Fabrica los documentos de prueba: PDFs que son imágenes, sin capa de texto, más la verdad exacta de cada uno. |
| `scripts/entorno.py` | Imprime con qué se ha hecho la prueba (versiones, sistema, CPUs). |
| `scripts/indexar.py` | Lee cada página con OCR y guarda el texto en una base de datos SQLite local. |
| `scripts/buscar.py` | Busca un texto en el índice y dice en qué fichero y en qué página está. |
| `scripts/comprobar.py` | Compara el texto leído por el OCR con la verdad exacta del corpus, campo a campo. |
| `scripts/limites.py` | Enseña dónde falla el OCR: un documento mal escaneado. |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |
| `documentos/` | **Generado por la demo**: los PDFs de prueba (cada uno es una imagen, sin capa de texto) y `factura_mal_escaneada.jpg`, el caso de límite. |
| `documentos_nuevos/` | **Generado**: la factura que llega después, para enseñar que el índice solo lee lo nuevo. |
| `ground_truth.json` | **Generado**: la verdad exacta de cada documento (referencia, importe, fecha y texto), contra la que se mide el OCR. |
| `documentos.db` | **Generado**: la base SQLite local con el texto leído; es el índice dentro del cual se busca. |
| `paquete.json` | La ficha del paquete para el índice del repositorio (título, vídeo, estado y si pide claves). |
| `.gitignore` | Deja fuera del repositorio lo que genera la propia demo (`documentos/`, `documentos_nuevos/`, `ground_truth.json`, `documentos.db`): se versiona el material, no sus resultados. |
| `.env.example` | Plantilla de variables de entorno. Este material **no necesita ninguna clave** (todo corre en local); se deja por coherencia con el resto del repositorio. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo, en
  ese orden. Si el vídeo hace algo que no está aquí, el material está mal.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial con
  la versión fijada (nada de `latest`, para que mañana funcione igual), instala lo que el material
  necesita con las versiones clavadas y deja los pesos del modelo dentro de la imagen.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en dos pasos: (1) construye la imagen de
  `entorno/Dockerfile`; (2) copia la carpeta a un directorio temporal dentro del contenedor y ejecuta
  ahí la demo, con la carpeta original montada en solo lectura. Si algo falla, para y lo dice. No
  escribe nada fuera del contenedor.
- **`scripts/generar_corpus.py`** — los documentos del vídeo son **inventados y se fabrican aquí**;
  no se ha usado ningún documento real. Cada factura sale como un PDF que es una imagen (por eso el
  PDF no tiene texto que buscar), y al lado se guarda `ground_truth.json` con los datos exactos de
  cada una, para poder medir cuánto acierta el OCR en vez de «mirar si parece bien».

## Resultado esperado
`demo.sh` termina con `== Fin de la demo ==` y `EXIT=0`. Estas son las líneas de una ejecución real
en un contenedor limpio (los tiempos cambian de una máquina a otra; el resto es igual). Se omiten los
avisos de las librerías de Paddle (`UserWarning: No ccache found`), que no son de la demo:

```
-- 3. El problema: ni el PDF ni la carpeta se pueden buscar -----------------
caracteres que saca pdftotext de una factura: 1
ficheros de la carpeta que contienen F-2026-0443 buscando texto: 0

-- 4. Índice: OCR de cada página a una base de datos local -------------------
Documentos en documentos/: 6
Por leer ahora: 6
Indice: 6 documentos, 7 paginas en total

-- 5. Llega una factura nueva: el índice lee SOLO lo que ha cambiado --------
Ya indexados (no se repiten): 6
Por leer ahora: 1
Documentos nuevos indexados: 1
Tiempo real de OCR: 73.5 s (73.5 s por pagina)
Indice: 7 documentos, 8 paginas en total

-- 6. La búsqueda que antes era imposible -----------------------------------
Busqueda: "F-2026-0443"   (paginas indexadas: 8)
   1 coincidencia(s):
   - factura_03_F-2026-0443.pdf  pagina 1

-- 7. Comprobación campo a campo contra la verdad del corpus -----------------
Documentos comprobados: 7
Campos comprobados:     26
Campos correctos:       26
Tasa de acierto:        100.0 %

-- 8. Dónde falla: un documento mal escaneado -------------------------------
Contra la verdad exacta del documento:
     numero: F-2026-0999    NO leido
   campos leidos: 0/4
```

Eso es el material entero en cuatro cifras: **1** carácter extraíble de un PDF escaneado, **6**
documentos leídos la primera vez y solo **1** la segunda (el índice es incremental), **26 campos de
26** correctos en los documentos legibles y **0 de 4** en el escaneo malo. Ningún número es una
impresión: todos salen de esta salida.

## Lo que este material NO demuestra
- **No es una herramienta terminada, es lo que enseña el vídeo.** El índice es didáctico: guarda el
  texto de cada página y busca dentro; no es un buscador semántico ni entiende de sinónimos.
- **El OCR se equivoca, y aquí se mide.** `scripts/comprobar.py` existe precisamente para publicar
  ese número en vez de esconderlo, y `scripts/limites.py` enseña un documento mal escaneado que el
  OCR lee mal.
- **Los documentos son inventados** (nombres, CIF y direcciones ficticios). No se ha usado ni una
  factura real: no podríamos publicarla, y tampoco la necesitas para probar esto.
- **Los tiempos son de una CPU concreta.** En tu máquina cambiarán: son el dato de la prueba, no una
  promesa de rendimiento.
- **No sustituye a un sistema de facturación.** No extrae importes con reglas de negocio propias,
  no valida contra tu contabilidad y no genera informes.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves. No se envía ningún documento a
ningún servidor; el OCR corre en tu máquina.

## Solución de problemas
- **«docker: command not found»**: te falta Docker; instálalo y vuelve a empezar.
- **«Cannot connect to the Docker daemon»**: arranca Docker (o tu motor remoto) y reinténtalo.
- **El paso 4 tarda mucho**: es normal la primera vez en una CPU modesta; mira el tiempo que imprime
  al terminar.
- **Resultados raros al buscar**: primero mira si el documento se leyó bien (paso 6); si el OCR falla,
  esa página no está bien en el índice.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.
