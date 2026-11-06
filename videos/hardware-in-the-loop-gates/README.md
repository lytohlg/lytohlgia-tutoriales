# Cómo detectar el código falso que escribe una IA (Python)

> Material del vídeo **Cómo detectar el código falso que escribe una IA (Python)** del canal
> [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está el proyecto falso que se audita en pantalla, las órdenes exactas del vídeo y el entorno
> para repetirlo. **Lo que se ejecuta es el repositorio público de otro autor**
> ([Kemerd/claude-hardware-in-the-loop](https://github.com/Kemerd/claude-hardware-in-the-loop),
> revisión `cfc1f19`), traído a la revisión fijada: no hay copias nuestras de su código.

## El problema

Le pides a un agente el driver de un sensor y contesta «hecho». El fichero compila, pasa el revisor,
y tres semanas después el registro dice veintiún grados durante toda la noche de la helada. Dentro
había una función que devolvía veintiuno.

No es mala fe: el trabajo del agente es producir código que **parezca** correcto. Si nadie lo
comprueba en la máquina, «parece correcto» y «es correcto» son la misma cosa hasta que falla lejos
de casa.

## Qué vas a conseguir

Ejecutar una auditoría que señala los sustitutos en un proyecto real, entender **por qué** un script
que solo imprime hallazgos no es un control (le falta el código de salida) y generar el esqueleto de
proyecto del método, con la puerta puesta dentro.

## Requisitos

**Software**
- Docker (`docker --version`, 20.10 o superior) — https://docs.docker.com/get-docker/
- Python 3.12 o superior en el contenedor (ya viene en la imagen). En tu máquina solo hace falta para
  leer los scripts: `python3 --version`.
- `git` para traer el repositorio (`demo.sh` lo hace por ti).

**Red**
- El contenedor necesita red **una vez**, para clonar el repositorio público en la revisión fijada.
  Si lo ejecutas en una máquina sin salida a internet, clona antes `repo/` a mano con
  `bash traer_repo.sh` desde una máquina que sí la tenga.

**Hardware**: 1 CPU, 1 GB de RAM y 1 GB de disco libre. La prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 5 minutos la primera vez (incluye descargar la imagen base y clonar).

## Entorno de pruebas

Todo lo que sale en el vídeo se ejecutó en un contenedor limpio, y aquí tienes ese mismo entorno para
repetirlo. La máquina de pruebas se describe en un fichero:

- `entorno/Dockerfile` — imagen base `python:3.12-slim` + `git` + `ca-certificates`. Nada más.
- `pruebas/pruebas.sh` — construye esa máquina, ejecuta la demo en limpio y comprueba la salida.

**Paso 1 — construir la máquina** (una sola vez):
```bash
docker build -t repro-hardware-in-the-loop-gates:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en **solo
lectura** (el script trabaja sobre una copia en `/tmp`, no toca tus ficheros):
```bash
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$PWD:/trabajo:ro" repro-hardware-in-the-loop-gates:local \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
```

**Paso 3 — o todo de una vez** con el script que usamos nosotros:
```bash
bash pruebas/pruebas.sh
```

## Qué hace cada fichero

| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Las órdenes del vídeo, en el mismo orden. Es el material en sí. |
| `traer_repo.sh` | Clona el repositorio público en la revisión que se comenta en el vídeo. |
| `proyecto_falso/firmware/barometro.c.txt` | El driver del barómetro que el agente dio por terminado: tres funciones con nombre de hardware que devuelven constantes. Va como `.txt` porque el índice de este repositorio no admite `.c`; la demo lo copia como `barometro.c`. |
| `proyecto_falso/control/alarmas.py` | La lógica de alarma del mismo proyecto: una función con `pass` y otra que lanza `NotImplementedError`. |
| `nuevo/bomba.c.txt` | El driver que «el agente añade» en la segunda parte: sirve para ver que la puerta solo bloquea lo nuevo. |
| `answers.json` | Las veinte respuestas del proyecto de ejemplo con el que se genera el andamio. |
| `entorno/Dockerfile` | La máquina donde se prueba: Python 3.12 y git, sin nada más. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. |
| `.env.example` | Variables de entorno: la demo no necesita ninguna, solo documenta `TMPDIR`. |
| `paquete.json` | Ficha del índice del repositorio: título, fecha, comando y salida esperada. |
| `material.json` | Ficha mínima que lee el índice. |
| `README.md` | Esto. |

## Los seis pasos, y qué demuestra cada uno

1. **La puerta mira el proyecto.** `audit_placeholders.py --root "$TMPDIR/proyecto_falso"` recorre los ficheros
   y devuelve cinco hallazgos: tres funciones de C con nombre de hardware cuyo cuerpo entero es
   devolver una constante, y dos funciones de Python vacías. Termina en **0**: informa y deja pasar.
2. **La misma puerta, exigiendo que bloquee.** Con `--fail-on-new` los hallazgos son idénticos y el
   código de salida es **1**. Esa es toda la diferencia entre un informe y un control.
3. **La deuda vieja se firma.** `--write-baseline` guarda los cinco hallazgos como línea base: al
   repetir, `new 0, gating 0` y termina en 0. No bloquea por lo que ya existía.
4. **Lo nuevo, sí.** Se copia `nuevo/bomba.c.txt` como `bomba.c` en la carpeta de trabajo y la auditoría devuelve `new 2, gating 2`,
   código de salida 1. La puerta distingue deuda vieja de trabajo recién entregado.
5. **El andamio.** `scaffold.py --answers answers.json` escribe **118 ficheros**: estructura, reglas,
   plan, herramientas y la auditoría dentro.
6. **El andamio nace en verde.** La misma auditoría sobre `/tmp/mi_placa` devuelve **0 hallazgos**.

## Resultado esperado (el que comprueba `pruebas.sh`)

```
new 2, gating 2
```

Si aparece esa línea, la puerta ha distinguido el trabajo nuevo del que ya estaba firmado: es la prueba
de que la auditoría funciona y no es un adorno.

## Coste / credenciales

- **Coste**: cero. No hay servicios de pago, ni claves de API, ni cuentas. Lo único que se descarga es
  la imagen base de Python (gratuita) y el repositorio público. Todo el trabajo ocurre en tu máquina.
- **Credenciales**: ninguna. La demo no pide usuario ni token, y no envía nada a ningún sitio. El
  contenedor puede ejecutarse sin red después de la primera vez (`traer_repo.sh` es lo único que la usa).
- **Disco**: menos de 1 GB (imagen base incluida).

## Solución de problemas

| Síntoma | Causa | Qué hacer |
|---|---|---|
| `docker: command not found` | No hay Docker | Instálalo: https://docs.docker.com/get-docker/ |
| `Cannot connect to the Docker daemon` | El servicio está parado o tu usuario no está en el grupo `docker` | `sudo systemctl start docker` y `sudo usermod -aG docker $USER` (reinicia la sesión) |
| `fatal: unable to access ... github.com` | El contenedor no tiene salida a internet | Clona antes desde una máquina con red con `bash traer_repo.sh` y copia la carpeta `repo/` |
| `Permission denied` al escribir en `/tmp` | El contenedor corre con tu usuario y `TMPDIR` apunta a otro sitio | `export TMPDIR=/tmp` y repite |
| La auditoría dice `new 0, gating 0` cuando esperabas hallazgos | Ya existe una línea base en esa carpeta de trabajo | Borra `${TMPDIR:-/tmp}/proyecto_falso` y vuelve a empezar |
| `ModuleNotFoundError` al ejecutar `scaffold.py` | Estás usando tu Python en vez del contenedor | Ejecuta dentro de la imagen, como indica «Entorno de pruebas» |
| Todo sale en verde y nada se bloquea | Olvidaste `--fail-on-new` | Es justo la lección del vídeo: sin la bandera, informa pero no bloquea |

## Los límites, dichos aquí también

- **No se ha fabricado ninguna placa.** Lo que se demuestra es la puerta que la comprobaría.
- **No se ha ejecutado KiCad** (ni el flujo de esquemático/PCB del repositorio) ni los simuladores con
  motor gráfico: no hay GPU en la máquina donde se grabó.
- El repositorio es un **punto de partida** que se reescribe, no un producto.
- Su licencia es **HIL-ASA-1.0 (source-available)**: se puede leer, pero no es software libre. Léela
  antes de reutilizar trozos.
- `--fail-on-new` solo compara con la línea base: si aceptas todo sin mirar, la puerta deja de servir.
