# MLflow: nunca pierdas el modelo que funcionó

> Material del vídeo **MLflow: nunca pierdas el modelo que funcionó** del canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA).
> Aquí está exactamente lo que se ejecuta en el vídeo, listo para que lo reproduzcas tú.

## El problema

Probaste tres configuraciones del modelo. La del martes daba mejor error que la del lunes, pero
sobrescribiste el fichero. Ahora hay tres archivos que se llaman `final` y ninguno dice con qué
parámetros se entrenó. En un cuaderno apuntaste «alpha 0.1, rmse 53», pero no sabes si ese 53 salió
con la misma partición de datos que el 55 de hoy.

El coste no es el tiempo de reentrenar: es **decidir con datos que ya no tienes**. Y el fallo caro no
es perder el modelo, es mandar a producción el peor de los tres creyendo que era el mejor.

## Qué vas a conseguir

Cada prueba de modelo queda registrada con sus parámetros, su métrica, el modelo guardado y una
ruta para recuperarlo. Al final puedes preguntar «¿cuál falló menos?», cargar **exactamente** ese
modelo y ponerle nombre al ganador. Todo en local, en una carpeta, sin cuenta y sin tarjeta.

Salida esperada al terminar la demo:

```
VERIFICADO: 3 pruebas registradas · ganadora ridge-alpha-0.1 · rmse 53.010 · modelo recuperado y registrado como version 1
```

## Coste y credenciales

- **Coste**: cero. Todo corre en tu máquina, sin cuenta, sin tarjeta y sin servicios de pago.
- **Credenciales**: ninguna. No hay claves, ni tokens, ni login. La única descarga es la imagen base
  de Python y los paquetes de pip.
- **Datos**: el dataset de diabetes viene dentro de scikit-learn; no sales a ninguna API.

## Requisitos

**Software**
- Sistema: Linux, macOS o Windows con WSL2 (los comandos son de shell).
- Docker instalado (`docker --version`, versión 20.10 o superior) — si no lo tienes:
  https://docs.docker.com/get-docker/

**Hardware** (mínimo para el entorno de pruebas)
- 2 GB de RAM libres, 1 CPU y 1,5 GB de disco libre para la imagen del contenedor.
- La prueba se hizo con 1 CPU; con menos va igual, pero lento.

**Tiempo estimado**: 5-10 minutos la primera vez (incluye descargar la imagen base y las dependencias).

## Entorno de pruebas

Todo lo que sale en el vídeo se probó **en un contenedor limpio**, y aquí tienes ese mismo entorno
para repetirlo tú. No hay nada que instalar en tu sistema: la máquina de pruebas se describe en un
fichero y se construye con una orden.

**Ficheros que forman el entorno**:
- `entorno/Dockerfile` — describe la máquina: Python 3.13, MLflow 3 y scikit-learn.
- `pruebas/pruebas.sh` — construye esa máquina, ejecuta la demo dentro y comprueba la salida.
- `scripts/` — los cinco scripts de la demo (entrenar, comparar, recuperar, registrar, filtrar).
- `.env.example` — las dos variables de entorno **opcionales** que leen los scripts
  (`MLFLOW_TRACKING_URI` y `MLFLOW_ARTIFACT_ROOT`) con sus valores por defecto. No hace falta
  copiarlo para que la demo funcione: está para que veas qué se puede cambiar y dónde. Si lo copias
  a `.env`, exporta esas variables antes de ejecutar `demo.sh`.

## Pasos

**Paso 1 — construir la máquina** (una sola vez):
```bash
docker --context default build -t repro-mlflow-experimentos-que-no-se-pierden:local entorno
```

