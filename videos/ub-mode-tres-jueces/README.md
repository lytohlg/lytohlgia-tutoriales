# Mis tests pasaban en verde y no probaban nada: ub-mode de Uncle Bob

> Material del vídeo **«Mis tests pasaban en verde y no probaban nada: ub-mode de Uncle Bob»** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir

Medir un módulo de Python con las tres herramientas de calidad que la skill `ub-mode` de
Robert C. Martin manda ejecutar, y obtener un veredicto con código de salida:

- **complejidad** (crapper): CRAP = CC² × (1−cobertura)³ + CC, con umbral 10
- **duplicación** (dryer): huellas estructurales por Jaccard, umbral 0,82
- **mutaciones** (mutator): inyecta fallos en tu código y comprueba si tus tests los matan

El módulo que se mide (`src/pedidos.py`) está escrito a propósito para suspender: una función
con 17 caminos y dos funciones de envío copiadas.

## Requisitos

**Software**
- Docker instalado (`docker --version`, 20.10 o superior) — https://docs.docker.com/get-docker/
- Git dentro de la imagen (lo instala el propio `Dockerfile`); en tu máquina no hace falta nada más.
- Red en la **primera** construcción: las tres herramientas se descargan de sus repositorios.

**Hardware** (mínimo para el entorno de pruebas)
- 1 CPU, 2 GB de RAM libres, 1 GB de disco para la imagen.
- La prueba se hizo en un contenedor de 1 CPU; el mutator tarda ahí menos de un minuto.

**Tiempo estimado**: 6-8 minutos la primera vez (incluye construir la imagen y las 53 mutaciones).

## Entorno de pruebas

Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú.

- `entorno/Dockerfile` — describe la máquina: `python:3.12-slim`, `git`, las tres herramientas
  instaladas desde su repositorio original ancladas a un commit, y las versiones de `pytest` y
  `coverage` fijadas.
- `pruebas/pruebas.sh` — construye esa máquina y ejecuta la demo dentro, con la carpeta montada en
  solo lectura y una copia de trabajo en `/tmp`. Es la prueba que pasó el material antes de
  publicarse.
- `demo.sh` — la demo en sí: los once pasos que se ven en el vídeo.

## Pasos

**Paso 1 — construir la máquina y probarlo todo de una vez** (lo que se ejecutó antes de publicar):

```bash
bash pruebas/pruebas.sh
```

**Paso 2 — a mano, si quieres ir parando**:

```bash
docker build -q -t repro-ub-mode-tres-jueces:local -f entorno/Dockerfile .
docker run --rm -it -v "$PWD:/trabajo" -w /trabajo repro-ub-mode-tres-jueces:local bash
# dentro del contenedor:
bash demo.sh
```

**Paso 3 — solo el veredicto**, dentro del contenedor y tras la demo:

```bash
python gate.py; echo "exit=$?"
```

## Qué hace cada fichero

- `src/pedidos.py` — el módulo feo a propósito: un `if` anidado de 17 ramas y dos funciones de envío calcadas.
- `tests/test_pedidos.py` — tres tests que pasan y no comprueban nada (solo miran `> 0`).
- `gate.py` — ejecuta cobertura, crapper, dryer y mutator, imprime la tabla y devuelve exit 0/1 según el umbral CRAP (10) y los fallos de duplicación y mutación.
- `demo.sh` — los once pasos del vídeo, en orden, con las cifras comentadas.
- `entorno/Dockerfile` — la máquina de pruebas (Python 3.12, git, las tres herramientas, pytest y coverage fijados).
- `pruebas/pruebas.sh` — build de la imagen + demo en limpio con la carpeta en solo lectura.
- `material.json` y `paquete.json` — metadatos del paquete (slug, título, fecha de publicación, comando, imagen, pruebas).
- `.env.example` — no hay credenciales que rellenar; el fichero explica las únicas variables que usan los scripts.

## Resultado esperado

Salida real de la última ejecución completa (`bash pruebas/pruebas.sh`) en un contenedor limpio:

```
funcion                   CC    cob%    CRAP  juez
clasifica_pedido          17    38.9    83.0  FALLA
calcula_envio_normal       5    58.3     6.8  OK
calcula_envio_urgente      5    58.3     6.8  OK

duplicados: 1 bloque(s)
mutantes:   1 matado / 29 sobreviven / 23 sin cubrir (53 sitios)

VEREDICTO: RECHAZADO (3 fallos)
   código de salida de gate.py: 1
```

Y, con la cobertura al 100 %, el CRAP de `clasifica_pedido` bajaría a 17,0: la cobertura deja de
esconder la complejidad, no la reduce.

Detalle por paso:

