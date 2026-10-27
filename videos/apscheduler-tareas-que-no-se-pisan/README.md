# APScheduler: que tu script se ejecute solo y no se pise

> Material del vídeo **APScheduler: que tu script se ejecute solo y no se pise** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Tienes un script que tiene que correr todos los días a las ocho: el informe de ventas, la copia de
seguridad, el correo con el resumen. Y tú no estás delante a las ocho.

Hoy lo resuelves de tres maneras, y las tres te han fallado alguna vez:

- **A mano**: te acuerdas, lo lanzas, y el día que no te acuerdas el informe no existe. Lo descubres
  el lunes, cuando alguien lo pide.
- **Con cron**: funciona hasta que dos copias se solapan porque la tarea anterior tardó más de lo
  normal. Entonces el fichero sale con el doble de filas, o a medias.
- **Con un `while True` y un `sleep`**: el proceso se queda despierto, y si reinicias el servidor la
  agenda desaparece sin que nadie te avise.

El coste no es el rato de programarlo: es el informe que falta el día que hay reunión, y las horas
que pierdes averiguando si el problema fue la tarea, el solape o el reinicio.

## Qué vas a conseguir

Un script que se ejecuta a su hora sin nadie delante, que **rechaza la copia que llegaría encima**
en vez de duplicar el trabajo, y cuya agenda vive en un fichero: si el proceso muere, otro proceso
recupera las tareas y las ejecuta.

Salida esperada al terminar la demo:

```
VERIFICADO: disparo cada 2 s · 6 copias rechazadas por max_instances · tarea vencida descartada · agenda en disco con 1 tarea(s) · tarea ejecutada por un proceso nuevo
```

## Coste y credenciales

- **Coste**: cero. Todo corre en tu máquina, sin cuenta, sin tarjeta y sin servicios de pago.
- **Credenciales**: ninguna. No hay claves, ni tokens, ni login. La única descarga es la imagen base
  de Python y los paquetes de pip.
- **Datos**: ninguno. La demo no lee ficheros tuyos ni sale a ninguna API.

## Requisitos

**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/

**Hardware** (mínimo para el entorno de pruebas)
- 1 GB de RAM libres, 1 CPU y 500 MB de disco libre para la imagen del contenedor.
- La prueba se hizo con 1 CPU; con menos va igual, pero lento.

**Tiempo estimado**: 3-5 minutos la primera vez (incluye descargar la imagen base y las dependencias).

## Entorno de pruebas

Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno**:
- `entorno/Dockerfile` — describe la máquina: Python 3.13, APScheduler 3.11.3 y SQLAlchemy.
- `pruebas/pruebas.sh` — construye esa máquina, ejecuta la demo dentro y comprueba la salida.
- `scripts/` — los seis scripts de la demo (informe, lento, perdido, agenda, listar, comprobar).
- `.env.example` — las dos variables de entorno **opcionales** que leen los scripts (`APS_TZ` y
  `AGENDA_DB`) con sus valores por defecto. No hace falta copiarlo: está para que veas qué se puede
  cambiar y dónde.

## Pasos

**Paso 1 — construir la máquina** (una sola vez):
```bash
docker --context default build -t repro-apscheduler-tareas-que-no-se-pisan:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script trabaja sobre una copia en `/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" \
  repro-apscheduler-tareas-que-no-se-pisan:local \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
