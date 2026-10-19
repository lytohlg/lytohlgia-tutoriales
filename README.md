# Tutoriales de automatización con Python — @lytohlgIA

Aquí está, **por separado para cada vídeo**, exactamente el código que se ejecuta en el vídeo del
canal [@lytohlgIA](https://www.youtube.com/@lytohlgIA). El objetivo es simple: que puedas
**reproducir** lo que ves, no solo verlo.

Una carpeta = un vídeo. Dentro de cada carpeta tienes los scripts y un `README.md` con el paso a
paso, escrito para que lo siga alguien que empieza de cero.

## Índice de vídeos

<!-- INDICE:INICIO -->

| Fecha | Vídeo | Carpeta | Credenciales |
|---|---|---|---|
| 2026-10-11 | [SkillCorpus: 222 skills de agente filtradas y buscables con Python](https://www.youtube.com/watch?v=0FCGz3RKs1A) | [`videos/skillcorpus`](videos/skillcorpus) | no |
| 2026-10-13 | Avisos de stock bajo con Python: inventario real en Docker | [`videos/stock-ssm`](videos/stock-ssm) | no |
| 2026-10-14 | [invoice2data: extrae datos de facturas PDF a CSV con Python (instalado y probado)](https://www.youtube.com/watch?v=F-qetN02DJ0) | [`videos/invoice2data-facturas`](videos/invoice2data-facturas) | no |
| 2026-10-15 | restic: restaurar y comparar para saber si tu copia sirve | [`videos/restic-verificar-copia`](videos/restic-verificar-copia) | no |
| 2026-10-16 | imap_tools: convierte correos en tareas con Python | [`videos/correo-a-tareas`](videos/correo-a-tareas) | no |
| 2026-10-17 | SQL Explorer: que el informe de excepciones te llegue solo | [`videos/informes-excepciones-por-correo`](videos/informes-excepciones-por-correo) | no |
| 2026-10-18 | PaddleOCR: busca dentro de tus PDF escaneados con Python | [`videos/paddleocr-documentos-escaneados`](videos/paddleocr-documentos-escaneados) | no |
| 2026-10-19 | InvenTree: controla el stock de tus componentes con Python | [`videos/inventree-stock-minimos`](videos/inventree-stock-minimos) | no |

<!-- INDICE:FIN -->

## Cómo probamos estos materiales

Ninguna carpeta se publica sin pasar por una prueba real. El procedimiento es siempre el mismo y
está dentro de cada carpeta para que lo repitas tú:

1. **Se construye un entorno limpio** con `entorno/Dockerfile` (imagen base + dependencias con
   versiones fijadas). Nada de «en mi máquina funcionaba».
2. **Se ejecuta la demo dentro de un contenedor sin privilegios**, con la carpeta montada en
   **solo lectura** y una copia de trabajo en `/tmp`: así el script no puede tocar el original.
3. **Se comprueba el resultado**, no solo que el comando termine: si el material dice que genera
   un fichero o imprime algo concreto, eso es lo que tiene que aparecer.
4. El fichero `pruebas/pruebas.sh` de cada carpeta es exactamente esa prueba. Si a ti te funciona
   y a nosotros nos funcionaba, estamos hablando del mismo entorno.

Por eso cada `README.md` trae los requisitos de **hardware y software**, el **entorno de pruebas**
con sus comandos y la explicación de **qué hace cada fichero**. Si algo no está explicado, no se
publica: ese es el criterio de la casa.

## Cómo usar una carpeta

1. Entra en la carpeta del vídeo que quieras reproducir (columna *Carpeta* del índice).
2. Lee su `README.md` de arriba abajo: indica los requisitos, los pasos y el resultado esperado.
3. Si el material necesita claves de algún servicio, lo dice en la sección *Coste y credenciales*
   y trae un `.env.example` para que pongas las tuyas. **Nunca escribas una clave dentro de un
   script**: se lee de una variable de entorno.

## Reglas de este repositorio

- **Nada de datos personales ni credenciales.** Ni claves, ni rutas privadas, ni correos, ni nada
  que identifique a nadie. Si necesitas una clave, la pones tú en tu `.env` (que está ignorado
  por Git).
- **Código real, no decorativo.** Es el que se ejecuta en el vídeo, con rutas relativas y
  variables de entorno.
- **Un vídeo, una carpeta.** Si algo no funciona, abre una incidencia y se corrige.
- El código de terceros que se use se enlaza a su repositorio y a su licencia: no se copia aquí.

## Licencia

MIT. Puedes usar, modificar, vender y redistribuir este código como quieras. Ver
[`LICENSE`](LICENSE).

## Plantilla

Si quieres ver la estructura que sigue cada carpeta, mira [`_PLANTILLA`](_PLANTILLA): es la misma
que se usa para preparar cada vídeo antes de grabarlo.
