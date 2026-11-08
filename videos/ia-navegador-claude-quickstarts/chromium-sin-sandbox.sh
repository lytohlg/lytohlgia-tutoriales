#!/bin/sh
# Lanzador de Chromium para ejecutar la demo SIN ser root dentro de un contenedor.
#
# Por qué existe: Chromium necesita un sandbox, y dentro de un contenedor con
# namespaces de usuario desactivados no puede montarlo. El driver del repositorio
# añade --no-sandbox por su cuenta cuando detecta que corre como root, pero si lo
# ejecutas con tu usuario normal (uid 1000, como en un contenedor de pruebas) nadie
# lo añade y Chromium se niega a arrancar con «No usable sandbox».
#
# El driver acepta una ruta de binario en la variable CHROME_PATH; esto es ese
# binario. Si ejecutas en tu máquina con tu usuario, NO uses este lanzador: el
# sandbox de Chromium funcionará y es más seguro dejarlo activado.
exec /usr/bin/chromium --no-sandbox --disable-dev-shm-usage "$@"
