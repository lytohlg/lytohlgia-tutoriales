# Un panel para vigilar tu red doméstica (Vantage)

Tienes el router, un NAS, una raspberry, una tele con Plex y alguna máquina virtual. Cada aparato
cuenta su estado en un sitio distinto y ninguno te avisa cuando algo se cae: te enteras porque lo
necesitabas y no estaba.

Vantage es un panel que se instala en una máquina tuya, comprueba esos aparatos por ti y guarda el
resultado. Este paquete es el entorno con el que se grabó el vídeo: la misma imagen, los mismos
comandos y las mismas pruebas.

## Qué vas a conseguir

1. Ver el panel arrancar en una máquina limpia: clave maestra, base de datos con sus migraciones y
   servidor escuchando en local.
2. Crear el primer administrador con un **código de un solo uso**, sin contraseña por defecto.
3. Listar los **doce tipos de integración** que trae y saber qué le pide a cada aparato.
4. Comprobar el **guardián de red**: el panel no puede apuntar a la propia máquina (`127.0.0.1`) ni a
   direcciones públicas, y sí acepta una dirección de tu red local. Un panel que hace peticiones por
   ti y guarda tus contraseñas no puede ser una puerta abierta.

## Requisitos

- Docker con el motor en marcha (la demo se ejecuta en un contenedor limpio, sin privilegios).
- Conexión a Internet la primera vez: al construir la imagen se descarga `python:3.12-slim` y se
  clona el repositorio del proyecto en un commit fijado.
- Hardware mínimo: **2 vCPU, 2 GB de RAM y 3 GB de disco libre**. La demo en sí usa menos de 300 MB
  de RAM; el resto es margen para Docker y la imagen.
- Nada más: no hace falta router, ni homelab, ni credenciales de ningún servicio.

## Entorno de pruebas

La prueba corre dentro de Docker. La imagen se construye desde `entorno/Dockerfile`, que parte de
`python:3.12-slim`, instala `git`, `curl` y el backend del proyecto en un **commit exacto**
(`803b47f65089329fbf369df2a0c931d770a87da3`, versión 0.1.1) y deja el código en `/opt/vantage`.

La demo se ejecuta después en un contenedor **sin privilegios**, como usuario sin privilegios, con
la carpeta del paquete montada en solo lectura: el script trabaja sobre una copia en `/tmp`. Todo
ocurre en `127.0.0.1`.

- Repositorio: <https://github.com/levi-xy/vantage> (licencia MIT)
- Imagen de partida: `python:3.12-slim`
- Fichero de construcción: `entorno/Dockerfile`

## Pasos

```bash
cd pruebas
bash pruebas.sh
```

Eso hace dos cosas: construye la imagen desde `entorno/Dockerfile` y ejecuta `demo.sh` dentro de un
contenedor limpio. Si prefieres hacerlo a mano, es equivalente a:

```bash
docker build -t repro-vantage-panel-homelab:local entorno
docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp \
  -v "$PWD:/origen:ro" repro-vantage-panel-homelab:local \
  bash -c 'cp -r /origen /tmp/paquete && cd /tmp/paquete && bash demo.sh'
```

Los pasos que ejecuta `demo.sh`, en el mismo orden que en el vídeo:

1. Generar la clave maestra con 32 bytes aleatorios (`/dev/urandom`) y una base de datos SQLite
   temporal.
2. Aplicar las migraciones con `alembic upgrade head`.
3. Arrancar el backend FastAPI con `uvicorn` y comprobar `http://127.0.0.1:8000/healthz`.
4. Crear el administrador con un código de un solo uso (`python -m app.cli setup-code`).
5. Pedir el catálogo de integraciones y ver los doce tipos.
6. Probar una dirección de red privada: la política la deja pasar (si no responde, se ve el error de
   conexión, no un rechazo de la política).
7. Probar `http://127.0.0.1:8000/healthz` y `https://example.com/`: el guardián las rechaza.

## Qué hace cada fichero

