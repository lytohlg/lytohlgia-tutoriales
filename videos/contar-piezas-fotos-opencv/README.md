# OpenCV en Python: contar piezas en una foto y que el número cuadre

> Material del vídeo **OpenCV en Python: contar piezas en una foto y que el número cuadre** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Contar piezas en fotos de bandejas con OpenCV puro (sin modelos de IA, sin servicios de pago) y
comprobar que el número cuadra: 12 fotos, 47 piezas, 12 de 12 fotos bien contadas. El programa deja
un `informe.csv` con una fila por foto y una copia de cada foto con las piezas numeradas, para
revisarlo a ojo.

El detalle que hace que esto no sea un juguete: cuando dos piezas se tocan, el contorno las ve como
**una sola**. El material incluye la versión ingenua (que falla, y se ve fallar) y la versión con
transformada de distancia + watershed (que acierta). Verás el antes y el después con los mismos datos.

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
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada
  (`opencv-python-headless==4.10.0.84`, `numpy==2.1.3`).
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de las claves que necesite el material. Aquí no hay ninguna: el fichero
  está vacío a propósito y se queda como ejemplo de lo que **no** hace falta.

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno (basta con `docker compose up`).

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base):
```bash
docker --context default build -t repro-contar-piezas-fotos-opencv:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" python:3.12-slim bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
contenedor no dependa de nada de fuera. El contenedor no lleva credenciales dentro (aquí no hay
ninguna que meter).

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd contar-piezas-fotos-opencv
   ```
2. Si vas a ejecutarlo **fuera de Docker**, instala las dos dependencias (son las mismas versiones
   que fija el Dockerfile, para que el resultado sea el mismo):
   ```bash
   pip install opencv-python-headless==4.10.0.84 numpy==2.1.3
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `contar.py` | El contador: lee las fotos de una carpeta y escribe el número de piezas de cada una. Tiene dos modos (contornos y watershed) y saca `informe.csv` + las fotos marcadas. |
| `generar_fotos.py` | Fabrica las fotos de prueba y su `manifiesto.csv` con las piezas que hay de verdad. Sin verdad conocida no se puede decir si el contador acierta. |
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (aquí, ninguna: se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`contar.py`** — el corazón del material. Hace cuatro cosas, en este orden:
  1. Pasa la foto a gris y la separa en «pieza» y «bandeja» con el umbral de Otsu, que se calcula
     solo a partir del histograma (no hay que elegir un número a mano).
  2. Limpia el ruido con una apertura de 3×3 y descarta lo que no puede ser una pieza: menos de
     400 px² (ruido) o más de un cuarto de la foto (eso es el fondo de la bandeja).
  3. **Modo contornos** (`por defecto`): cuenta los contornos exteriores que quedan. Es rápido y
     falla en un caso concreto: dos piezas que se tocan forman **un solo** contorno.
  4. **Modo `--separar-tocadas`**: calcula la transformada de distancia (cuánto está cada píxel del
     borde), toma los máximos locales como semilla de cada pieza y reparte el resto con watershed.
     Cuando dos piezas se tocan, cada una conserva su centro, así que cada una se lleva su trozo.
  Opciones: `--carpeta` o `--foto`, `--salida informe.csv`, `--marcadas carpeta/` (fotos con las
  piezas numeradas) y `--verdad manifiesto.csv` (compara con lo que hay de verdad y te dice si cuadra).
- **`generar_fotos.py`** — dibuja bandejas de 800×600 con piezas de radio 26 px, algunas en grupos
  que se solapan, una bandeja vacía (`p06`) y anota en `manifiesto.csv` cuántas piezas hay en cada
  foto. Todo sale de una semilla fija (`20261118`), así que las fotos son siempre las mismas: si
  alguien obtiene otro número, es que cambió el código, no la suerte. Opciones: `--salida`,
  `--solape` (cuánto se pisan dos piezas, 0,30 por defecto) y `--solo` (generar solo algunas fotos).
  **Por qué fotos sintéticas**: con fotos reales no sabes la respuesta sin contarlas a mano, que es
  justo lo que quieres evitar. Sin verdad conocida, un contador que se equivoca parece que acierta.
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
  nombre exacto de cada variable. Se copia a `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado
Con el modo por defecto (contornos) el material **no cuadra**, y eso es parte de la lección:

```
12 fotos · contadas 39 · de verdad 47 · acertadas 8/12
TOTAL NO CUADRA: 39 != 47
```

Con `--separar-tocadas` (watershed) sí:

```
12 fotos · contadas 47 · de verdad 47 · acertadas 12/12
TOTAL OK: el recuento cuadra con el manifiesto
```

Las fotos que fallan en modo contornos son las que tienen grupos que se tocan (`p03`, `p05`, `p08`,
`p10`): el contador pierde 1, 2, 2 y 3 piezas respectivamente. Si tus números no son estos, mira la
sección siguiente: casi siempre es que se está ejecutando otro código o otra semilla.

## Cuándo esto sirve y cuándo no
Está pensado para **piezas parecidas en una bandeja plana, vistas desde arriba y con contraste
claro** (piezas oscuras sobre fondo claro, o al revés). Lo que no hace, y conviene saberlo antes de
usarlo:

- **El umbral es global (Otsu).** Si la mitad de la foto está a la sombra, ese lado se separa mal:
  no hay corrección de iluminación ni umbral adaptativo. Es la primera mejora que pediría el cuerpo.
- **El tamaño de pieza se supone parecido.** El corte de semillas usa el radio más grande de la
  foto (`0.4 ×` el máximo de la transformada de distancia), así que una pieza mucho más pequeña que
  las demás puede quedarse sin semilla y no contarse.
- **Perspectiva.** Las fotos de prueba son ortogonales; una bandeja fotografiada en escorzo hace
  elipses y el radio deja de ser constante. Habría que corregir la perspectiva primero.
- **Piezas partidas o con agujeros.** El filtro de área (más de 400 px²) puede descartar trozos
  pequeños legítimos si lo que cuentas son fragmentos.
- **Lo que no hay aquí**: ni aprendizaje profundo, ni segmentación entrenada, ni lectura de códigos.
  Es OpenCV clásico, y por eso es gratis, rápido y explicable línea a línea. Cuando el fondo es
  sucio de verdad, el siguiente escalón es un modelo, y eso ya es otro vídeo.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **`ModuleNotFoundError: cv2`**: te falta `pip install opencv-python-headless` (o estás fuera del
  contenedor, que ya lo trae).
- **Números distintos a los del vídeo**: comprueba que `contar.py` y `generar_fotos.py` son los de
  esta carpeta y que no has tocado `SEMILLA`.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
