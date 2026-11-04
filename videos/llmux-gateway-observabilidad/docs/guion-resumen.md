# Guion (resumen por escena)

01 · concept   · EL PROBLEMA
    Tu agente llama al modelo y la respuesta no es la que esperabas. Y no tienes ni idea de qué se envió por el camino.
02 · terminal  · EL RESULTADO
    Esto es lo que voy a tener en pantalla veinte segundos después de empezar: el registro exacto de lo que llegó al proveedor. Yo pedí el modelo gpt-4. Al proveedor le llegó gpt-4o-mini, con una cabecera que he inyectado yo, y sin mi clave. Esto no es documentación: es lo que viajó de verdad por el cable.
03 · concept   · A QUIÉN LE DUELE
    Y esto le pasa a cualquiera que tenga un agente en producción. Al que monta un asistente sobre sus documentos, al que cambia de modelo para ahorrar, al que recibe una factura del proveedor con un número que no cuadra. Todos acaban igual: poniendo prints dentro del código para adivinar qué se está enviando.
04 · bullets   · HOY SE HACE ASÍ
    Hoy hay tres apaños, y los he usado los tres. Uno: imprimir la petición dentro de tu código, que solo funciona para tu código y no para lo que añade la librería por debajo. Dos: un proxy general, que te devuelve un tráfico enorme que no sabes leer. Y tres: mirar la factura del proveedor, que llega al día siguiente y sin el cuerpo de la petición.
05 · concept   · LA HERRAMIENTA
    Lo que he encontrado se llama llmux. Es un binario pequeño, escrito en Go, que se pone en medio: tu agente le habla a él, y él habla con el proveedor. Todo lo que pasa por el medio lo deja registrado. El repositorio está en github, barra rnapoles, barra llmux, y es de licencia MIT.
06 · bullets   · QUÉ HACE
    Hace cuatro cosas que importan. Emula la API de OpenAI y también la de Ollama, así que tus clientes no cambian ni una línea. Reescribe el nombre del modelo, para poder probar uno barato sin tocar tu código. Añade cabeceras y no reenvía tu clave. Y guarda cada intercambio, petición y respuesta, en una base de datos SQLite.
07 · code      · EL EXPERIMENTO
    Vamos a probarlo sin gastar un céntimo. El montaje es este, y quiero que lo veas antes de que se ejecute nada. A la izquierda, un cliente de Python con el SDK de OpenAI, el de verdad. En medio, el gateway. Y a la derecha, un servidor que he escrito yo, que finge ser el proveedor y apunta por pantalla todo lo que le llega. Si el gateway funciona, lo voy a ver en el servidor de la derecha.
08 · code      · EL CLIENTE
    Este es el cliente, y lo enseño antes de ejecutarlo. Son nueve líneas. Creo un cliente de OpenAI, pero en lugar de apuntar a OpenAI, apunto a mi máquina, al puerto del gateway. La clave es la del gateway, no la del proveedor. Y pido el modelo gpt-4, un nombre que quiero que alguien reescriba por mí.
09 · terminal  · LA EJECUCIÓN
    Lo ejecuto, y contesta: la factura suma mil doscientos cuarenta euros y vence el día quince. Y tres líneas que importan más que la respuesta: el modelo que el gateway me devuelve, que ya no es el que pedí, y los tokens. Todo esto ha pasado por el gateway, no ha ido directo al proveedor.
10 · code      · EL OTRO LADO
    Ahora el otro lado, el servidor que hace de proveedor. Tiene una sola línea que importa: lee el cuerpo, saca el modelo, saca la cabecera X-Team y los imprime. Nada más. Con eso ya puedo ver qué me está llegando de verdad, sin creerme la documentación de nadie.
