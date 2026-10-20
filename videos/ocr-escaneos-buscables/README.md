# OCRmyPDF: convierte un PDF escaneado en texto que se puede buscar

> Material del vídeo **OCRmyPDF: convierte un PDF escaneado en texto que se puede buscar** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

El escáner no guarda texto: guarda una foto del papel. Para un ordenador, un PDF escaneado es un montón de píxeles, así que no se puede buscar dentro, ni copiar un importe, ni archivar un documento por lo que dice. Con doscientos contratos escaneados, encontrar el que habla del alquiler significa abrirlos uno a uno.

Esto lo arregla el OCR: un programa mira la imagen, reconoce las letras y pega el texto **debajo** de la imagen, en una capa invisible. El documento sigue pareciendo el mismo papel y a partir de ahí se puede buscar dentro.

## Qué vas a conseguir

Tres PDF escaneados de verdad (imagen, sin una sola letra de texto) que, al terminar, tienen una capa de texto buscable: los 502 caracteres del contrato de alquiler se pueden buscar con `grep` y encontrar la cláusula de la renta y el importe. Y un script de 20 líneas que, dada una frase, dice en qué PDF de una carpeta está.

Resultados medidos en este entorno (los mismos del vídeo):

- Antes del OCR: **0 caracteres** en los tres documentos.
- Después: **502** en el contrato, **388** en la factura, **468** en el acta.
- Unos **3 segundos por página** y unos **5 KB más** por documento.
- Repetir el comando con `--skip-text` no cambia nada: **508 caracteres antes y 508 después**.

## Requisitos

**Software**

- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes: https://docs.docker.com/get-docker/
- Nada de Python en tu máquina: todo corre dentro del contenedor.

**Hardware** (mínimo para el entorno de pruebas)

- 2 GB de RAM libres, 1 CPU y 2 GB de disco libre para la imagen del contenedor.
- El OCR es de CPU, no de tarjeta gráfica: no hace falta GPU.

Si quieres usarlo fuera de Docker: `ocrmypdf` y el paquete de español de `tesseract` (`sudo apt install ocrmypdf tesseract-ocr-spa` en Debian/Ubuntu, `brew install ocrmypdf tesseract-lang` en macOS).

## Entorno de pruebas

Todo se prueba en **Docker**, con la imagen que construye **`entorno/Dockerfile`** (base `python:3.11-slim`): dentro van `ocrmypdf` 16.10.4, `tesseract` con el idioma español, `poppler-utils` (que trae `pdftotext`), `ghostscript`, `qpdf` y las fuentes DejaVu con las que se dibujan los PDF de prueba.

```bash
docker build -t ocr-escaneos ./entorno
```

Las versiones están fijadas en el `Dockerfile` a propósito: si un día el OCR cambia de comportamiento, sabes con cuál se hizo el vídeo.

## Pasos

1. Construye el entorno (una vez, tarda un par de minutos):

   ```bash
   docker build -t ocr-escaneos ./entorno
   ```

2. Ejecuta la demo completa dentro del contenedor, con esta carpeta montada:

   ```bash
   docker run --rm -v "$PWD":/trabajo:ro --workdir /tmp ocr-escaneos \
     bash -lc 'cp -r /trabajo /tmp/repro && cd /tmp/repro && bash demo.sh'
   ```

3. Para hacerlo a mano, paso a paso, dentro de ese mismo contenedor:

   ```bash
   bash scripts/ocr_uno.sh contrato_alquiler.pdf          # un documento
   bash scripts/ocr_lote.sh                               # la carpeta entera
   bash scripts/buscar.sh "renta mensual" salida          # buscar dentro
   ```

4. La prueba automática del paquete (hace todo lo anterior y comprueba el resultado):

   ```bash
   bash pruebas/pruebas.sh
   ```

## Qué hace cada fichero

- **`demo.sh`** — la secuencia del vídeo, en orden: sembrar, medir antes, hacer OCR, medir después, buscar, repetir con `--skip-text` y enseñar el límite.
- **`scripts/sembrar_escaneos.py`** — fabrica los tres PDF escaneados (imagen, sin texto) con semilla fija, para que salgan iguales siempre.
- **`scripts/estado.py`** — cuenta los caracteres que `pdftotext` saca de cada PDF: la prueba de que antes no había texto y después sí.
- **`scripts/ocr_uno.sh`** — el comando del vídeo sobre un solo documento, con bytes y segundos.
- **`scripts/ocr_lote.sh`** — el mismo comando sobre toda la carpeta `entrada/`, una línea por documento y un total.
- **`scripts/buscar.sh`** — busca una frase dentro de todos los PDF de una carpeta y dice en cuál está.
- **`scripts/limite.py`** — el lado incómodo: degrada el contrato al 35% y al 22% de resolución y mide qué lee el OCR en cada caso.
- **`pruebas/pruebas.sh`** — ejecuta `bash demo.sh` y comprueba que los resultados aparecen.
- **`entorno/Dockerfile`** — el entorno con las versiones fijas.
- **`paquete.json`** — manifiesto del paquete: comando, prueba, fecha de publicación, salida esperada.
- **`.env.example`** — no hay nada que configurar: este material no usa credenciales ni variables de entorno.

## Resultado esperado

Al final de `demo.sh` tienes que ver, entre otras líneas:

```
documentos: 3 | sin capa de texto: 3      <- antes
documentos procesados: 3                  <- el OCR
documentos: 3 | sin capa de texto: 0      <- después
ENCONTRADO en contrato_alquiler_ocr.pdf
   CLÁUSULA SEPTIMA. La renta mensual se fija en 780 euros,
caracteres antes: 508 | después de repetir el comando: 508
```

Y en el último paso, el límite medido: al 35% de resolución el OCR devuelve texto casi correcto pero se le escapa una letra («cada mos» en vez de «cada mes»); al 22% devuelve texto ilegible (el número de documento sale con cifras cambiadas). **En los dos casos el comando termina con código 0: no avisa de que se ha equivocado.**

## Coste / credenciales

- **Credenciales: ninguna.** No hay claves, ni API, ni cuenta que crear. Todo ocurre en local.
- **Coste: 0 €.** El OCR corre en tu máquina, con `tesseract`, que es software libre.
- **Tiempo:** unos 3 segundos por página. Cuatrocientas páginas son entre 20 y 30 minutos, una sola vez.

## Solución de problemas

- **«`ocrmypdf` no encuentra el idioma»** — falta `tesseract-ocr-spa`. Sin él, las tildes y las eñes salen mal, y peor: la búsqueda con tilde deja de encontrar el texto.
- **«El PDF de salida sigue sin texto»** — mira el código de salida de `ocrmypdf` y la calidad del escaneo: por debajo de una resolución mínima el OCR no añade capa. Empieza por `python3 scripts/estado.py` sobre la carpeta de salida.
- **«La búsqueda no encuentra lo que veo en el documento»** — el OCR ha leído otra cosa. Compara el texto extraído con la imagen; es el fallo típico de un escaneo torcido o con poca luz.
- **«`ocrmypdf` se queja de las páginas que ya tienen texto»** — usa `--skip-text`, que es lo que hace el paso 9 de la demo.
- **«Docker no arranca el contenedor»** — comprueba `docker run --rm hello-world`; si eso falla, el problema es de Docker, no del paquete.
