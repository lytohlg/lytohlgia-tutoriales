# SQL Explorer: que el informe de excepciones te llegue solo

> Material del vídeo **SQL Explorer: que el informe de excepciones te llegue solo** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Dejar GUARDADA una consulta de excepciones (pedidos con la entrega pasada y sin servir,
facturas vencidas sin cobrar) dentro de **SQL Explorer** y que el informe llegue solo al
correo, sin abrir la base de datos a buscarlo. En el vídeo se hace de verdad, paso a paso:
se guarda la consulta, se ejecuta con el motor de la propia herramienta, sale el correo y
se lee el correo recibido.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor
  (la imagen de la demo ocupa unos 430 MB; la prueba se hizo en un contenedor de 1 CPU).
- Con menos va igual, pero lento.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar las imágenes base).

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
docker --context default build -t sqlexplorer-demo:v1 entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" sqlexplorer-demo:v1 bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno. **Este material no
necesita red**: el correo de pruebas y el S3 de pruebas son dos servidores locales que se levantan
dentro del propio contenedor, así que se puede ejecutar con `--network=none` y funciona igual.

**Detalles de nuestra ejecución, por si tu caso es distinto:** las órdenes de arriba son las mismas
que usamos nosotros, tal cual. El `--context default` fuerza el motor Docker local — útil si tienes
configurado además uno remoto; si en tu equipo solo hay uno, déjalo igual (funciona) o quítalo.
Ejecutamos con el usuario `1000:1000` para no correr como root y con `HOME=/tmp` para que el
contenedor no dependa de nada de fuera. El contenedor no lleva credenciales dentro: las claves, si
el material las necesita, entran por variables de entorno.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd informes-excepciones-por-correo
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
| `excepciones.sql` | La consulta de excepciones que se guarda en SQL Explorer. |
| `scripts/` | Los seis pasos, uno por script (ver la tabla de abajo). |
| `proyecto/` | El proyecto Django mínimo donde vive la herramienta (no se instala una librería suelta). |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
- **`scripts/entorno.py`** — crea las tablas de la herramienta con `migrate` (como en cualquier
  proyecto Django) y enseña las versiones con las que se está trabajando.
- **`scripts/arrancar_servicios.sh` + `scripts/servicios.py`** — levantan los dos servidores de
  pruebas dentro del contenedor: el correo (SMTP real) y el S3 local donde la herramienta publica el
  informe. Si ya estaban levantados, no los duplica.
- **`scripts/sembrar.py`** — crea `empresa.db` con los pedidos y las facturas de ejemplo, con fechas
  **relativas a hoy**, y dice cuántas filas entran.
- **`scripts/crear_consulta.py`** — da de alta la consulta guardada dentro de SQL Explorer (título +
  SQL + a qué base apunta), por el camino de la aplicación, y comprueba que quedó en su tabla.
- **`scripts/ejecutar_consulta.py`** — ejecuta ESA consulta guardada con el motor de la herramienta
  (no un `SELECT` suelto) y muestra las excepciones y el apunte en su histórico.
- **`scripts/enviar_alerta.py`** — dispara el envío por correo de esa consulta por la ruta real de
  la herramienta y dice qué tarea se ha encargado del envío.
- **`scripts/leer_correo.py`** — lee el buzón de pruebas por su API, saca el asunto y el cuerpo del
  informe y **descarga el enlace** que viene dentro, para enseñar lo que ha llegado.
- **`scripts/estado_alertas.py`** — enseña el histórico de ejecuciones y vuelve a lanzar el envío
  para contar lo que pasa de verdad la segunda vez.
- **`scripts/arranque.py`** — dos líneas de fontanería que usan todos los pasos: pone el proyecto
  en el `sys.path` y prepara Django antes de tocar la base de datos.
- **`proyecto/`** — el proyecto Django, que es lo que deja claro que SQL Explorer es una app de
  Django y no un programa de consola: `proyecto/manage.py` (el lanzador de siempre), `settings.py`
  (correo, base de datos y SQL Explorer), `urls.py`, `celery.py` y `proyecto/informes/__init__.py`.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial
  con la versión fijada (nada de `latest`, para que mañana funcione igual), instala lo que el
  material necesita y deja el directorio de trabajo preparado. No copia claves ni tus datos: eso
  entra después, por variables de entorno y solo si tú las pones.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en dos pasos: (1) construye la imagen desde
  `entorno/Dockerfile`; (2) la ejecuta con la carpeta montada en solo lectura y una copia de trabajo
  en `/tmp`, y para si algo falla. Si termina bien, tu copia funciona igual que la del vídeo: compara
  su salida con la de «Resultado esperado» (arriba) y verás que cuadra. No escribe nada fuera del
  contenedor.
- **`.env.example`** — la lista de claves que el material espera, con valores de mentira y el
  nombre exacto de cada variable. Se copia a `.env`; `.env` está en `.gitignore` y nunca se sube.

## Resultado esperado
Esto es la salida **real** de `bash demo.sh` en un contenedor limpio (las fechas se calculan solas a
partir de hoy, así que los días cambian; el resto es igual):