11 · terminal  · PRIMERA PRUEBA
    Primera prueba: la puerta. Sin clave, el gateway corta en seco, cuatrocientos uno, y la petición ni sale de casa. Con la clave del gateway, doscientos. Y aquí está el detalle que me hizo confiar en esto: en el proveedor, la cabecera de autorización llega vacía. Mi clave se queda en el gateway.
12 · code      · EL ARRANQUE
    Así se arranca. Cuatro banderas y ninguna sobra. La dirección donde escucha y a quién reenvía. La clave que va a exigir a los clientes. El mapa de modelos, que dice que gpt-4 se convierta en gpt-4o-mini. Y una cabecera que añade a todo lo que salga. Al final, el fichero donde guarda la base de datos.
13 · terminal  · EL MAPA
    Pruebo el mapa con dos peticiones: una pidiendo gpt-4, otra pidiendo gpt-4o. En el proveedor aparecen dos líneas. La primera dice gpt-4o-mini: se ha reescrito. La segunda dice gpt-4o: ha pasado tal cual. El mapa solo toca lo que tú le dices que toque, y eso es exactamente lo que quieres de una pieza en medio.
14 · concept   · POR QUÉ IMPORTA
    Y esto no es un truco de fontanería. Significa que el proveedor ve lo que tú decides, y no lo que la librería de turno ha decidido por ti. Cuando algo se rompe a las tres de la mañana, la pregunta deja de ser qué creo que envié. Es qué envié, y lo tengo guardado.
15 · terminal  · STREAMING
    Segunda prueba: el streaming. Esto es lo que usa cualquier chat que escribe letra a letra. Le pido que me lo mande por trozos, y llegan los trozos: tres deltas y la marca de fin. El gateway no rompe el streaming, que es justo donde se caen casi todas las herramientas de este tipo.
16 · terminal  · OTRO DIALECTO
    Y aquí lo que de verdad me sorprendió. Le hablo en el dialecto de Ollama, con la ruta api barra chat. Y fíjate en lo que contesta: líneas con done, true, que es formato Ollama. Pero en el proveedor ha entrado una petición a v1 barra chat barra completions, que es formato OpenAI. Ha traducido el dialecto por el camino, y las dos partes creen que hablan su idioma.
17 · code      · LA MEMORIA
    Y todo esto queda en una base de datos. El esquema es una tabla sola, con una idea muy buena: guarda la petición que entró y la petición que salió, por separado. Con eso puedes poner las dos al lado y ver la diferencia exacta. Estas son las columnas que importan.
18 · terminal  · LA CONSULTA
    Consulta directa a la base, sin interfaz de por medio. Primero el estado y el modelo: doscientos, y gpt-4, el que pedí yo. Y ahora la prueba que buscaba, en forma de dos preguntas a la tabla. ¿Mi petición contiene gpt-4o-mini? Cero. ¿La petición que salió hacia el proveedor lo contiene? Uno. El cambio no lo cuento yo: lo cuenta la base de datos. Y esto es lo que me faltaba de verdad, una forma de discutir con datos en la mano, sin abrir el editor ni reiniciar el agente para volver a mirar. Cada fila es una conversación que ya ocurrió, y se queda ahí para cuando la necesites.
19 · terminal  · LO QUE NO SALE
    Y la prueba que más me importa, la de la clave. Pregunto a la base por las cabeceras: si mi autorización está en lo que entró y si está en lo que salió hacia el proveedor. Uno y cero. Está en la entrada, no está en la salida: el gateway la ha quitado por el camino. Esto no es una promesa del README, es una consulta que puedes repetir tú en tu propia base de datos. Y si algún día tienes que demostrar que tu clave no viaja, ya sabes qué preguntar.
20 · bullets   · TRES USOS
    Tres usos concretos. Depurar un agente que contesta mal y ver el mensaje de sistema que añadió la librería, ese que tú no escribiste. Comparar dos modelos con la misma petición exacta, para saber si el barato cambia la respuesta. Y auditar qué datos de un cliente salen de casa, el día que alguien te lo pregunta.
