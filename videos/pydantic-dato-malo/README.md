# El validador dijo OK y guardó una fecha que no existe: pydantic

> Material del vídeo **El validador dijo OK y guardó una fecha que no existe: pydantic** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Que un CSV con filas malas deje de entrar en tu programa sin que nadie se entere: seis pedidos,
un validador a mano que los da todos por buenos (71,40 € de total), un modelo de pydantic que
acepta dos y rechaza los otros cuatro con el campo y el motivo (42,50 €).

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
docker --context default build -t repro-pydantic-dato-malo:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" python:3.12-slim bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd pydantic-dato-malo
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
| `datos/pedidos.csv` | Seis pedidos inventados; cuatro tienen un defecto distinto. |
| `datos/pedidos_typo.csv` | La misma tabla con la columna escrita `importee`. |
| `mirar_csv.py` | Enseña las filas en crudo, sin validar nada. |
| `valida_manual.py` | El validador a mano: `if`, `re`, `float`. Acepta las seis filas. |
| `modelo.py` | El mismo control declarado como modelo de pydantic (`extra="forbid"` incluido). |
| `normaliza.py` | Dos reglas propias: coma decimal (`"12,50"`) y estado en mayúsculas. |
| `revisar_lote.py` | El id repetido: lo que un modelo no ve, porque valida fila a fila. |
| `limpia.py` | El flujo real: escribe `pedidos_ok.csv` (lo único que debería llegar a la BD) e `informe.csv` (una fila por problema). Los dos se generan al ejecutar; no se versionan. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |
| `.gitignore` | Los ficheros que genera la demo (`pedidos_limpios.csv`, `pedidos_ok.csv`, `informe.csv`, `__pycache__/`): salidas de ejecución, no fuentes. Se regeneran cada vez, así que no se versionan. |

### Ficheros que genera la demo (no están en el repo)

- `pedidos_limpios.csv` — lo escribe `valida_manual.py` con todo lo que su validación da por bueno.
- `pedidos_ok.csv` — lo escribe `limpia.py` con los pedidos que pasan el modelo, ya con tipos.
- `informe.csv` — lo escribe `limpia.py` con una fila por problema: línea, campo, motivo y valor.

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Recorre los seis pasos: mirar el CSV crudo, el validador manual, la instalación,
  el modelo, la columna mal escrita, las dos reglas propias y el id repetido.
- **`valida_manual.py`** — el validador que cualquiera escribiría: comprueba que el cliente no esté
  vacío, que el importe sea un número (cambiando la coma por un punto), que la fecha case con una
  expresión regular y que el estado sea uno de los tres. No compara filas entre sí ni comprueba que
  la fecha exista en el calendario.
- **`modelo.py`** — la misma validación declarada: tipos (`int`, `Decimal`, `date`, `EmailStr`),
  restricciones (`gt=0`, `le=5000`, `min_length=2`), un dominio cerrado con `Literal` y
  `extra="forbid"` para que una columna que no está en el modelo no se ignore en silencio.
- **`normaliza.py`** — añade lo que un contrato no trae: `field_validator(mode="before")` para el
  «12,50» de Excel y para admitir `PAGADO` guardándolo en minúsculas.
- **`revisar_lote.py`** — cuenta los ids que pasan el modelo y denuncia los repetidos. Es el límite
  explícito: pydantic valida un registro, no el lote.
- **`entorno/Dockerfile`** — construye la máquina de pruebas. Empieza de una imagen base oficial
  con la versión fijada (nada de `latest`, para que mañana funcione igual) e instala
  `pydantic==2.12.3` y `email-validator==2.3.0`. No copia claves ni tus datos.
- **`pruebas/pruebas.sh`** — la prueba de verdad, en dos pasos: construye la imagen de
  `entorno/Dockerfile` y ejecuta la demo dentro de un contenedor limpio, con la carpeta montada en
  solo lectura y una copia de trabajo en `/tmp`. No escribe nada fuera del contenedor.

## Resultado esperado
El script termina con las seis filas clasificadas: dos válidas y cuatro con el motivo concreto.

```
== 1. El validador manual: dice que todo está bien ==
filas leídas:      6
pedidos válidos:   6
pedidos rechazados:0
TOTAL: 71.40 EUR

== 3. El mismo CSV, con un modelo declarativo ==
pedidos válidos:    2
pedidos con fallos: 4
  fila 3:
    email    value is not a valid email address … (recibido: 'luis@example')
    importe  Input should be a valid decimal  (recibido: '12,50')
  fila 4:
    fecha    Input should be a valid date … day value is outside expected range  (recibido: '2026-02-31')
  fila 5:
    importe  Input should be greater than 0  (recibido: '-5.00')
  fila 6:
    estado   Input should be 'pagado', 'pendiente' or 'cancelado'  (recibido: 'PAGADO')
TOTAL de los válidos: 42.50 EUR
```

## Límites que conviene saber antes de usarlo
- Los mensajes de error están en inglés.
- Un «12,50» **no** se convierte solo: con `Decimal` es un error de formato. Por eso `normaliza.py`
  lo arregla con `field_validator(mode="before")`, que es código tuyo, no magia del modelo.
- `extra="forbid"` no está activo por defecto: si no lo escribes, la columna desconocida se ignora.
- Pydantic valida datos **en ejecución** y mejora el autocompletado del editor; no sustituye a
  Pyright ni a mypy, que revisan el código sin ejecutarlo.
- No es un ORM: la unicidad del lote (`revisar_lote.py`) sigue siendo responsabilidad tuya.

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
