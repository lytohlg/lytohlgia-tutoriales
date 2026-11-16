# El programa va, hasta que llega un dato con otra forma

Un programa de facturación y stock, escrito en Python, que funciona con los datos de prueba.
En cuanto alguien mete una cifra que viene de un Excel o un campo que llega vacío, revienta en
una línea que no tiene nada que ver con el sitio por donde entró el dato.

Casi nunca es un error de lógica. Es un error de **forma**: el dato no tiene la forma que la
función espera. Y se puede ver **antes de ejecutar**.

Este material reproduce ese caso, con el proyecto entero, el fallo real y el arreglo. Es el mismo
orden que sigue el vídeo.

## Qué vas a conseguir

- Ver con tus ojos los **cuatro fallos de forma reales** de un proyecto pequeño (un entero donde
  se prometió texto, un camino sin `return`, un `None` multiplicado y un `"120"` pasado como
  entero) **sin ejecutar el programa**.
- Leer un aviso de mypy y saber qué te está diciendo: fichero, línea, tipo encontrado y tipo
  esperado.
- Aplicar el arreglo (un parche real, no una edición a mano) y comprobar que el programa queda
  limpio y sigue haciendo lo mismo: `105`, `37.5`, `6`.
- Entender el límite del código viejo sin anotaciones y cómo se adopta la herramienta por partes
  sin parar el proyecto.

## Requisitos

- **Docker** (probado con Docker 24+; vale cualquier motor compatible, también en otro contexto).
- **2 GB de RAM libres, 2 vCPU y 2 GB de disco** para la imagen base y las ruedas de mypy. La demo
  entera tarda menos de un minuto; no compila nada.
- Si lo haces a mano sin Docker: **Python 3.12** y `mypy` (`pip install mypy`). El vídeo se grabó
  con mypy **2.4.1**.
- No hay servidor, ni cuenta, ni claves.

## Entorno de pruebas

Todo se ejecuta dentro de un contenedor construido con **`entorno/Dockerfile`** (imagen base
`python:3.12-slim` + las ruedas de mypy en `/opt/wheels`, para poder instalar **sin red**). El
contenedor corre sin privilegios, con la carpeta montada en **solo lectura** y una copia de trabajo
en `/tmp`: la demo no puede tocar tu copia original.

Hardware mínimo: **2 GB de RAM, 2 vCPU, 2 GB de disco**. La imagen se construye una vez y queda
cacheada.

## Pasos

```bash
cd mypy-tipos-antes-de-ejecutar
bash pruebas/pruebas.sh        # construye el entorno desde entorno/Dockerfile y ejecuta la demo
```

O a mano, si ya tienes mypy instalado:

```bash
cd proyecto && mypy .           # 4 errores en 3 ficheros, sin ejecutar nada
python main.py                  # el fallo real, con el dato de verdad
cd ..                            # el arreglo se aplica con patch, no editando a mano
cp -r proyecto /tmp/arreglado && cd /tmp/arreglado && patch -p1 < ../arreglo.txt
mypy . && python main.py        # limpio: el programa hace su trabajo
cd .. && cd legacy && mypy --strict .   # el código viejo: sin anotaciones no hay nada que mirar
```

## Qué hace cada fichero

- **`demo.sh`** — la demo completa, en el mismo orden que el vídeo (punto de partida, fallo real,
  aviso con contexto, arreglo, resultado y código viejo).
- **`pruebas/pruebas.sh`** — la prueba que se hizo antes de publicar: construye el entorno y ejecuta
  `demo.sh` en un contenedor limpio, sin privilegios y con la carpeta en solo lectura.
- **`entorno/Dockerfile`** — define el entorno reproducible: Python 3.12 y las ruedas de mypy.
- **`arreglo.txt`** — el parche, en formato diff unificado, que corrige los cuatro fallos de forma.
  Se aplica con `patch -p1`; no se edita a mano.
- **`proyecto/main.py`** — el punto de entrada del programa de facturación y stock.
- **`proyecto/stock.py`** — descuenta unidades del stock; recibe la cantidad como entero.
- **`proyecto/facturas.py`** — busca el precio de un artículo y calcula el importe de la línea.
- **`proyecto/informe.py`** — resume las ventas del día en texto.
- **`legacy/limpieza.py`** — un script viejo, sin anotaciones, que sigue funcionando: sirve para ver
  qué hace mypy con el código que no declara tipos.