| Fichero | Para qué sirve |
|---|---|
| `demo.sh` | La demo completa, en el orden del vídeo. Se ejecuta dentro del contenedor y no necesita nada fuera de él. |
| `pruebas/pruebas.sh` | Construye la imagen y lanza `demo.sh` en un contenedor limpio. Es la prueba que hicimos nosotros. |
| `entorno/Dockerfile` | La máquina de pruebas: Python 3.12, `git`, `curl` y el backend del proyecto en un commit fijado. |
| `.env.example` | Las variables que usa la demo (`VANTAGE_MASTER_KEY_FILE`, `VANTAGE_DATABASE_URL`, `LAN_IP`) con valores de ejemplo. Ninguna es un secreto. |
| `material.json` | Ficha del paquete: título, licencia de uso y fecha de publicación. |
| `paquete.json` | Ficha interna con el comando y la imagen. No es necesario para reproducir la demo. |

## Resultado esperado

Al final de `demo.sh` la salida contiene, en este orden:

- `45 clave.key` — la clave son 32 bytes aleatorios que en base64 ocupan 44 caracteres más el salto
  de línea.
- Un JSON de `healthz` con el estado del panel.
- `codigo: <código>` y un JSON con el usuario administrador y su `csrf_token`.
- La lista de tipos de integración separada por comas (doce entradas).
- En el paso 6, una respuesta de prueba para la dirección privada (o su error de conexión).
- En el paso 7, dos respuestas del guardián rechazando `127.0.0.1` y la web pública, con el motivo
  en el mensaje.

## Coste y credenciales

- Coste: **0 €**. Todo es software libre (MIT) y corre en tu máquina.
- Credenciales: **ninguna**. No hay claves de API, ni cuentas, ni tokens. La contraseña que usa la
  demo (`Mi-Clave-Larga-2026`) es inventada y solo existe dentro del contenedor temporal.
- Necesita un servidor encendido 24 h si quieres el panel siempre disponible.

## Lo que este paquete NO demuestra (honestidad primero)

- **No** demuestra los avisos por Telegram: hacen falta un bot y una cuenta, y en la grabación no se
  envió ningún aviso.
- **No** demuestra el mapa de red visual: en la interfaz se dibuja a mano, caja por caja.
- **No** usa tu red: las pruebas se hacen contra `127.0.0.1` y contra una dirección privada de
  ejemplo, no contra tus aparatos.
- **No** mide precisión universal: es la versión 0.1.1 del proyecto, publicada hace un mes.

## Instalarlo de verdad en tu casa

```bash
curl -fsSLO https://github.com/levi-xy/vantage/releases/latest/download/compose.yml
export VANTAGE_BIND_ADDRESS=127.0.0.1
docker compose up -d
docker compose exec backend python -m app.cli setup-code
```

El contenedor de arranque genera la clave maestra, el token de Prometheus y un certificado
autofirmado, y no los regenera si ya existen. El panel queda en `https://127.0.0.1:8443`.

## Solución de problemas

- **`docker: command not found`** → instala Docker y comprueba que el motor está en marcha
  (`docker info`).
- **El `docker build` falla al clonar** → el commit fijado necesita conexión a Internet; revisa la
  red o vuelve a intentarlo.
- **`healthz` no responde** → el script espera hasta 30 segundos. Si el backend tarda más, mira el
  fichero `uvicorn.log` dentro del directorio temporal del contenedor: ahí está el error real.
- **`setup-code` no devuelve código** → suele ser que las migraciones no se aplicaron; vuelve a
  ejecutar `alembic upgrade head` y revisa la variable `VANTAGE_DATABASE_URL`.
- **La prueba de la dirección privada da timeout** → es normal si esa dirección no existe en tu red;
  lo que se demuestra es que la política **no la bloquea**. El bloqueo se ve en el paso 7.
- **La demo se queda a medias** → el contenedor se para al terminar; relanza `bash pruebas.sh`. No
  guarda estado entre ejecuciones.

## Límites que conviene saber antes de instalarlo

- Interfaz **solo en inglés**.
- El mapa de red se dibuja a mano.
- Versión **0.1.1**, proyecto de un mes: cuatro contenedores (arranque, backend, frontal, Prometheus).
- Si solo quieres un ping cada minuto, veinte líneas de Python te hacen el trabajo.
