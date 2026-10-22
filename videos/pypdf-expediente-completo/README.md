# pypdf: detecta PDFs faltantes antes de unir y cifrar

Viernes, seis de la tarde. Tienes que cerrar un expediente y mandarlo. El índice exige seis
documentos, en la carpeta hay cinco y uno de ellos llegó girado. Lo mandas igual, y dos días
después vuelve: «falta el certificado». Ese viaje de vuelta cuesta más que el documento que
faltaba, y casi siempre se cae por lo mismo: **no había ninguna comprobación antes de enviar**.

Este paquete hace esa comprobación, y además cierra el paquete: une los documentos **en el orden
del índice** (no en el orden alfabético de la carpeta), endereza lo que el escáner dejó girado,
numera las hojas, pone un marcador por documento y lo cifra con contraseña. Todo en local, con
`pypdf`, sin subir un solo PDF a ningún sitio.

Los datos de los documentos son **inventados**: no hace falta el documento de nadie para
demostrar esto.

## Qué vas a conseguir

- Un script que dice **NO** y explica por qué, antes de que el expediente salga de tu mesa.
- Un paquete de 9 páginas con los 6 documentos **en el orden del índice**, numerado y navegable.
- La certeza, comprobada con **otras herramientas** (qpdf, pdfinfo), de que está cifrado y de que
  no queda ninguna hoja girada.
- Saber qué **no** hace esto: no firma, no certifica validez legal y no lee escaneos sin OCR.

## Requisitos

- Python 3.11 o superior (probado con 3.12.15).
- `pypdf` 6.1.1 **con el extra `crypto`**: sin él, el cifrado AES-256 no funciona.
- `reportlab` 4.2.5, solo para generar los documentos de ejemplo y pintar el número de página.
- Opcional pero recomendado: `qpdf` y `poppler-utils` (`pdfinfo`, `pdftotext`) para verificar con
  una herramienta que **no** es la del vídeo.
- Nada de conexión a internet, ni cuentas, ni claves de API.

## Entorno de pruebas

El vídeo y estas pruebas se grabaron en **Docker**, sobre la imagen `python:3.12-slim`, con el
`Dockerfile` que está en `entorno/Dockerfile` (instala `qpdf`, `poppler-utils`, las fuentes
DejaVu y las dos bibliotecas de Python fijadas de versión). Hardware mínimo real: **1 GB de
memoria RAM y 1 CPU**; disco, menos de 500 MB para la imagen. El proceso completo tarda segundos:
lo más lento es instalar dependencias.

## Pasos

1. Instala las dependencias:

   ```bash
   pip install "pypdf[crypto]==6.1.1" reportlab==4.2.5
   ```

2. (Opcional, pero es lo que hace honesto el vídeo) instala los verificadores ajenos:

   ```bash
   sudo apt-get install -y qpdf poppler-utils
   ```

3. Ejecuta la demo entera, que es exactamente la secuencia del vídeo:

   ```bash
   bash demo.sh
   ```

   Si prefieres ir paso a paso, `demo.sh` está numerado del 0 al 8 y cada número es un comando
   que puedes copiar tal cual.

4. Lee la salida **antes** de fiarte: el paso 1 tiene que decir que **no se une** y el paso 5
   tiene que decir **VERIFICADO**. Si el paso 1 dijera que sí, tienes los seis documentos y no has
   reproducido el problema.

## Qué hace cada fichero

- `demo.sh` — la secuencia del vídeo, numerada del 0 al 8, con los mismos comandos y los mismos
  números. Es el punto de entrada: no hay nada más que ejecutar.
- `scripts/sembrar_expediente.py` — genera los PDF de ejemplo y el `indice.txt` (que es la única
  fuente del orden). Por defecto deja fuera `certificado_empresa.pdf`; con `--completo` lo añade.
- `scripts/comprobar.py` — la comprobación: por cada documento del índice mira si existe y si se
  puede abrir de verdad, avisa de las hojas giradas y sale con código distinto de 0 si el
  expediente no se puede cerrar.
- `scripts/unir.py` — une en el orden del índice, quita la marca de giro, añade un marcador por
  documento, numera las hojas y cifra con AES-256 leyendo la clave del entorno.
- `scripts/verificar.py` — la verificación: intenta abrir sin clave (tiene que fallar al leer las
  páginas), pregunta el algoritmo a `qpdf`, y con la clave comprueba páginas y marcadores.
- `scripts/manifiesto.py` — compara la página donde debería empezar cada documento (sumando el
  índice) con la página a la que apunta su marcador.
- `scripts/limites.py` — mide lo que se suele prometer de más: tiempo real, una hoja sin capa de
  texto y las tres cosas que este paquete no hace.
- `entorno/Dockerfile` — el entorno exacto de las pruebas (`python:3.12-slim` + las dependencias).
- `pruebas/pruebas.sh` — ejecuta `bash demo.sh` y comprueba que aparecen los números del vídeo.
- `.env.example` — la única variable de entorno (`EXPEDIENTE_CLAVE`) con un valor de ejemplo.
- `material.json` — la ficha pública del vídeo (título y fecha de estreno).

## Resultado esperado

Con el expediente incompleto:

```
presentes: 5 de 6 documentos | paginas: 8

EXPEDIENTE INCOMPLETO: no se une y no se entrega.
  falta: certificado_empresa.pdf (Certificado de empresa)
```

Con los seis documentos:

```
EXPEDIENTE COMPLETO: 6 documentos, 9 paginas. Se puede unir.
...
unidas 9 paginas de 6 documentos | hojas enderezadas: 1
escrito: salida/expediente_EXP-2026-0431.pdf (17.8 KB)
```

Y al final:

```
VERIFICADO: 6 documentos en el orden del indice, 9 paginas, cifrado AES-256, ninguna hoja girada
MANIFIESTO CUADRA: 6 documentos, 9 paginas, cada marcador en su pagina
```

## Coste y credenciales

Cero euros y cero cuentas: todo se ejecuta en tu máquina. La única «credencial» es la clave con
la que cifras el PDF, y la eliges tú. Tres cosas que conviene tener claras:

- Una contraseña escrita en la línea de comandos queda en el historial del terminal. En una
  variable de entorno, no.
- Si pierdes la clave, **ese PDF no se abre**: no hay teléfono al que llamar.
- `pypdf` es software libre con licencia BSD; `qpdf` y poppler también son libres.

## Solución de problemas

- **`FileNotDecryptedError` al leer las páginas**: es lo correcto si no has dado la clave. Si
  aparece con la clave puesta, la clave no es la del fichero: vuelve a generar el paquete.
- **`ModuleNotFoundError: cryptography`** o el cifrado falla: instalaste `pypdf` sin el extra.
  Usa `pip install "pypdf[crypto]"`.
- **`PdfStreamError` en la comprobación**: el PDF está cortado o corrupto (descarga a medias). Es
  justo el caso que el paso 2 de la demo provoca a propósito.
- **Un escaneo «no tiene texto»**: `pypdf` mueve páginas, no convierte píxeles en letras. Eso es
  OCR, y es otra herramienta.
- **El paquete se ve bien pero el cliente dice que falta un documento**: comprueba el `indice.txt`
  antes que la carpeta. El orden y la lista los manda el índice, no el nombre de los ficheros.