**Paso 2 — ejecutar la demo dentro**, sin privilegios de root y con esta carpeta montada en
**solo lectura** (el script trabaja sobre una copia en `/tmp`):
```bash
docker --context default run --rm --user 1000:1000 --workdir /tmp -e HOME=/tmp -v "$PWD:/trabajo:ro" \
  repro-mlflow-experimentos-que-no-se-pierden:local \
  bash -lc 'set -e; mkdir -p /tmp/repro && cp -r /trabajo/. /tmp/repro/ && cd /tmp/repro && bash demo.sh'
```

**Paso 3 — o todo de una vez** con el script que usamos nosotros, que hace lo anterior y además
comprueba que la salida es la esperada:
```bash
bash pruebas/pruebas.sh
```

El `--context default` fuerza el motor Docker local — útil si tienes configurado además uno remoto;
si en tu equipo solo hay uno, funcionará igual con o sin él.

## Qué hace cada script

1. `scripts/entrenar.py` — entrena tres Ridge (alpha 0.1, 1.0 y 10.0) sobre el dataset de diabetes
   que trae scikit-learn. Por cada uno abre una *run*, registra parámetros (`alpha`), la métrica
   (`rmse`), guarda el modelo y anota su ruta como etiqueta `model_uri`.
2. `scripts/comparar.py` — pregunta a MLflow cuál es la mejor run por `metrics.rmse` y saca la tabla.
3. `scripts/recuperar.py` — elige la mejor run, lee la etiqueta `model_uri` y carga ese modelo para
   predecir cuatro casos. No se elige ningún fichero a mano.
4. `scripts/registro.py` — registra el modelo ganador con un nombre (`progresion-diabetes`) y muestra
   la versión que le asigna el registro.
5. `scripts/filtrar.py` — filtra las runs por parámetro (`params.alpha != '0.1'`), que es lo que hace
   falta cuando hay cincuenta pruebas y no tres.

## Resultado esperado

- `alpha=0.1  rmse=53.010` es la run ganadora: el error medido sobre la partición de validación.
- `models:/m-<id>` es la ruta del modelo en esta instalación local. Es lo que se guarda y lo que se
  carga después; la ruta `runs:/<run>/modelo` sigue funcionando por compatibilidad, pero la que
  devuelve `log_model` en MLflow 3 es `models:/`.
- `modelo registrado: progresion-diabetes · versión 1` es el registro: un historial de versiones con
  nombre, **no** un despliegue. Cada vez que registres, sube la versión.

## Límites (lo que este material NO hace)

- **No optimiza nada.** Compara lo que tú lanzas; si tus parámetros son malos, la tabla será un
  registro ordenado de modelos malos.
- **No dice si el modelo es bueno.** Dice cuál falló menos con *esta* métrica y *esta* partición.
  Cambiar la métrica o la partición a mitad invalida la comparación.
- **No es una plataforma de despliegue.** El registro de modelos numera versiones; servir el modelo
  es otro trabajo (y otro vídeo).
- **Con varias personas escribiendo a la vez**, el fichero SQLite se queda corto: para un equipo,
  MLflow propone un servidor de seguimiento con base de datos propia.
- **Modelos serializados**: en MLflow 3, algunos tipos (por ejemplo los bosques aleatorios) exigen
  declarar los tipos en los que confías al guardarlos. Si te sale ese aviso, no es un fallo del
  material: es la política de serialización segura.

## Si algo va mal: problemas y errores

- `No such file or directory: mlflow.db` → estás ejecutando `demo.sh` desde otra carpeta; el script
  hace `cd` a la suya, pero si lo copiaste a mano, comprueba que `scripts/` está al lado.
- La tabla sale vacía → se borró `mlflow.db` entre pasos; vuelve a empezar con `bash demo.sh`.
- Error de versión de MLflow → este material se probó con `mlflow>=3,<4`.

## Créditos y licencia

Material didáctico del canal @lytohlgIA. La herramienta es [MLflow](https://github.com/mlflow/mlflow)
(Apache-2.0); aquí solo se muestra cómo usarla. Los scripts de esta carpeta son míos y puedes
copiarlos, cambiarlos y romperlos a gusto.