- **`legacy/ventas.csv`** — los datos que lee `limpieza.py` (inventados, sin datos personales).
- **`paquete.json`** — la ficha del material: slug, título, fecha de publicación, comando de prueba
  y salida esperada.
- **`.env.example`** — la única variable que admiten los scripts (`DOCKER`, para elegir el contexto
  del motor). Por defecto no hace falta tocar nada.

## Resultado esperado

Salida de la primera orden (la del vídeo):

```
informe.py:11: error: Incompatible return value type (got "int", expected "str")  [return-value]
informe.py:14: error: Missing return statement  [return]
facturas.py:9: error: Unsupported operand types for * ("None" and "int")  [operator]
main.py:12: error: Argument 1 to "stock_restante" has incompatible type "str"; expected "int"  [arg-type]
Found 4 errors in 3 files (checked 4 source files)
```

Y al final del arreglo:

```
Success: no issues found in 4 source files
Quedan 105 unidades
Importe de la línea: 37.5
Resumen de ventas: 6
```

## Coste / credenciales

**Coste: cero.** No hay API de pago, ni cuenta, ni claves, ni límites de uso. Todo corre en tu
máquina dentro de un contenedor. La única "credencial" es tener Docker instalado.

## La herramienta

[mypy](https://github.com/python/mypy) — comprobador de tipos para Python. **No ejecuta tu
programa: lo lee.** Parte de las anotaciones que ya están en el código (`total: int -> int`,
`-> float | None`) y sigue lo que le pasa a cada dato por dentro de tus funciones.

- **Qué es**: un paquete de Python (Apache-2.0 / MIT en su núcleo, mantenido por la Python
  Typed Summit community), más de 20.000 estrellas en GitHub.
- **Para qué sirve**: detectar que un sitio espera un número y recibe un texto, o que usas como
  número algo que puede ser `None`, sin esperar a que ocurra en producción.
- **Cómo funciona**: lee el árbol del código, anota cada expresión con su tipo y comprueba la
  compatibilidad en cada llamada, asignación y retorno. Los avisos salen con `fichero:línea`.
- **Cuándo usarlo**: cuando el código lo toca más de una persona, lo llama otro módulo o lo
  despliega alguien que no eres tú. En un script de usar y tirar es papeleo.
- **Ventajas**: cero cambios en el programa (solo anotaciones), se puede ir fichero a fichero,
  los avisos son accionables y el comando se puede meter en lo que ya ejecutas antes de subir.
- **Límites**: no encuentra errores de lógica, no valida datos que llegan de fuera y no sustituye
  a los tests. Con librerías sin tipos avisa de que no puede mirarlas.

## El código del vídeo

Lo que hay que recordar de los cuatro errores:

1. **`informe.py:11`** — la función declara que devuelve texto y devuelve un número.
2. **`informe.py:14`** — hay un camino en el que no devuelve nada (falta el `return`).
3. **`facturas.py:9`** — `buscar_precio` puede devolver `None`, y `None * 3` no se puede hacer.
4. **`main.py:12`** — se pasa el texto `"120"` donde la función espera un entero.

Los cuatro se arreglan sin tocar la lógica del programa: se corrige la forma. El programa hacía lo
mismo antes y después; lo que cambia es que ahora el compilador de tipos lo sabe.

## Solución de problemas

- **`docker: command not found`** → instala Docker o define el motor: `DOCKER="docker --context
  mi-contexto" bash pruebas/pruebas.sh`.
- **`Cannot connect to the Docker daemon`** → el motor no está arrancado, o tu usuario no está en
  el grupo `docker`.
- **`permission denied` al copiar a `/tmp`** → el contenedor corre como usuario 1000; en Linux,
  comprueba que la carpeta es legible por otros (`chmod -R a+r .`).
- **`mypy: error: Cannot find implementation for ...`** → la librería no trae tipos; es justo el
  caso que explica la sección de límites. No es un fallo de este material.
- **`patch: **** malformed patch`** → estás aplicando el parche desde otra carpeta; usa `patch -p1`
  dentro de la copia del proyecto, como en los pasos.

## Notas de honestidad

- El número de errores (4), el código de salida (1) y la salida del programa arreglado (105, 37.5,
  6) son los que produce la ejecución real en este contenedor, no una narración.
- La instalación del vídeo se hace **desde ruedas descargadas** (`/opt/wheels`), para que se pueda
  ver sin red. En tu máquina, `pip install mypy` hace lo mismo bajándolas de PyPI.
- Ejemplo didáctico: los datos (catálogo, ventas) son inventados y no hay ningún dato personal.

— @lytohlgIA