21 · terminal  · LA SUPERFICIE
    Y las banderas que no he usado también dicen mucho de la herramienta. Miro la ayuda: hay configuración por fichero, hay varios hosts, hay límites de tamaño de cuerpo y hay una interfaz de terminal. Una herramienta que enseña sus límites en la ayuda es una herramienta que espera que la uses en serio.
22 · bullets   · POR DENTRO
    Por dentro es una cadena corta, y conviene saber el orden porque explica todos los límites. Entra la petición y se identifica el dialecto. Se busca a qué proveedor va. Se comprueba la clave antes de nada. Se aplican tus reescrituras y tus cabeceras. Se reenvía, se guarda el intercambio y se devuelve al cliente. Ninguno de esos pasos es magia.
23 · concept   · EL COSTE
    Y esto no es gratis, aunque el binario sí lo sea. Guardar cada cuerpo cuesta disco, y en un agente que habla mucho eso crece rápido. Además hay que decidir qué guardas: si guardas todo, guardas también los datos de tus clientes. Esa decisión es tuya, y la herramienta no la toma por ti.
24 · bullets   · TRIAJE
    Y cuando algo falla, este es el orden que sigo, porque ahorra tiempo. Primero miro el estado: si no es doscientos, el problema es de puerta y no del modelo. Después el cuerpo que salió, para comprobar que el modelo era el que yo creía. Y solo entonces la respuesta del proveedor. Con esas tres columnas se resuelven casi todos los sustos.
25 · bullets   · LÍMITES
    Ahora los límites, que también son parte de la honestidad de este vídeo. Uno: no hay binario publicado, hay que compilarlo tú. Dos: guarda los cuerpos enteros, así que esa base de datos tiene datos sensibles y crece. Tres: solo ve lo que pasa por él. Y cuatro: el function calling no lo he probado aquí, y no voy a decirte que funciona.
26 · bullets   · CUÁNDO SÍ Y CUÁNDO NO
    Cuándo te sirve: si tienes un agente y quieres ver el tráfico exacto sin tocar tu código. Cuándo no: si lo que buscas es enrutar entre diez proveedores con reintentos y presupuestos, para eso hay piezas mucho más maduras. Y si no puedes cambiar la dirección de tu aplicación, esto no te vale: necesitas un proxy de red.
27 · concept   · EN TU CÓDIGO
    Engancharlo a tu código es una línea. Donde pones la dirección del proveedor, pones la del gateway. No hay que importar nada y no hay que cambiar de SDK. Eso es lo que me convenció: la integración más pequeña que he visto para algo que necesito siempre.
28 · code      · INSTALACIÓN
    La instalación, y la dejo para el final porque hasta ahora no la necesitabas. No hay paquete ni binario publicado: clonas el repositorio y compilas. Un comando, con el compilador de Go. Tarda unos segundos y deja un ejecutable de un solo fichero, sin dependencias. Ese fichero te lo puedes llevar a cualquier servidor.
29 · concept   · HONESTIDAD
    Y para que no te lleves una idea falsa, esto es lo que el vídeo no demuestra. El proveedor de la derecha lo he escrito yo: lo que has visto es qué bytes viajan, no la calidad de un modelo. Y la interfaz de terminal que trae el proyecto no la he grabado, porque necesita una terminal interactiva que aquí no puedo mostrar con justicia.
30 · terminal  · COMPILAR DE VERDAD
    Y la compilación, ejecutada aquí y ahora, para que no sea una línea de la documentación. Entro en el código, lanzo la compilación y espero. Sale un binario y lo listo para ver el tamaño. Ese fichero, tal cual, es el gateway: no necesita ni Python ni Node al lado, solo un sistema donde correr.
31 · outro     · CIERRE
    Eso es todo. Un binario en medio, y por primera vez sabes exactamente qué estás enviando. Si te sirve, el repositorio está en la descripción.
