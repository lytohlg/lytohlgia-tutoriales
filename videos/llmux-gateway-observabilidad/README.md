# llmux — ver qué viaja de verdad al proveedor del modelo

## El problema

Tienes un agente que llama a un modelo y contesta mal. Cambias el prompt, cambias el
modelo, reinicias... y sigues sin saber **qué se envió**. La petición real no es la que
escribiste: la librería añade mensajes de sistema, reescribe el nombre del modelo, mete
cabeceras y a veces reenvía tu clave a donde no toca.

Los tres apaños de siempre no bastan: los `print` en tu código solo ven tu parte, un proxy
genérico devuelve ruido y la factura del proveedor llega tarde y sin el cuerpo de la petición.

## Qué vas a conseguir

Un gateway local delante del proveedor que guarda cada intercambio en SQLite y te deja
comprobar, con una consulta, cuatro cosas que normalmente se suponen:

- qué modelo pediste y qué modelo salió hacia el proveedor;
- qué cabecera añadió el gateway y cuál no;
- si tu credencial viajó al proveedor o se quedó en casa;
- cuántas peticiones rechazó por no llevar clave (401).

`llmux` es un gateway en Go, de un solo binario, que escucha en local y reenvía a la API que
le digas. Habla el dialecto de OpenAI y el de Ollama, admite mapa de modelos, cabeceras
fijas, lista de claves y guarda cada petición y cada respuesta en SQLite. Es útil cuando
quieres observar sin cambiar el código de tu agente: le cambias la URL base y ya está.
Ventaja: no toca tu aplicación y no depende de ningún servicio en la nube. Límite honesto:
añade un salto de red, y lo que midas es lo que ve el gateway, no lo que hace el proveedor
por dentro.

Repo: https://github.com/rnapoles/llmux (MIT).

## Requisitos

- Docker (probado con Docker Engine 29 y contexto `default`; también vale Docker Desktop).
- 2 GB de RAM libres y unos 2 GB de disco la primera vez (compila el binario de Go).
- Nada de claves reales: la demo usa un proveedor falso que corre dentro del contenedor.

## Entorno de pruebas

Todo se ejecuta dentro de un contenedor construido desde `entorno/Dockerfile`
(`golang:1.26-bookworm` + python3 + sqlite3 + curl + el SDK de OpenAI). La carpeta se monta
en solo lectura y se copia a `/tmp` para trabajar, así que la demo no puede tocar tu copia.
No hay red hacia ningún proveedor real: el «proveedor» es `scripts/upstream.py`, que escucha
en `:9000` y devuelve siempre la misma respuesta.

## Pasos

```bash
# 1. construir el entorno (la primera vez tarda unos minutos)
docker --context default build -t repro-llmux-observabilidad:local entorno

# 2. ejecutar la demo completa dentro de un contenedor limpio
bash pruebas/pruebas.sh
```

Si quieres hacerlo a mano, dentro del contenedor: `bash demo.sh`.

## Qué hace cada fichero

- `demo.sh` — la demo de principio a fin: arranca, hace las peticiones, consulta la base y comprueba.
- `entorno/Dockerfile` — el entorno reproducible (compila llmux desde su repo).
- `pruebas/pruebas.sh` — construye el entorno, ejecuta `demo.sh` en contenedor limpio y verifica la salida.
- `scripts/arranque.sh` — arranca el proveedor falso y el gateway con la configuración de la demo.
- `scripts/pide.sh` — las peticiones de la demo, un caso por escenario (`sin-clave`, `con-clave`, `consulta`).
- `scripts/cliente.py` — un cliente real con el SDK de OpenAI contra el gateway (recibe la clave por argumento).
- `scripts/upstream.py` — el proveedor falso: responde siempre lo mismo y apunta lo que recibe.
- `scripts/comprobar.py` — lee la base y falla si lo que dice el vídeo no se cumple.
- `docs/guion-resumen.md` — el recorrido del vídeo, para seguirlo sin mirar la pantalla.
- `.env.example` — las variables que admiten los scripts (ninguna es obligatoria).

## Resultado esperado

La demo termina con una línea que empieza por `VERIFICADO:` y contiene, como mínimo:

```
modelo pedido reescrito en el cuerpo reenviado · cabecera X-Team inyectada · credencial del cliente no reenviada
```

Antes de esa línea verás las tres consultas a SQLite: el estado y el modelo de cada
intercambio, el mapeo del modelo medido como dos booleanos (0 = no aparece, 1 = aparece) y la
credencial medida igual, en la entrada (1) y en la salida (0).

## Coste / credenciales

Cero coste y cero credenciales reales: el proveedor es falso y local. La clave que usa la
demo es de juguete y solo sirve para que el gateway enseñe cómo la quita antes de reenviar.
Si algún día apuntas el gateway a un proveedor real, el gasto lo fija tu cuenta con ese
proveedor, no esta herramienta.

## Solución de problemas

- **`docker: command not found`** → instala Docker Engine y usa `--context default`.
- **El build falla al compilar** → necesita red la primera vez: clona el repo de llmux y baja los módulos de Go.
- **`gateway en :8095` no aparece** → el puerto está ocupado; para los procesos con `pkill -x llmux` y repite.
- **`VERIFICADO` no aparece** → mira antes la línea `FALLO:` de `scripts/comprobar.py`: dice exactamente qué no cuadró.
- **Todo va pero la tabla está vacía** → el gateway no arrancó; mira `llmux.log` en la carpeta de trabajo.
