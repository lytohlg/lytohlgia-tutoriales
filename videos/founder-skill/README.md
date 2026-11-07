# Pon los números de tu negocio en un JSON y el script te dice si pierdes dinero

> Material del vídeo **Pon los números de tu negocio en un JSON y el script te dice si pierdes
> dinero (founder-skill)** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está lo mismo que se ejecuta en pantalla, listo para que lo repitas tú. **Lo que se ejecuta es
> el repositorio público de otro autor** ([Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill)),
> traído a una revisión fijada: no hay copias nuestras de su código.

## El problema

Un negocio puede vender todos los días y perder dinero en cada venta. El cálculo que casi todo el
mundo hace es *precio menos coste de la materia prima*, y lo que sale parece beneficio. Pero el
alquiler, el sueldo, la cuota del software y el seguro se pagan todos los meses, vendas una unidad o
vendas cero. Con esa cifra mal llamada «margen» se firman locales, se compra stock y se ponen precios.

Y casi nadie lo recalcula, porque el Excel que se montó tiene veinte pestañas, fórmulas que ya nadie
recuerda y números de hace dos años. El problema se nota en la cuenta del banco, cuando ya hay un
contrato firmado.

## Qué vas a conseguir

Sacar los números del Excel y dejarlos en un fichero de texto que se lee de un vistazo, y dejar que
las cuentas las haga un script cada vez que cambies una cifra. En concreto, con este material:

- la **contribución** por venta (lo que deja cada unidad para pagar la estructura);
- el **break-even**: cuántas ventas al día hacen falta para no perder dinero;
- el **margen al volumen que planeas**, y el aviso cuando el break-even **no cabe en tu capacidad**;
- el **año uno mes a mes**, la caja que necesitas y qué pasa si bajas el precio un 10 %;
- el **precio aceptable** a partir de las respuestas de tus clientes;
- un **veredicto del plan** (`Verdict: Not yet`) que sale con código de salida 1: lo puede comprobar
  un programa, no solo una persona.

## Requisitos

**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell POSIX).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.10 o superior y `git` en el contenedor (ya vienen en la imagen del entorno).
- **Ningún paquete de Python.** Las cuatro herramientas del repositorio son biblioteca estándar pura:
  no hay `pip install`, ni entorno virtual, ni claves de API, ni cuenta que crear.

**Hardware** (mínimo para el entorno de pruebas)
- 512 MB de RAM libres, 1 CPU y 300 MB de disco para la imagen del contenedor.
- Con menos va igual, pero lento: la prueba se hizo en un contenedor de 1 CPU.

**Tiempo estimado**: 5 minutos la primera vez (casi todo es descargar la imagen base y clonar el repo).

## Entorno de pruebas

Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno:**
- `entorno/Dockerfile` — describe la máquina: imagen base fijada (`python:3.13-slim`) y `git`. El
  repositorio del autor no va dentro de la imagen.
- `pruebas/pruebas.sh` — construye esa máquina, ejecuta la demo dentro, en limpio, y comprueba que la
  salida trae las cifras del vídeo. Es la prueba que pasó el material antes de publicarse.
- `traer_repo.sh` — clona el repositorio del autor en la revisión exacta del vídeo.
- `.env.example` — plantilla de las claves que necesite el material. Este material **no usa ninguna**:
  está vacía a propósito y se documenta para que no haya sorpresas.
- `datos/` — los dos ficheros de entrada que se usan en el vídeo, más el script que generó el CSV.

