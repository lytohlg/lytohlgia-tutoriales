# imap_tools: convierte correos en tareas con Python

> Material del vídeo **imap_tools: convierte correos en tareas con Python** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Un buzón de correo que se lee solo: el script entra por IMAP, reconoce por el remitente qué correo es
cada cosa, le saca la fecha límite y te deja una **tarea con vencimiento** en una base de datos
SQLite. Y lo hace **sin duplicar**: si el mismo correo se procesa dos veces, la tarea ya estaba y no
se repite. Al final tienes una lista de lo que vence esta semana.

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
docker --context default build -t repro-correo-a-tareas:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-correo-a-tareas:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd correo-a-tareas
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
| `scripts/arrancar_buzon.sh` | Levanta el servidor de correo de pruebas (GreenMail) dentro del entorno. |
| `scripts/sembrar.py` | Envía tres correos al buzón de pruebas por SMTP (factura, presupuesto y publicidad). |
| `scripts/listar_buzon.py` | Lee la bandeja por IMAP: remitente, asunto, fecha, adjuntos y su contenido. |
| `scripts/reglas.py` | Reglas remitente→tarea, saca el vencimiento y guarda en SQLite sin duplicar. |
| `scripts/tareas.py` | Lista las tareas por fecha límite (`--semana`, `--vencidas`). |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (aquí ninguna: se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

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
Salida real de la última ejecución (recortada; es la que se ve en el vídeo):

```
-- 2. llegan tres correos: se envían de verdad por SMTP
  enviado  facturacion@example.com          Factura 2026-4471 - vence el 30/10/2026
  enviado  pedidos@example.org              Presupuesto 88-A - necesitamos respuesta antes...
  enviado  newsletter@example.net           Ofertas de la semana: tornilleria y abrasivos
3 correos entregados en el buzón compras@example.com (SMTP 127.0.0.1:3025)
...
-- 5. reglas: cada correo con regla se convierte en una tarea
correo  facturacion@example.com  |  Factura 2026-4471 - vence el 30/10/2026
        -> TAREA: Revisar y pagar la factura | tipo pago | vence 2026-10-30
correo  pedidos@example.org  |  Presupuesto 88-A - necesitamos respuesta antes del 22/10/2026
        -> TAREA: Responder al presupuesto | tipo respuesta | vence 2026-10-22
correo  newsletter@example.net  |  Ofertas de la semana: tornilleria y abrasivos
        -> sin regla: se queda en la entrada sin tocar

correos leidos: 3 | tareas nuevas: 2 | sin duplicar: 0 | sin regla: 1
tareas en la base de datos: 2

-- 6. la misma pasada otra vez: ni una tarea duplicada
        -> ya tenia tarea (mismo Message-ID): no se duplica      (x2)
correos leidos: 3 | tareas nuevas: 0 | sin duplicar: 2 | sin regla: 1

-- 8. qué toca esta semana
VENCE         DIAS  TIPO       TAREA
2026-10-22       7  respuesta  Responder al presupuesto
                               de pedidos@example.org
```

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
