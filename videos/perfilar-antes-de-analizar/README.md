# Mira qué esconde tu Excel antes de analizarlo con ydata-profiling

> Material del vídeo **Mira qué esconde tu Excel antes de analizarlo con ydata-profiling** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
Perfilar un fichero de ventas con suciedad conocida y leer las alertas antes de analizarlo

## Requisitos
**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/
- Python 3.10 a 3.13 (`python3 --version`). El paquete **no** funciona en 3.14 todavía.

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
docker --context default build -t repro-perfilar-antes-de-analizar:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script no puede tocar tus ficheros originales: trabaja sobre una copia en
`/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" repro-perfilar-antes-de-analizar:local bash -lc "set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh"
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
   cd perfilar-antes-de-analizar
   ```
2. Este material **no usa credenciales**: no hay claves que rellenar. (Si añades algo que las necesite,
   usa el patrón de `.env.example` → `.env`, que nunca se sube al repositorio.)
3. Ejecuta la demo (dentro del contenedor del paso 2; en tu máquina es lo mismo):
   ```bash
   bash demo.sh
   ```

## Qué hace cada fichero
| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | Los comandos del vídeo, en el mismo orden. Es el material en sí. |
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `material.json` | La ficha del índice del repositorio: título, fecha, enlace al vídeo y si pide claves. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |
| `datos/generar_datos.py` | Fabrica el CSV de ventas con los defectos contados de antemano y los apunta en `datos/manifest.json`. Es lo que convierte la demo en una prueba: hay un «esperado» con el que comparar. |
| `explorar.py` | Lo que te dice un vistazo rápido con pandas: forma, tipos y huecos totales. Sirve de contraste, no de enemigo. |
| `perfilar.py` | El comando del vídeo: lee el CSV y escribe `perfil.html` (informe para mirar) y `perfil.json` (el mismo contenido en datos). Con `--minimo` hace la versión reducida. |
| `alertas.py` | Lee el bloque `alerts` de `perfil.json` y lo imprime en una línea por hallazgo. No inventa: traduce el JSON a pantalla. |
| `ficha.py` | Imprime la ficha de una columna concreta (huecos, distintos, mínimo, máximo, ceros, negativos y valores más repetidos) sacada del mismo `perfil.json`. |
| `comparar.py` | Cierra el círculo: pone lo que metió `generar_datos.py` al lado de lo que encontró el perfil. Si los números coinciden, el perfil sirve. |
| `umbral.py` | Usa el perfil desde un script: recibe el JSON y un umbral de huecos, lista las columnas que lo pasan y sale con código 1 si hay alguna. Es la pieza que permite validar un fichero en un cron o en un CI sin que nadie lo mire. |
| `fechas.py` | Enseña el problema que el perfil **no** resuelve solo: el fichero mezcla tres formatos de fecha y el mismo dato se puede leer día/mes o mes/día. Cuenta cuántas filas cambian según cómo se lea. |

### Ficheros que se generan al ejecutar (no están en el repositorio)
- `datos/ventas_2026.csv` — 60.300 filas de ventas con suciedad contada. Se genera con
  `datos/generar_datos.py` (semilla fija: mismo fichero siempre) y **no se sube** porque pesa 2,7 MB
  y porque el interés está en el generador, no en el resultado.
- `datos/manifest.json` — el «esperado»: cuántos huecos, duplicados y negativos se metieron.
- `perfil.html` / `perfil.json` / `perfil_min.html` / `perfil_min.json` — la salida del perfilador.

### Qué hace cada script, paso a paso
- **`demo.sh`** — no tiene nada de decorativo: es la lista de órdenes que se ejecutan en el vídeo,
  en ese orden. Si el vídeo hace algo que no está aquí, el material está mal. Se puede leer entero
  antes de ejecutarlo (son pocas líneas) y no pide permisos ni toca ficheros fuera de su carpeta.
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

Salida real de la última ejecución en limpio (60.300 filas, 1 CPU). Los tiempos varían con la máquina;
los recuentos, no: el generador es determinista.

```
leído:        0.1 s   (60300 filas)
perfilado:    0.2 s
escrito:     82.4 s
informe:    perfil.html      (4,1 MB)
resumen:    perfil.json      (9,4 MB)

2 alertas
  · Dataset has 300 (0.5%) duplicate rows
  · [importe] 1200 (2.0%) missing values

columna canal   (tipo detectado: Categorical)
  valores distintos      6
    'WEB '         10166
    'Tienda'       10086
    'Web'          10076

defecto                            metido  detectado   coincide
huecos en importe                    1200       1200         sí
huecos en cliente                      40         40         sí
huecos en fecha                        90         90         sí
filas duplicadas enteras              300        300         sí
importes negativos (abonos)           700        700         sí

modo --minimo: escrito: 5.4 s   (frente a los 82,4 s del informe completo)
```

Y el hallazgo incómodo, que sale de `fechas.py`: **7.872 de las 60.300 filas cambian de fecha según
se lea día/mes o mes/día**, y el informe se queda con una de las dos lecturas sin avisar.

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
