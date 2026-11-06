# Horizon: tu radar de noticias con IA, filtrado y puntuado (Python)

> Material del vídeo **Horizon: tu radar de noticias con IA, filtrado y puntuado (Python)** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí están los ficheros que salen en pantalla (config, perfiles y un boletín ya generado) y una demo
> que los lee y los comprueba. **La llamada al modelo no se reproduce aquí**: necesita una clave y
> cuesta dinero en cada ejecución. Todo lo demás sí, y sin instalar nada.

## El problema
Tienes veinte fuentes de noticias abiertas y ningún criterio para decidir qué leer primero. Al final
lees lo que ha sonado más fuerte, no lo que más te importa, y lo que no viste ese día se pierde. El
trabajo de filtrar con criterio propio es justo el que nadie hace a mano todos los días.

Este material enseña dónde vive ese criterio en Horizon: un fichero de configuración y una carpeta de
perfiles en markdown, con la rúbrica de puntuación escrita en texto plano.

## Qué vas a conseguir
Convertir un montón de fuentes de noticias en un boletín diario en español, filtrado por una rúbrica en markdown y puntuado con un modelo.

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
docker --context default build -t repro-horizon-boletin-noticias-ia:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-horizon-boletin-noticias-ia:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd horizon-boletin-noticias-ia
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
| `scripts/leer_config.py` | Lee `ejemplo/config.json` y dice en cuatro líneas qué fuentes están activas y con qué umbral se corta. |
| `scripts/listar_rubricas.py` | Lista los perfiles de `ejemplo/reglas` y saca por pantalla la rúbrica real de `analysis.md`. |
| `scripts/leer_boletin.py` | Lee `ejemplo/boletin-es.md` y resume qué trae: piezas recogidas, seleccionadas, notas y bloques. |
| `ejemplo/config.json` | El config real con el que se generó el boletín: modelo, idioma, fuentes y umbral. Sin claves dentro. |
| `ejemplo/reglas/` | Las cinco rúbricas reales del programa (en el proyecto, esta carpeta se llama `profiles/`). Cada perfil lleva `match.md` (cuándo aplica), `analysis.md` (cómo puntúa), `enrichment.md` (cómo redacta) y `profile.json` (los ajustes). |
| `ejemplo/boletin-es.md` | Un boletín ya generado, tal cual lo escribió el programa: seis piezas recogidas, cinco seleccionadas. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
- **`scripts/leer_config.py`** — abre `ejemplo/config.json` y traduce el JSON a cuatro líneas: modelo,
  idioma del boletín, perfil y umbral de corte, y qué fuentes están activas. Es el mismo fichero que
  lee el programa; aquí solo se lee, no se ejecuta nada.
- **`scripts/listar_rubricas.py`** — recorre `ejemplo/reglas` y enseña cuántos perfiles hay y qué
  ficheros tiene cada uno. Después imprime las bandas de puntuación de `analysis.md` del perfil que le
  pidas: ahí está el criterio, en texto plano, para que puedas cambiarlo sin tocar Python.
- **`scripts/leer_boletin.py`** — lee `ejemplo/boletin-es.md` (la salida real del programa) y cuenta lo
  que trae: piezas recogidas, seleccionadas, la nota de cada una y los bloques de cada entrada.
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
Salida real de `bash demo.sh` (no la que nos gustaría: esta):

```
== Horizon: tu radar de noticias con IA, filtrado y puntuado ==

1) El config: de dónde lee y con qué criterio decide
modelo: deepseek-chat
idioma del boletín: es
perfil por defecto: noticias-es · umbral de corte: 6.0
fuentes activas: hackernews, Python Insider, Simon Willison

2) Los perfiles: el criterio está escrito en markdown, no en el código
perfiles: 5
- tech-news: 3 ficheros de texto (match.md, analysis.md, enrichment.md) + profile.json
perfil elegido: Technology News (id tech-news)
rúbrica de puntuación:
  - **9-10: Groundbreaking.** ...
  - **7-8: High value.** ...
  ...

3) Un boletín ya generado, leído por la máquina
piezas recogidas: 6
seleccionadas: 5
nota media: 6.6/10
- 8.0/10 Moonshot AI publica los pesos abiertos de Kimi K3.1 Pro
...
```

Lo que tiene que aparecer sí o sí: **`seleccionadas: 5`**. Si tu salida no lo trae, algo se rompió en
el camino (mira la sección de problemas).

El config trae `noticias-es` como perfil por defecto; en el vídeo se usa `tech-news` porque ese día se
buscaba tecnología. Los dos están en `ejemplo/reglas`.

## Coste / credenciales
La **ejecución completa** (la del vídeo) llama a un modelo: necesita `DEEPSEEK_API_KEY` en el entorno
—el nombre de la variable, no la clave, está en `ejemplo/config.json` y en `.env.example`— y cuesta
tokens en cada pasada. La del vídeo gastó unos 34.000 tokens en una sola ejecución (unas cinco
piezas). El coste corre de tu cuenta.

La **demo de este paquete no gasta nada**: no llama a ningún modelo ni sale a internet. Lee ficheros
que ya están aquí. Por eso se puede reproducir sin clave y sin tarjeta.

Ojo con el idioma: `languages: ["es"]` afecta al cuerpo del boletín, no a las etiquetas ni a los
encabezados del markdown, que el programa escribe en inglés.

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
