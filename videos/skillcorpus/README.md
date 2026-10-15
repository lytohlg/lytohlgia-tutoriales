# SkillCorpus: 222 skills de agente filtradas y buscables con Python

> Material del vídeo **SkillCorpus: 222 skills de agente filtradas y buscables con Python** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Convertir ficheros `SKILL.md` sueltos de cuatro repositorios públicos en **un corpus de 222 skills
(20 columnas)**: `skills.parquet` + `attachments.tar.zst` + una tarjeta de dataset, pasando por los
cuatro filtros del proyecto (seguridad, calidad, duplicados y licencia). Al terminar sabrás construir
el corpus, leerlo y ver de dónde sale cada fila.

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.13 lo trae el propio contenedor: no instalas nada en tu máquina. El repositorio se clona
  dentro, así que no necesitas tener `git` fuera.

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 2 CPU y 3 GB de disco libre (la imagen ocupa ~1,5 GB con las dependencias CPU:
  `faiss-cpu`, `sqlite-vec`, `pyarrow`).
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU y 2 GB de RAM.

**Tiempo estimado**: 15 minutos la primera vez. La mayor parte se va en clonar los cuatro repositorios
de origen y en construir el corpus, no en instalar.

## Entorno de pruebas
Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno** (van todos en esta carpeta, no hay más):
- `entorno/Dockerfile` — describe la máquina: imagen base (`python:3.13-slim`), dependencias, y el
  repositorio de SkillCorpus **fijado por commit** (`7b3a0ea`, el del vídeo).
- `entorno/deploy/` — los ficheros de la demo que en el vídeo viven en `/opt/deploy`: `config.yaml`
  (configuración del corpus), `mis_fuentes.yaml` (los cuatro repositorios de origen) y `report.py`
  (el informe que se lee al final).
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, en limpio. Es la prueba que
  pasó el material antes de publicarse.
- `.env.example` — plantilla de las claves que necesite el material. Aquí está vacía a propósito:
  este material no pide ninguna clave. Se copia a `.env` (que **no** se sube nunca al repositorio).

No usamos `docker-compose`: para un contenedor que ejecuta un comando no hace falta, y el Dockerfile
es el punto de partida si algún día hiciera falta más de uno.

**Paso 1 — construir la máquina** (una sola vez; tarda unos minutos porque descarga la imagen base y
las dependencias):
```bash
docker --context default build -t repro-skillcorpus:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-skillcorpus:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace exactamente lo
anterior y además comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra
montada como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu
máquina: lo que falla en limpio es un fallo real, no un resto de tu entorno. El contenedor **sí
necesita red**, porque clona cuatro repositorios públicos y consulta PyPI; lo que **no** tiene son
tus datos.

**Detalles de nuestra ejecución, por si tu caso es distinto:** el `--context default` fuerza el motor
Docker local — útil si tienes configurado además uno remoto; si en tu equipo solo hay uno, déjalo
igual o quítalo. Ejecutamos con el usuario `1000:1000` y `HOME=/tmp`; por eso el Dockerfile deja el
árbol de Python y `/work` a nombre de ese usuario (si no, el `pip install -e .` del vídeo fallaría con
«Permission denied»).

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd skillcorpus
   ```
2. Construye la máquina de pruebas (el paso 1 de arriba). No hay claves que rellenar.
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