| Paso | Comando | Resultado real |
|---|---|---|
| tests | `pytest tests -q` | 3 passed (y no comprueban nada) |
| CRAP sin cobertura | `crapper --root . --source-root src` | `NO TESTS RAN`, CRAP **306.0** |
| cobertura real | `coverage run --source=src -m pytest` + `coverage lcov` | **38,9 %** (crapper) / 47 % de sentencias (coverage) |
| CRAP con cobertura | `crapper ... --use-existing-coverage` | CRAP **83.0** |
| duplicación | `dryer --root . --source-root src` | `DUPLICATE score=1.00` |
| mutaciones | `mutator ... --mutate-all --test-command "python -m pytest tests -q"` | 53 sitios: **1 matado**, 29 supervivientes, 23 sin cubrir |
| gate | `python gate.py` | `RECHAZADO (3 fallos)`, exit 1 |

**No se demuestra** que un agente de código (Claude Code, Cursor, etc.) obedezca la skill: en este
material no se ha probado eso, solo las herramientas que la skill manda ejecutar. La skill es un
markdown de instrucciones; no mide nada por sí sola.

## Las tres herramientas no vienen dentro de ub-mode

`unclebob/ub-mode` tiene tres ficheros: `SKILL.md`, `README.md` y `LICENSE`. Las herramientas son
tres repositorios aparte:

- https://github.com/unclebob/crapper (commit `c757ec7`)
- https://github.com/unclebob/dryer (commit `66ff6d2`)
- https://github.com/unclebob/mutator (commit `0136cf5`)

No van copiadas dentro del paquete: `entorno/Dockerfile` las instala desde su repositorio
original, ancladas a esos commits (`pip install "crapper @ git+https://github.com/unclebob/crapper@c757ec7"`).
Las tres son BSD Zero Clause (0BSD) y no se tocan. La primera construcción necesita red.

## El tropiezo que hace útil este material

La primera pasada de `crapper` da `Cov 0.0%` aunque `pytest` diga que los tests pasan. La causa:
la herramienta busca los tests con `unittest discover`, y con `pytest` no los encuentra; además,
`pytest-cov` escribe en su XML `filename="pedidos.py"` (sin la carpeta) y la herramienta busca
`src/pedidos.py`. No enlaza y asume 0 %.

La solución que funciona:

```bash
python -m coverage run --source=src -m pytest tests -q
python -m coverage lcov -o target/coverage/python/lcov.info
python -m crapper --root . --source-root src --use-existing-coverage
```

## Coste / credenciales

- **Coste**: 0. Todo se ejecuta en local: no hay servicios de pago, ni API, ni cuenta.
- **Credenciales**: ninguna. No hace falta token, ni clave, ni `.env` relleno.
- **Red**: solo para construir la imagen la primera vez (descarga de las tres herramientas desde
  GitHub y de `pytest`/`coverage` desde PyPI). Después, la demo funciona sin red.

## Solución de problemas

- **`docker: command not found`** — instala Docker y vuelve a lanzar `bash pruebas/pruebas.sh`.
- **La construcción falla al descargar las herramientas** — es un problema de red o de acceso a
  GitHub. Comprueba `git ls-remote https://github.com/unclebob/crapper` y reintenta.
- **`permission denied` al montar la carpeta** — el montaje es de solo lectura y la copia se hace en
  `/tmp`; si usas SELinux, añade `:z` al volumen.
- **El mutator tarda** — son 53 sitios y cada uno lanza la suite; en 1 CPU puede irse a un minuto.
  Es normal, no está colgado.
- **El mutator marca 53/53 como matados (score 100 %) y huele raro** — falso positivo típico: si el
  comando de test falla por configuración (por ejemplo `pytest` sin colección válida), la
  herramienta interpreta «los tests fallaron» como «mutante detectado». Verifica que
  `python -m pytest tests -q` pasa de verdad antes de fiarte del score.
- **`Cov 0.0%` con tests en verde** — es el tropiezo del vídeo: usa `coverage run --source=src` +
  `coverage lcov` y `--use-existing-coverage`, como en el paso anterior.

## Estructura

```
.
├── demo.sh               # los once pasos del vídeo
├── gate.py               # los tres jueces + veredicto + exit 0/1
├── src/pedidos.py        # el módulo feo a propósito
├── tests/test_pedidos.py # tres tests que pasan siempre
├── entorno/Dockerfile    # la máquina de pruebas
├── pruebas/pruebas.sh    # build + demo en limpio
├── .env.example          # no hay credenciales: lo explica
├── material.json         # metadatos del paquete
└── paquete.json          # manifiesto (comando, imagen, pruebas)
```

## Licencia

El código de este paquete (`gate.py`, `src/`, `tests/`, `demo.sh`) se publica bajo MIT.
Las tres herramientas (`crapper`, `dryer`, `mutator`) son de Robert C. Martin, con licencia BSD Zero Clause.
