# MiniMind en CPU: cuánto cuesta de verdad entrenar tu propia IA

Material reproducible del vídeo *"Entrenar tu propia IA sin GPU"*. Reproduce lo mismo que se ve en
pantalla: un preentreno **real** de MiniMind con unos pocos pasos, en CPU, con la pérdida medida del log.

## Qué demuestra

- Que el proyecto [jingyaogong/minimind](https://github.com/jingyaogong/minimind) entrena de verdad en
  CPU, sin tarjeta gráfica, sobre una muestra pequeña del dataset de preentreno.
- Que la pérdida baja y se estanca en pocos pasos: 100 pasos con 800 líneas no dan para más.
- Que el número de "3 yuanes y 2 horas" que repite el README **no** es lo que se mide aquí: es la
  estimación del autor con una GPU alquilada.

## Qué NO demuestra

- No entrena el modelo completo (1,27 M de líneas, 1,2 GB de datos, GPU y horas de reloj).
- No produce un asistente usable: con 100 pasos el modelo escupe texto sin sentido, y así se ve en el vídeo.

## Requisitos

- Docker (recomendado), o Python 3.12 con las dependencias de `entorno/Dockerfile`.
- `git` disponible dentro del entorno: la demo clona el proyecto original.
- Unos 2 GB de disco y 4 GB de RAM. No hace falta GPU: precisamente se ejecuta en CPU.
- No hace falta ninguna credencial ni clave de API.

## Qué vas a conseguir

Un log de entrenamiento real, con la pérdida por paso, y un resumen medido: pasos ejecutados, pérdida
inicial, final y mínima, tokens vistos y confirmación de que se ha entrenado en CPU.

## Entorno de pruebas

- Imagen: `repro-minimind-coste-real:local`, construida desde `entorno/Dockerfile`
  (Python 3.12 + torch CPU + transformers + tokenizers + datasets).
- Se ha reproducido en un contenedor limpio, sin GPU y sin acceso a ningún servicio externo salvo
  GitHub (para clonar) y el dataset local que acompaña al paquete.
- Máquina de referencia del vídeo: 2 vCPU y 6 GB, sin tarjeta gráfica.

## Pasos

1. Construye la imagen:

   ```bash
   docker build -t repro-minimind:cpu -f entorno/Dockerfile .
   ```

2. Lanza la demo (clona el proyecto en el commit del vídeo, prepara la muestra y entrena 5 pasos):

   ```bash
   docker run --rm -v "$PWD":/work -w /work repro-minimind:cpu bash demo.sh
   ```

3. Sin Docker, con las dependencias instaladas, basta con `bash demo.sh`. Para más pasos,
   `PASOS=10 bash demo.sh` (tarda más).

La demo tarda minutos: cada paso de entrenamiento en CPU son decenas de segundos, no milisegundos.

## Qué hace cada fichero

- `demo.sh` — clona el repo en el commit del vídeo, recorta la muestra, entrena unos pasos y llama a `medir.py`.
- `medir.py` — lee el log y saca pasos, pérdida inicial/final/mínima, tokens y aviso de GPU. Falla si el
  log no contiene ninguna línea de pérdida: no estima nada.
- `datos/muestra_200.txt` — 200 líneas del dataset de preentreno de MiniMind (Apache-2.0), en formato
  JSON Lines (una línea = un documento). Se incluye para no depender de una descarga de 1,2 GB.
- `entorno/Dockerfile` — Python 3.12 + torch CPU + transformers + tokenizers + datasets + git.
- `.env.example` — variables disponibles (`PASOS`, `SEGUNDOS`). No hace falta ninguna credencial.
- `paquete.json` — manifiesto del paquete (comando, imagen, salida esperada, versión).

## Resultado esperado

```
PASOS:  5
PERDIDA: 8.xx -> 7.xx  (minima 7.xx)
TOKENS: 13600
GPU:    0 (ejecución en CPU)
```

Con tan pocos pasos es normal que la última pérdida no baje de la primera; en ese caso `medir.py`
añade la línea `AVISO: la pérdida no bajó en esta ejecución` y sigue siendo un resultado válido.

Los valores exactos cambian con el número de pasos y con la máquina; el orden no. Si `PERDIDA:` no
aparece, la demo ha fallado y no hay nada que medir.

## Solución de problemas

- **`git: command not found`** — la imagen ya trae `git`; si ejecutas sin Docker, instálalo.
- **`ModuleNotFoundError: torch`** — estás fuera del contenedor y sin las dependencias: usa la imagen o
  instala `entorno/Dockerfile`.
- **`KO: el log no tiene ninguna línea de pérdida`** — el entrenamiento no llegó a arrancar dentro del
  tiempo límite. Sube `SEGUNDOS` (por ejemplo `SEGUNDOS=300 bash demo.sh`).
- **La pérdida no baja de forma monótona** — es normal con lotes de 8: hay ruido paso a paso. Mira la
  tendencia, no el paso suelto.
- **Se queda sin memoria** — reduce `PASOS` o `--batch_size` en `demo.sh`.

## Coste real medido

En una máquina de 2 vCPU y 6 GB, sin GPU: **100 pasos en 28 min 41 s**, pérdida de **8,88 a 7,15**,
**272.000 tokens** vistos. 0 € de GPU; la electricidad no está medida.

## Licencias

- Código de MiniMind: Apache-2.0 (se clona, no se copia aquí).
- Datos de la muestra: del dataset publicado por el autor del proyecto.