**Paso 1 — construir la máquina** (una sola vez; tarda un par de minutos porque descarga la imagen
base):
```bash
docker build -t repro-founder-skill:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en **solo
lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en `/tmp`):
```bash
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$PWD:/trabajo:ro" repro-founder-skill:local \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
```

**Paso 3 — o las dos cosas de una vez** con el script que usamos nosotros, que hace lo anterior y
además comprueba la salida:
```bash
bash pruebas/pruebas.sh
```

**Por qué así, y no de otra forma:** el contenedor no lleva nada tuyo dentro, la carpeta entra montada
como solo-lectura y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en tu máquina: lo
que falla en limpio es un fallo real, no un resto de tu entorno. El contenedor necesita **red solo para
clonar** el repositorio; lo que **no** tiene son tus datos.

**Detalle de nuestra ejecución, por si tu caso es distinto:** el motor Docker de esta máquina tenía
configurado además uno remoto, así que las órdenes se lanzaron con `--context default` para forzar el
local. Si en tu equipo solo hay un motor, déjalo como está (funciona igual).

## Pasos

1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd founder-skill
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
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `traer_repo.sh` | Clona `Jakeschincariol/founder-skill` en la revisión `fd9385b` y dice qué revisión es. |
| `datos/mi_negocio.json` | Los números del segundo caso del vídeo (un obrador de barrio), escritos a mano. |
| `datos/pricing.csv` | 40 respuestas de precio **sintéticas** (ver «Qué está probado y qué no»). |
| `datos/gen_pricing.py` | El script que generó ese CSV, con semilla fija: puedes regenerarlo igual. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y `git`, con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno, ejecuta la demo en limpio y comprueba el resultado. |
| `.env.example` | Plantilla de las claves que necesita el material (este no usa ninguna). |
| `paquete.json` | Ficha interna del repositorio didáctico: título, fecha y comando. |
| `material.json` | La ficha del índice: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: el problema, los pasos, el entorno de pruebas y el resultado esperado. |

### Qué hace cada script, paso a paso

- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes del vídeo, en ese orden. Mira qué
  trae el repositorio (`ls skills`), enseña el fichero de ejemplo `skills/founder-cfo/example.json` y
  calcula con `unit_economics.py` la contribución, el break-even y el margen; después el año uno mes a
  mes y la tabla de escenarios; luego repite el cálculo con **mis números**, escribe el informe en
  `founder/cfo.md` y pide el veredicto del plan (`compile.py --check`); a continuación el análisis de
  precio sobre el CSV (`van_westendorp.py`), el panel de 100 compradores (`panel.py`) y, al final, el
  plan compilado. Trabaja siempre sobre una copia en `/tmp`, así que no toca el repositorio clonado.
- **`traer_repo.sh`** — clona el repositorio del autor y hace `checkout` de la revisión `fd9385b`, la
  que se usó en el vídeo. Imprime la revisión y la fecha del último commit: así sabes qué estás
  ejecutando.
- **`entorno/Dockerfile`** — la máquina de pruebas: `python:3.13-slim` con `git`. No instala ningún
  paquete de Python porque el material no necesita ninguno, y no copia claves ni datos.
- **`pruebas/pruebas.sh`** — la prueba de verdad: construye la imagen, ejecuta la demo en un contenedor
  sin privilegios con la carpeta en solo lectura, y comprueba que la salida trae `Break-even: 186 cups a
  day`, `Break-even: 289 bandejas a day`, `-66%`, `Verdict: Not yet` y `0 answered`. Si falta alguna,
  sale con error y dice cuál.

## Resultado esperado

Primero, con el caso de ejemplo del propio repositorio:
```
Contribution: $4.76 (73%)
Break-even: 186 cups a day
Margin at plan: 38%
```

Y después, con los números del vídeo (el obrador de barrio), la comparación que da sentido a todo:
```
Break-even: 289 bandejas a day
Capacity: 90 bandejas a day
Profit margin at your plan: -66%
```

El veredicto del plan, que es lo que se puede comprobar desde un programa:
```
Verdict: Not yet
codigo de salida: 1
```

## Coste y credenciales

Nada: no hay claves, no hay cuenta y no hay servicio de pago. El repositorio es de licencia MIT y todo
corre en tu máquina.

## Solución de problemas

- **«command not found: git»** — estás ejecutando fuera del contenedor y sin `git` instalado; usa la
  imagen de `entorno/Dockerfile` o instala `git`.
- **Falla al clonar** — el contenedor necesita red para bajar el repositorio; si estás en una red
  corporativa, puede bloquear GitHub. Prueba `./traer_repo.sh` desde tu máquina.
- **`Permission denied` al escribir en `founder/`** — la demo escribe dentro de su copia en `/tmp`; si
  ejecutas los comandos a mano sobre la carpeta montada en solo lectura, fallará. Copia la carpeta.
- **`Verdict: Not yet` con código de salida 1** — no es un error: es el veredicto. La herramienta
  devuelve 1 cuando el plan no cierra, para que puedas usarlo en un script.
- **El panel dice `0 answered`** — es lo esperado sin agentes: ver el apartado siguiente.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Qué está probado y qué no

- **Probado (🟢):** los cuatro cálculos y el veredicto, ejecutados en `python:3.13-slim` sin
  privilegios, sobre la revisión `fd9385b` del repositorio. El CSV de precio se genera con
  `datos/gen_pricing.py` (semilla 11): **son datos sintéticos**, no una encuesta real. Lo que demuestra
  la demo es el cálculo sobre un fichero, no una investigación de mercado.
- **No probado (🟡):** el panel de compradores **no piensa solo**. `panel.py` reparte las fichas y lleva
  la cuenta, pero las respuestas las tienen que escribir agentes; en el vídeo se ve `0 answered` y así
  se dice, en pantalla y en la narración. Tampoco está probado con datos reales de un negocio: los
  números los pones tú, y si los pones inventados la herramienta te devuelve una certeza inventada.
- **Lo que este material no es:** contabilidad, impuestos, nóminas ni asesoría. Es aritmética de negocio
  para decidir antes de firmar.

## Licencia

El material de esta carpeta es MIT. El repositorio `Jakeschincariol/founder-skill` es de su autor,
también MIT: se clona, no se copia.
