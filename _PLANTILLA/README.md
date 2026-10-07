# TÍTULO DEL VÍDEO

> Material del vídeo **TÍTULO DEL VÍDEO** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## Qué vas a conseguir
(una frase: qué consigue quien lo ejecute, en resultados y no en herramientas)

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
Todo lo de este vídeo se probó en un contenedor limpio, y aquí tienes ese mismo entorno para
repetirlo. El fichero `entorno/Dockerfile` describe la máquina; `pruebas/pruebas.sh` la construye
y ejecuta la demo dentro.

1. Construye el entorno (una sola vez):
   ```bash
   docker build -t repro-slug-del-video:local entorno
   ```
2. Ejecuta la demo en un contenedor limpio, sin privilegios y con la carpeta en **solo lectura**:
   ```bash
   docker run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp      -v "$PWD:/trabajo:ro" repro-slug-del-video:local      bash -lc 'mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
   ```
3. O todo de una vez con el script que usamos nosotros:
   ```bash
   bash pruebas/pruebas.sh
   ```

Por qué así: el contenedor no lleva tus datos dentro, la carpeta va montada solo lectura (el script
no puede tocar el original) y la copia de trabajo se hace en `/tmp`. Si funciona ahí, funciona en
tu máquina.

## Pasos
1. Copia esta carpeta a tu máquina y entra en ella:
   ```bash
   cd slug-del-video
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
| `entorno/Dockerfile` | La máquina donde se prueba: imagen base y dependencias con versiones fijadas. |
| `pruebas/pruebas.sh` | Construye ese entorno y ejecuta la demo en limpio. Es la prueba real previa a publicar. |
| `.env.example` | Plantilla de las claves que necesita el material (se copia a `.env`, que nunca se sube). |
| `paquete.json` | Ficha técnica del material para el índice del repositorio. |
| `README.md` | Esto: los pasos, el entorno de pruebas y el resultado esperado. |

## Resultado esperado
(pega aquí la salida REAL, la que has visto tú)

## Coste y credenciales
(nada, o qué servicio hace falta y cuánto cuesta)

## Solución de problemas
- **«command not found»**: te falta la herramienta del paso 1; instálala y vuelve a empezar.
- **Error de permisos**: ejecuta desde tu carpeta de usuario, no desde rutas del sistema.
- **Falla la descarga**: comprueba tu conexión; si usas una red corporativa, puede bloquear salidas.
- Sigue con dudas: deja un comentario en el vídeo y lo miro.

## Licencia
MIT — puedes usar, modificar y distribuir este código libremente. Ver `LICENSE` en la raíz del
repositorio.
