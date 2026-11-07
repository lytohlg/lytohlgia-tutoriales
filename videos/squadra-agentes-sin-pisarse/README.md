# Tres agentes de IA en el mismo repositorio sin pisarse

> Material del vídeo **Tres agentes de IA en el mismo repositorio sin pisarse (Squadra)** del canal
> [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está lo mismo que se ejecuta en pantalla, listo para que lo repitas tú. **Lo que se ejecuta es
> el repositorio público de otro autor** ([dagoSte/squadra](https://github.com/dagoSte/squadra)),
> traído a una revisión fijada: no hay copias nuestras de su código.

## El problema

Trabajas con dos o tres ventanas de agentes de código abiertas sobre el mismo repositorio. Una
reescribe un fichero que la otra acaba de tocar. Las dos dan la tarea por terminada y ninguna tiene
prueba de nada. A la mañana siguiente te toca leer diferencias a mano para averiguar quién rompió
qué, y volver a pedir lo mismo que ya pediste dos veces.

No es que los agentes escriban mal: es que **nadie lleva el registro** de quién tiene cada tarea, qué
se acordó comprobar y quién revisó el resultado. Todo eso vive en tu cabeza y en el historial del
chat, que el agente de al lado no ve.

## Qué vas a conseguir

Montar un registro compartido en disco, con tres ventanas dadas de alta (una coordina, una construye,
una revisa), y ver las cuatro negativas que de verdad protegen el trabajo:

- una tarea no arranca sin acuse de recibo;
- **la prueba no se puede cambiar a mitad de camino** (si el comando no es el pactado, no hay prueba);
- el paquete entregado se congela con un hash, y el revisor revisa esa copia;
- si el código cambia después de entregar, el cierre se niega.

Al final tienes un tablero que dice qué está hecho, con qué prueba y quién lo revisó.

## Requisitos

**Software**
- Linux o macOS (en Windows, WSL2). Los comandos son de shell POSIX.
- Docker (`docker --version`, 20.10 o superior) — https://docs.docker.com/get-docker/
- Python 3.12 o superior y `git` en el contenedor (ya vienen en la imagen del entorno).

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco para la imagen del contenedor.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base y clonar el repo).

## Entorno de pruebas

Todo lo que sale en el vídeo se ejecutó **en un contenedor limpio**, y ese mismo entorno está aquí
descrito para que lo repitas. La máquina se declara en `entorno/Dockerfile` (imagen base
`python:3.13-slim` con `git`), no hay nada que instalar en tu sistema.

**Ficheros que forman el entorno:**
- `entorno/Dockerfile` — la máquina: imagen base fijada y `git`. El repositorio público no va dentro.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio.
- `traer_repo.sh` — clona el repositorio del autor en la revisión exacta del vídeo.
- `.env.example` — plantilla de variables de entorno. Este material no necesita ninguna: está vacía
  a propósito y se documenta para que no haya sorpresas.

**Paso 1 — construir la máquina** (una sola vez):
```bash
docker build -t repro-squadra-agentes-sin-pisarse:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en **solo
lectura** (el script trabaja sobre una copia en `/tmp`):
```bash
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$PWD:/trabajo:ro" repro-squadra-agentes-sin-pisarse:local \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros:
```bash
bash pruebas/pruebas.sh
```

**Por qué así:** el contenedor no lleva nada tuyo dentro, la carpeta entra como solo-lectura y la
copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu máquina. El contenedor tiene red
(la demo clona el repositorio); lo que no tiene son tus datos.

## Pasos

1. Copia esta carpeta a tu máquina y entra:
   ```bash
   cd squadra-agentes-sin-pisarse
   ```
2. Trae el repositorio en la revisión fijada (o deja que la demo lo haga sola):
   ```bash
   ./traer_repo.sh
   ```
3. Ejecuta la demo:
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero

| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Las órdenes del vídeo, en el mismo orden. Es el material en sí. |
| `traer_repo.sh` | Clona `dagoSte/squadra` en la revisión `0e56ba3` y dice qué revisión es. |
| `entorno/Dockerfile` | La máquina de pruebas: imagen base fijada y `git`. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba previa a publicar. |
| `.env.example` | Plantilla de variables de entorno (este material no usa ninguna). |
| `paquete.json` | Ficha interna del repositorio didáctico: título, fecha y comando. |
| `material.json` | Ficha del índice con el enlace al vídeo y si pide claves. |
| `README.md` | Esto: problema, pasos, entorno de pruebas y resultado esperado. |

**Qué hace `demo.sh`, paso a paso:** crea un registro nuevo en una carpeta temporal, da de alta tres
ventanas (`coord`, `builder`, `reader`), escribe el alcance y la prueba **antes** de abrir la tarea,
abre la tarea con dueño, revisor y prueba pactada, acusa recibo y arranca, intenta demostrar con otro
comando (el sistema lo rechaza), demuestra con el comando pactado, entrega el paquete con su hash,
el revisor lo acusa y lo revisa, y el coordinador comprueba y cierra. El tablero final dice
`Done 1 of 1`.

## Resultado esperado

```
Done 1 of 1
```

Y antes de eso, la negativa que da sentido a todo el vídeo:

```
Proof command differs from agreed task contract
```

## Coste y credenciales

Nada: no hay claves, no hay cuenta y no hay servicio de pago. El repositorio es de licencia MIT y
todo corre en tu máquina.

## Solución de problemas

- **`command not found: git`** — estás ejecutando fuera del contenedor y sin `git` instalado; usa la
  imagen de `entorno/Dockerfile` o instala `git`.
- **Falla al clonar** — el contenedor necesita red; si estás en una red corporativa puede bloquear
  GitHub. Prueba `./traer_repo.sh` desde tu máquina.
- **`Permission denied` al escribir el registro** — el registro debe ir a una carpeta escribible
  (la demo usa `$TMPDIR` o `/tmp`); no lo apuntes dentro de la carpeta montada en solo lectura.
- **Docker tarda mucho la primera vez** — está descargando la imagen base; son ~1 GB una sola vez.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Qué está probado y qué no

- **Probado (🟢):** todo el ciclo de arriba, ejecutado en `python:3.13-slim` sin privilegios, sobre la
  revisión `0e56ba3` del repositorio. Las tres ventanas las escribo yo a mano en la demo: no hay
  agentes autónomos decidiendo, y el vídeo lo dice.
- **No probado (🟡):** escrituras simultáneas reales de dos procesos al mismo registro. La demo es
  secuencial. Windows nativo tampoco está cualificado (el proyecto declara macOS/POSIX).

## Licencia

El material de esta carpeta es MIT. El repositorio `dagoSte/squadra` es de su autor, también MIT:
se clona, no se copia.