```

**Paso 3 — o todo de una vez** con el script que usamos nosotros, que hace lo anterior y además
comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

El `--context default` fuerza el motor Docker local — útil si tienes configurado además uno remoto;
si en tu equipo solo hay uno, funcionará igual con o sin él.

## Qué hace cada script

1. `scripts/informe.py` — registra una tarea cada 2 segundos con `BackgroundScheduler`. No hay bucle:
   el planificador mira el reloj y llama a la función. La función no sabe a qué hora se ejecuta.
2. `scripts/lento.py` — la misma idea con una tarea de 3 segundos programada cada 1 segundo y
   `max_instances=1`. Es el caso que en cron te duplica el informe.
3. `scripts/perdido.py` — una tarea con `run_date` de hace 5 minutos y `misfire_grace_time=60`: el
   planificador la descarta y lo dice en el log. Es la prueba de que una tarea vencida no arranca a
   destiempo.
4. `scripts/agenda.py` — guarda dos tareas en un fichero SQLite (`SQLAlchemyJobStore`): el resumen
   diario a las 08:00 y un aviso programado para dentro de 8 segundos. Imprime las dos con su próxima
   ejecución y **el proceso termina**.
5. `scripts/listar.py` — otro proceso, el mismo fichero. Recupera las dos tareas, las imprime y las
   reanuda: el aviso dispara aquí, en un proceso distinto del que lo creó.
6. `scripts/comprobar.py` — lee las salidas anteriores y la tabla `apscheduler_jobs` del fichero
   SQLite, y comprueba que cada prueba ocurrió de verdad. Si algo no cuadra, falla.

## Resultado esperado

- `maximum number of running instances reached (1)` aparece **seis veces** en la prueba del solape:
  esas son las copias que el planificador rechazó. El vídeo las cuenta en pantalla.
- `was missed by 0:05:00` es la tarea vencida: existía, su hora pasó, y se descarta porque la ventana
  de gracia era de 60 segundos.
- `guardada: resumen_diario | proxima: 2026-10-25 08:00:00+01:00` incluye el desfase horario: la
  zona es `Europe/Madrid` y esa noche cambia la hora.
- `total en disco: 2` y luego `AVISO DISPARADO por el proceso nuevo`: la agenda sobrevive al proceso,
  y la tarea **se ejecuta** en el proceso siguiente, no solo se lee.
- Queda **una** fila en `apscheduler_jobs`: las tareas de tipo `date` se borran al ejecutarse; la de
  cron se queda esperando su próxima hora.

## Límites (lo que este material NO hace)

- **No mantiene vivo tu programa.** APScheduler programa dentro de un proceso: si el proceso no está
  corriendo, no hay planificador. Para eso hace falta un servicio (systemd, un contenedor con
  reinicio automático) o un cron del sistema que lo arranque.
- **No reparte trabajo entre máquinas.** Si lanzas la misma agenda en dos servidores, los dos
  ejecutan. Para coordinar hace falta una cola (Celery, RQ), que es otro problema.
- **No es una cola de tareas.** No hay reintentos con espera creciente, ni prioridades, ni workers
  separados. Si necesitas eso, APScheduler no es la herramienta.
- **El fichero SQLite se queda corto con escrituras concurrentes.** Para varios procesos escribiendo
  a la vez, usa el job store de SQLAlchemy con PostgreSQL.
- **Las tareas en `date` se borran al ejecutarse**: si quieres que se repitan, usa `interval` o
  `cron`.

## Si algo va mal: problemas y errores

- `TypeError: Unsupported type for run_date: float` → en APScheduler 3 la fecha va como `datetime`,
  no como número de segundos (`time.time()`). Es el error exacto que corregimos al probar este
  material.
- `skipped: maximum number of running instances reached` **no es un error**: es el planificador
  haciendo su trabajo. Si no quieres verlo, sube `max_instances`, pero antes pregúntate por qué tu
  tarea tarda más que su intervalo.
- La agenda sale vacía en el segundo proceso → los dos scripts tienen que apuntar al **mismo**
  fichero (`AGENDA_DB`), y las funciones referenciadas deben tener el mismo nombre en los dos.
- Error de versión → este material se probó con `apscheduler==3.11.3`. La versión 4 está en alfa y
  cambia la forma de escribir los disparadores.

## Créditos y licencia

Material didáctico del canal @lytohlgIA. La herramienta es
[APScheduler](https://github.com/agronholm/apscheduler) (MIT); aquí solo se muestra cómo usarla. Los
scripts de esta carpeta son míos y puedes copiarlos, cambiarlos y romperlos a gusto.
