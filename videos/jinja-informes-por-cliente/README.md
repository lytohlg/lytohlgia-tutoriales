# Jinja: el mismo informe para cada cliente sin copiar y pegar

> Material del vídeo **Jinja: el mismo informe para cada cliente sin copiar y pegar** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Generar el informe mensual de cada cliente desde sus datos con una sola plantilla y un solo script. Al final: tres informes correctos, con el nombre y las cifras de cada cliente, y un error claro si a un cliente le falta un dato.

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
docker --context default build -t repro-jinja-informes-por-cliente:local entorno
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
contenedor no dependa de nada de fuera. El contenedor no lleva credenciales dentro: las claves, si
el material las necesita, entran por variables de entorno.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd jinja-informes-por-cliente
   ```
2. Prepara tus variables de entorno (nunca escribas claves dentro de un script):
   ```bash
   cp .env.example .env
   # edita .env con tu editor y rellena los valores
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |
| `datos/clientes.csv` | Los datos de los tres clientes del ejemplo (nombre, contacto, concepto, horas y precio/hora). Es la única fuente de verdad del informe: si un nombre está mal aquí, está mal en el informe. |
| `datos/clientes_con_descuento.csv` | Los mismos clientes **con** una columna extra `descuento`. Sirve para lo contrario: cuando el dato existe, la plantilla que lo pide lo imprime. |
| `datos/clientes_inyectado.csv` | El mismo CSV, pero el nombre de un cliente trae una etiqueta HTML dentro (`<b>Aurora</b>`). Se usa solo para la prueba del escape: el mismo dato, dos plantillas, dos resultados opuestos. |
| `plantilla/informe.html` | La plantilla del informe (Jinja). Tiene el texto fijo y los huecos `{{ … }}` y `{% … %}`; no sabe de ningún cliente concreto. |
| `plantilla/base.html` | La plantilla base: la cabecera y el pie que comparten todos los informes. No se renderiza sola; la usan las que la extienden. |
| `plantilla/informe_extiende.html` | La misma idea que `informe.html`, pero con `{% extends "base.html" %}`: hereda la cabecera y solo escribe lo que cambia. Así no se repite el encabezado en cada informe. |
| `plantilla/informe_safe.html` | La plantilla que imprime el nombre con el filtro `safe`, es decir, sin escapar. Con `clientes_inyectado.csv` se ve el peligro: el `<b>` entra como HTML de verdad en vez de como texto. |
| `plantilla/informe_descuento.html` | La misma plantilla con una línea más que pide `cliente.descuento`. Es la que enseña qué pasa cuando la plantilla pide un dato que los datos no traen. |
| `generar.py` | El programa: lee el CSV, agrupa las líneas por cliente, renderiza la plantilla y escribe un HTML por cliente. |
| `revisar.py` | La comprobación del resultado (no del «terminó sin error»): que cada informe lleva su nombre, que no aparece ningún otro cliente y que el total impreso coincide con el recalculado desde el CSV. |
| `gen_clientes.py` | Genera un CSV con 100 clientes inventados para ver que el mismo código escala sin tocarlo. |

### Qué hace cada script, paso a paso
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
Tres informes (`informes/informe_panaderia_aurora.html`, `informe_talleres_bravo.html` e
`informe_ferreteria_la_clave_hijos.html`), cada uno con el nombre de su cliente, su tabla de conceptos
y su total. La comprobación imprime `3/3 informes correctos · nombres cruzados: 0`. Después, la
plantilla que pide un `descuento`: con datos que lo traen, sale la línea; con datos que no lo traen, con
`StrictUndefined` el programa se para y nombra el campo que falta, y sin él los tres informes se
escriben igual **sin** la línea del descuento — el fallo silencioso. Al final, 100 clientes con el mismo
código.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