```
== SQL Explorer: el informe de excepciones te llega solo ==

-- 1. el entorno: Django + SQL Explorer, y los servidores de prueba
entorno de la demo
  python            3.12.15
  django            5.2.18
  sql explorer      django-sql-explorer 5.3  (app de django)
  base de la app    explorer.db   (18 tablas de la herramienta)
  datos del negocio empresa.db    (la siembra los crea en el paso 2)
servidores de prueba listos: correo SMTP 127.0.0.1:1025 (API 8025) | s3 127.0.0.1:5000 (bucket informes)

-- 2. la siembra: pedidos y facturas con datos realistas
empresa.db sembrada (fechas relativas a hoy)
  pedidos    7 filas
  facturas   5 filas
  total      12 filas

-- 3. la consulta de excepciones queda GUARDADA en SQL Explorer
consulta guardada dentro de SQL Explorer
  id        1
  titulo    Excepciones: pedidos sin servir y facturas vencidas
  conexion  empresa  (la base de los datos)
  tabla     explorer_query        <- la de la propia herramienta
  estado    guardada (1 consulta(s) en la tabla)

-- 4. se ejecuta la consulta guardada (con el motor de la herramienta)
consulta: Excepciones: pedidos sin servir y facturas vencidas  (id 1)
excepciones encontradas: 5

REFERENCIA   CLIENTE            VENCE       IMPORTE  EXCEPCION
1001         Ferreteria Vega    2026-10-04  1284.50  pedido sin servir
F-2026-0441  Ferreteria Vega    2026-10-07  1284.50  factura vencida sin cobrar
1002         Talleres Rios      2026-10-10  640.00   pedido sin servir
F-2026-0455  Talleres Rios      2026-10-13  640.00   factura vencida sin cobrar
1003         Suministros Norte  2026-10-14  298.75   pedido sin servir

la herramienta lo ha apuntado en su historico (explorer_querylog): ejecucion #1, 1 ms, correcta=si

-- 5. la alerta: el informe sale por correo y se lee el correo recibido
alerta lanzada: el informe se manda por correo
  consulta   Excepciones: pedidos sin servir y facturas vencidas
  ruta       explorer/1/email_csv   <- el boton de correo de SQL Explorer
  destino    operaciones@example.com
  respuesta  200 {"message": "message was sent successfully"}
  tarea      explorer.tasks.execute_query (la cola de la herramienta)
buzon de pruebas (127.0.0.1:1025): 2 correo(s) recibido(s)

[1] asunto : [SQL Explorer] Your query is running...
    de     : informes@example.com
    para   : operaciones@example.com
[2] asunto : [SQL Explorer] Report "Excepciones: pedidos sin servir y facturas vencidas" is ready
    de     : informes@example.com
    para   : operaciones@example.com

informe recibido: [SQL Explorer] Report "Excepciones: pedidos sin servir y facturas vencidas" is ready
enlace del propio correo: http://127.0.0.1:5000/informes/NWK2M5DGRY5S9NERY5FH.csv?X-Am...
informe descargado: 5 excepciones

  referencia,cliente,vence,importe,excepcion
  1001,Ferreteria Vega,2026-10-04,1284.5,pedido sin servir
  F-2026-0441,Ferreteria Vega,2026-10-07,1284.5,factura vencida sin cobrar
  1002,Talleres Rios,2026-10-10,640.0,pedido sin servir
  F-2026-0455,Talleres Rios,2026-10-13,640.0,factura vencida sin cobrar
  1003,Suministros Norte,2026-10-14,298.75,pedido sin servir

-- 6. estado: histórico de la consulta y qué pasa si vuelve a lanzarse
historico de la consulta (tabla explorer_querylog, de la herramienta)
  #1  2026-10-16 00:17:13  ok  0 ms

correos en el buzon antes de la segunda pasada: 2
correos en el buzon despues de la segunda pasada: 4

la herramienta ha vuelto a mandar el informe (2 correos):
  no lleva control de duplicados; la frecuencia la pone quien la programa.
  su enganche periodico propio es explorer.tasks.snapshot_queries (celery beat).
```

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves. El correo de pruebas y el S3 de
pruebas se levantan dentro del contenedor y no salen de tu máquina; los destinatarios del ejemplo son
direcciones inventadas (`example.com`), que no existen.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- **El correo no llega**: mira el buzón de pruebas en `http://127.0.0.1:8025` (si ejecutas la demo
  sin publicar el puerto, usa la API, que es lo que hace `scripts/leer_correo.py`).
- **El enlace del correo no descarga**: es una URL firmada temporal (va con `X-Amz-Expires`); si la
  abres mucho más tarde, vuelve a lanzar el aviso y tendrás un enlace nuevo. La ruta existe y se
  probó; no es un fallo del material.
- **La consulta falla con «unsupported operand type(s) for +»**: en un `UNION ALL` no mezcles
  números y textos en la misma columna. SQL Explorer resume las columnas numéricas y, si mezclas,
  se cae. En este material la referencia va como texto (mira `excepciones.sql`).
- **Aviso de `musl` al construir**: MailHog se distribuye para Alpine; su binario necesita la libc
  de musl. Por eso `entorno/Dockerfile` instala `musl` en la imagen de Debian antes de copiarlo.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

### Lo que este material NO promete
- SQL Explorer **no** trae un planificador de alertas propio: envía cuando se dispara el envío (a
  mano o desde un cron o un servicio tuyo). Lo que sí programa por sí mismo es
  `snapshot_queries`, que guarda una foto de los resultados.
- No hay control de duplicados: dos envíos son dos correos. La frecuencia la pones tú.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