Si prefieres hacerlo a mano en tu propia máquina, los comandos son los del vídeo, en este orden:
```bash
git clone --depth 1 https://github.com/EverMind-AI/SkillCorpus
cd SkillCorpus
pip install -e .
python -m skillcorpus.cli --lib /work/lib --config /opt/deploy/config.yaml build \
  --sources-config /opt/deploy/mis_fuentes.yaml
python examples/skillhub_demo.py "extract tables from a scanned PDF invoice"
ls -la /work/lib/corpus && head -16 /work/lib/corpus/README.md
python /opt/deploy/report.py
```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base, dependencias y el repositorio fijado por commit. |
| `entorno/deploy/config.yaml` | Configuración del corpus: pesos por fuente, umbrales del filtro de calidad y política de puntuación. |
| `entorno/deploy/mis_fuentes.yaml` | Los cuatro repositorios públicos que se agregan (registro de fuentes propio). |
| `entorno/deploy/report.py` | Lee los ficheros reales del corpus y resume filas, columnas y fuentes. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (aquí, ninguna; se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo, en
  ese orden, imprimiendo cada una con el `$` delante. Tiene **una** diferencia deliberada y a la
  vista: `git clone` deja el repositorio en el commit del vídeo (`7b3a0ea`) en lugar del HEAD de hoy,
  porque SkillCorpus ha seguido cambiando y sin el pin el recuento de skills ya no cuadraría. Se
  puede leer entero antes de ejecutarlo y no toca ficheros fuera de su carpeta.
- **`entorno/Dockerfile`** — construye la máquina de pruebas: imagen base oficial con versión fijada
  (`python:3.13-slim`, nada de `latest`), las dependencias del repositorio, el clon de SkillCorpus
  **fijado por commit**, y `/opt/deploy` con los ficheros de la demo. No copia claves ni tus datos.
- **`entorno/deploy/report.py`** — lee `/work/lib/corpus` y `/work/lib/index.db` de verdad (parquet
  incluido) y saca el recuento de filas, columnas, fuentes y categorías. Es el informe del final del
  vídeo: no hay ningún número escrito a mano.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en cuatro pasos: (1) comprueba que Docker responde;
  (2) construye la imagen de `entorno/Dockerfile`; (3) copia la carpeta a un directorio temporal
  dentro del contenedor y ejecuta ahí la demo, con la carpeta original montada en solo lectura;
  (4) compara la salida con la esperada y te dice si cuadra. Si algo falla, para y te dice en qué paso.
- **`.env.example`** — la lista de claves que el material espera. En este material está vacía porque
  no hace falta ninguna; el fichero se mantiene para que la estructura sea la misma en todos los vídeos.

## Resultado esperado
Salida real del build (resumida; los números salen de los repositorios de origen, no están escritos a
mano). Con los cuatro repositorios en el estado del commit fijado, el corpus queda así:

```
=== anthropics/skills (git_clone) ===        ingested 1/1 repo, added=18
=== vercel-labs/skills (git_clone) ===       ingested 1/1 repo, added=2
=== addyosmani/agent-skills (git_clone) ===  ingested 1/1 repo, added=25
=== K-Dense-AI/scientific-agent-skills ===   ingested 1/1 repo, added=177
→ export.corpus (parquet + attachments + card)...
  corpus: 222 rows, 197 with attachments → /work/lib/corpus
total: 0 -> 222 (delta 222)

== skills.parquet ==
  filas: 222   columnas: 20
  fuente K-Dense-AI/scientific-agent-skills 177 skills
  fuente addyosmani/agent-skills            25 skills
  fuente anthropics/skills                  18 skills
  fuente vercel-labs/skills                  2 skills
```

**Ojo con dos cosas, dichas sin adornos:**
- El recuento depende del estado de los **cuatro repositorios de origen**, que se clonan en su HEAD
  (el vídeo no los fija). Si hoy uno de ellos tiene más skills, tu número será mayor y las filas de
  la tabla cambiarán. El pin solo se aplica al repositorio de SkillCorpus, que es el programa.
- Si no hay un servidor de modelo accesible, el build lo dice en pantalla y sigue: las categorías
  quedan en `OTHER` y el filtro de seguridad avisa de que no se aplicó el juicio por modelo
  (`LLM unavailable`, `222 active skills have no LLM judgment`). Eso es **lo que se ve en el vídeo**,
  no un fallo de tu instalación: en `entorno/deploy/config.yaml` puedes apuntar a tu propio servidor
  (endpoints OpenAI-compatibles) y repetir el build.

## Coste y credenciales
Nada: todo lo que hace este material es gratis y no necesita claves. El `config.yaml` trae una clave
de mentira (`dummy`) apuntando a un servidor local, que es como se grabó el vídeo. Si le pones tus
endpoints de embeddings y de modelo, el corpus cambia (categorías, puntuación de calidad y duplicados
por similitud), pero eso ya es tu llamada, con tu clave y tu coste.

## Solución de problemas
- **«command not found»**: te falta Docker; instálalo y vuelve a empezar.
- **Error de permisos al escribir en `/work`**: estás usando una imagen vieja; reconstruye con
  `docker --context default build --no-cache -t repro-skillcorpus:local entorno`.
- **Falla al clonar**: el contenedor necesita salida a Internet (clona cuatro repositorios públicos y
  consulta PyPI). En una red corporativa puede estar bloqueado.
- **El recuento de filas no es 222**: mira el aviso de arriba; los repositorios de origen cambian cada
  semana. Con el commit fijado de SkillCorpus y los cuatro orígenes como estaban al grabar, sale 222.
- **`faiss-cpu` o `sqlite-vec` tardan en instalarse**: son dependencias CPU, no GPU; si tu equipo va
  justo de memoria, la primera construcción puede tardar unos minutos más.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
Este material (los ficheros de esta carpeta) es **MIT**: puedes usarlo, modificarlo y distribuirlo
libremente. Ver `LICENSE` en la raíz del repositorio.

El programa que se ejecuta es **SkillCorpus** (https://github.com/EverMind-AI/SkillCorpus), con
licencia **Apache-2.0**. Además, cada skill del corpus viene de uno de los cuatro repositorios de
origen y conserva su propia licencia en la columna `license` del parquet: el build solo activa
fuentes de la lista blanca (licencia verde) y descarta el resto, que es exactamente para lo que está
el filtro `license_audit`.
