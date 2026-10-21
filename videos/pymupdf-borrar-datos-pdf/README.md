# PyMuPDF: borra el texto privado de un PDF de verdad

Un PDF que mandas por correo con el DNI tapado con un rectángulo negro **sigue llevando el DNI
dentro**. El rectángulo se dibuja *encima* del texto: el texto sigue en el fichero y lo pude
recuperar tanto con PyMuPDF como con `pdftotext`. Este paquete demuestra el problema, lo arregla
con PyMuPDF (redacción real: el texto se elimina, no se tapa) y comprueba el resultado con **otra**
herramienta, `pdftotext`, además de mirar los píxeles de la zona.

Todo ocurre en tu ordenador: ni el documento ni los datos salen a ningún servicio.

> **Alcance (léelo antes de usar esto con documentos reales).** Este material demuestra redacción
> de texto y verificación sobre documentos sintéticos cuyos datos conocemos. **No garantiza la
> eliminación de todos los datos sensibles de un PDF cualquiera.** Antes de compartir un documento
> real, revisa a mano imágenes, campos de formulario, anotaciones, adjuntos, firmas y metadatos.

## Qué vas a conseguir

- Distinguir «tapar» de «redactar» con una prueba que se ve en pantalla, no con una opinión.
- Redactar datos personales en un PDF y **comprobarlo** contra una lista cerrada de secretos
  sembrados (no contra el contador del propio script, que puede mentir).
- Ver por qué un patrón incompleto deja fugas: el mismo lote con dos versiones del patrón.
- Conocer los dos límites que rompen el juguete: PDF escaneado (sin capa de texto) y campos de
  formulario (los valores viven en la ficha del campo, no en el texto de la página).

## Requisitos

- Python 3.11 o superior y PyMuPDF (`pip install pymupdf`). El paquete fija `pymupdf==1.26.5`.
- `pdftotext` (paquete `poppler-utils`) para la comprobación independiente.
- Nada de cuenta, nada de nube, ningún documento real: los PDF de entrada **los genera el propio
  script** con datos inventados.

## Entorno de pruebas

La demo del vídeo se ejecutó en un contenedor Docker construido con `entorno/Dockerfile`
(base `python:3.11-slim`, `poppler-utils` y `pymupdf==1.26.5`). Hardware mínimo: 1 CPU, 512 MB de
RAM y 200 MB de disco; el contenedor no necesita más porque no procesa escaneos grandes.

Construir y entrar:

```bash
docker build -t pymupdf-demo:1 entorno
docker run --rm -it -v "$PWD":/trabajo -w /trabajo pymupdf-demo:1 bash
```

Y dentro, `bash demo.sh`.

## Pasos

1. `python3 scripts/sembrar_docs.py` — genera cuatro PDF con datos inventados y la lista exacta de
   lo sembrado (`datos_conocidos.txt`). Esa lista es la verdad de referencia de todas las pruebas.
2. `python3 scripts/estado.py entrada` — cuántos datos personales localiza el extractor en cada uno.
3. `python3 scripts/censura_falsa.py` — dibuja un rectángulo negro sobre el DNI y guarda el fichero.
4. `pdftotext censura_falsa.pdf -` — el DNI sigue ahí, en el texto extraído.
5. `python3 scripts/censura_real.py` — marca la zona con `add_redact_annot` y la aplica con
   `apply_redactions()`; después cuenta apariciones en el fichero guardado y píxeles claros dentro
   de la zona.
6. `python3 scripts/lote.py v1` y `python3 scripts/verificar.py salida_v1` — la carpeta entera con un
   patrón ingenuo: aparece una fuga real.
7. `python3 scripts/lote.py v2` y `python3 scripts/verificar.py salida_v2` — el patrón completo: cero.
8. `python3 scripts/metadatos.py` — la ficha del fichero (autor, asunto, productor).
9. `python3 scripts/limites.py` — un escaneo: para el script, «este documento no tiene datos».
10. `python3 scripts/formulario.py` y `python3 scripts/campos.py` — los campos rellenables sobreviven
    a la redacción de la página.

## Qué hace cada fichero

- `scripts/sembrar_docs.py` — crea los PDF de entrada y `datos_conocidos.txt`.
- `scripts/patrones.py` — los patrones v1 (ingenuo) y v2 (con el DNI con puntos) y `buscar()`.
- `scripts/estado.py` — cuenta datos localizados por documento.
- `scripts/censura_falsa.py` — el error: rectángulo encima del texto.
- `scripts/censura_real.py` — la redacción de verdad, con comprobación de píxeles.
- `scripts/lote.py` — redacta una carpeta entera y separa «detectados» de «redactados».
- `scripts/verificar.py` — verificación independiente contra los secretos sembrados, en texto y en
  bytes crudos.
- `scripts/metadatos.py` — borra la ficha del documento (`set_metadata({})` + `del_xml_metadata()`).
- `scripts/formulario.py` / `scripts/campos.py` — el límite de los campos de formulario.
- `scripts/limites.py` — el límite del PDF escaneado (imagen sin capa de texto).
- `scripts/datos.py` — los datos inventados, en un único sitio: cámbialos aquí y en ningún otro.
- `.env.example` — deja explícito que este paquete **no necesita ninguna clave ni variable de
  entorno**; existe solo para que no haya dudas al revisar el repositorio. No hay que copiarlo
  ni rellenarlo para que la demo funcione.
- `demo.sh` — todos los pasos en orden. `pruebas/pruebas.sh` — ejecuta `bash demo.sh` y comprueba
  los números.

## Resultado esperado

Al final de `bash demo.sh`:

```
datos personales localizados en total: 13
veces que el DNI sigue apareciendo en el texto: 1
zonas marcadas para redactar: 1
veces que el DNI aparece en el texto guardado: 0
píxeles claros dentro de la zona redactada: 0 de 3861
datos detectados: 13 | zonas redactadas: 13
datos detectados: 14 | zonas redactadas: 14
TOTAL de secretos que siguen en los documentos: 1   (con el patrón v1)
TOTAL de secretos que siguen en los documentos: 0   (con el patrón v2)
campos con datos del autor que quedan: 0
escaneo: caracteres de texto = 0 | zonas encontradas del DNI = 0
```

`pruebas/pruebas.sh` falla si alguno de esos números cambia.

`pruebas/pruebas.sh` comprueba **diez cadenas** de esta salida; los **secretos** son **siete**
(`datos_conocidos.txt`). No es lo mismo: una misma cadena puede aparecer en varias líneas y un
secreto puede comprobarse en dos sitios (texto visible y bytes crudos del fichero).

## Coste y credenciales

Coste cero: es una biblioteca local (PyMuPDF, licencia AGPL-3.0, https://github.com/pymupdf/PyMuPDF).
No hay claves, ni API, ni cuentas. `requiere_credenciales: false` en el manifiesto.

## Solución de problemas

- **`ModuleNotFoundError: fitz`** — instala `pymupdf` (el import se llama `fitz`).
- **`pdftotext: command not found`** — instala `poppler-utils`; sin él pierdes la comprobación
  independiente (y el vídeo insiste en que no te fíes de una sola herramienta).
- **Redacto y el dato sigue apareciendo** — suele ser un patrón incompleto (mira la fuga del paso 6)
  o un dato que está en un campo de formulario o en los metadatos, no en el texto.
- **Un PDF escaneado sale «limpio» sin haber hecho nada** — no tiene capa de texto: primero hay que
  pasarlo por OCR y después redactar.
- **La zona queda gris en vez de negra** — usa `fill` en `add_redact_annot` y comprueba los píxeles,
  no solo el texto.
