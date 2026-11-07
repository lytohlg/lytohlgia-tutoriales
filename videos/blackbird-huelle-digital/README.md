# Blackbird: en qué 653 webs existe tu nombre de usuario (y cuáles no eres tú)

> Material del vídeo **Blackbird: en qué 653 webs existe tu nombre de usuario (y cuáles no eres tú)** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Te haces una cuenta nueva y el nombre ya está cogido. Alguien te escribe a un perfil que no es
tuyo. O al revés: quieres saber si el nombre que vas a usar como marca ya está ocupado, y
averiguarlo a mano significa abrir decenas de webs una por una. Y cuando por fin encuentras algo,
no sabes si ese perfil es tuyo, de un homónimo o de alguien que se está haciendo pasar por ti.

## Qué vas a conseguir

Ves, en un comando, en cuántas de 653 webs existe un nombre de usuario, y separas los perfiles
reales de los homónimos con una verificación automática que escribe un informe en Markdown y CSV.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.12 o superior (`python3 --version`).
- Conexión a internet: la herramienta consulta las webs en vivo y clona su repositorio.

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1 GB de disco libre para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 10 minutos la primera vez (incluye descargar la imagen base).

**Credenciales**: ninguna. Este material no usa claves ni cuentas de ningún servicio.

## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (los tres van en esta carpeta, no hay más):
- `entorno/Dockerfile` — describe la máquina: imagen base y dependencias con la versión fijada.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de claves. Aquí está vacía a propósito: este material no necesita
  ninguna.

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos la primera vez porque
descarga la imagen base):
```bash
docker --context default build -t repro-blackbird-huelle-digital:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" python:3.13-slim bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno. El contenedor tiene
red (la herramienta consulta webs en vivo y clona su repositorio); lo que **no** tiene son tus datos.

**Detalles de nuestra ejecución, por si tu caso es distinto:** las órdenes de arriba son las mismas
que usamos nosotros, tal cual. El `--context default` fuerza el motor Docker local — útil si tienes
configurado además uno remoto; si en tu equipo solo hay uno, déjalo igual (funciona) o quítalo.
Ejecutamos con el usuario `1000:1000` para no correr como root y con `HOME=/tmp` para que el
contenedor no dependa de nada de fuera.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd blackbird-huelle-digital
   ```
2. Elige el nombre de usuario que quieres revisar (por defecto el script usa uno público de ejemplo):
   ```bash
   export USUARIO=tu_nombre_de_usuario
   ```
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `huelle.py` | Convierte la lista cruda de Blackbird en un informe verificado: comprueba cada URL y separa «probable» de «dudoso» y «caído». |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de claves (vacía: este material no pide ninguna). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
- **`huelle.py`** — el script propio del vídeo. Hace tres cosas, en este orden: (1) lanza Blackbird
  con `--json` y localiza el JSON que acaba de escribir; (2) recorre cada hallazgo y pide la URL con
  un `GET` normal, con su propio `User-Agent`, para ver si responde y si el nombre aparece en la
  página; (3) escribe `results/informe_<usuario>.md` y `.csv` con el veredicto de cada uno —
  `probable` (200 y el nombre está en la página), `dudoso` (200 pero el nombre no aparece: muro de
  login, registro genérico o simplemente otra persona) o `caido` (error HTTP o timeout). Es lo que
  convierte una lista de pistas en algo que puedes leer y decidir. No necesita claves y no envía
  datos a ningún sitio: solo hace las peticiones a las URLs que Blackbird ya encontró.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial
  con la versión fijada (nada de `latest`), instala lo que el material necesita (`git`) y deja el
  directorio de trabajo preparado. No copia claves ni tus datos.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en dos pasos: construye la imagen de
  `entorno/Dockerfile` y ejecuta la demo con la carpeta original montada en solo lectura. Si algo
  falla, para y te dice en qué paso.
- **`.env.example`** — la lista de claves que el material espera. Está vacía porque no hay ninguna:
  así se ve de un vistazo que este material no pide credenciales.

## Resultado esperado
`INFORME LISTO`

## Aviso de uso responsable
Esta herramienta sirve para revisar **tu propia** huella o la de un sistema del que eres
responsable, y para comprobar un nombre antes de usarlo como marca. Usarla para seguir o perfilar a
terceros sin su consentimiento puede ser ilegal según el país y, desde luego, no es lo que se enseña
aquí. Los hallazgos son pistas, no identidades: muchas veces el perfil es de otra persona con el
mismo nombre.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **`Could not find a version that satisfies the requirement`**: pip está desactualizado dentro del
  contenedor; ejecuta `python3 -m pip install -U pip` y repite.
- **Muchos «caido»**: normal. Buena parte de la lista son webs que bloquean peticiones desde
  servidores o que ya no existen.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
