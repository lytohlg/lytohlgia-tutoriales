# Windows — cómo se ejecuta esto (NO verificado en Windows)

**Estado honesto:** el paquete se ha reproducido y revisado en **Linux/Docker**, no en Windows.
Los comandos de abajo son la traducción directa de los que sí se han ejecutado, pero **no los he
probado en una máquina Windows**: están aquí para que el camino sea reproducible, no como promesa.

Lo que **sí** es seguro: `python-docx` genera archivos `.docx` **sin necesidad de tener Microsoft
Word instalado**. Word solo hace falta para abrir y revisar los contratos.

## Requisitos

- Windows 10 u 11.
- Python 3.10 o superior (`py --version` en PowerShell).
- Word (o LibreOffice) para abrir los resultados.
- Nada de claves ni cuentas: el material no usa credenciales.

## Instalación

```powershell
py -m pip install "python-docx==1.2.0"
```

La versión está fijada a propósito: fijarla evita que una actualización cambie el comportamiento a
mitad de un trabajo.

## Ejecución equivalente a `demo.sh`

`demo.sh` es un script **bash**. En Windows tienes dos caminos:

1. **WSL o Git Bash** (lo más parecido a lo que se ve en el vídeo): abre una terminal en la carpeta
   `scripts` y ejecuta `bash demo.sh`.
2. **PowerShell, comando a comando** (lo que hace `demo.sh`, en el mismo orden):

```powershell
cd scripts
py crear_plantilla.py
py marcadores.py
py sustituir_xml.py --csv clientes.csv      # el atajo: escribe 12 y deja marcadores dentro
py rellenar.py --csv clientes.csv           # el camino bueno: 12 documentos, 0 detenidos
py verificar.py --csv clientes.csv          # relectura + comprobación de formato
py limites.py                               # los límites medidos
```

Los documentos se escriben en `scripts\salida\` (y `scripts\salida_xml\` para el atajo).

## El CSV, que es donde más gente tropieza

- Debe llevar **coma** como separador y **UTF-8**. Excel en español guarda por defecto con punto y
  coma y, a veces, con BOM: si editas `clientes.csv` con Excel, guárdalo como
  *CSV UTF-8 (delimitado por comas)* y comprueba la primera línea.
- Excel convierte solos los códigos con ceros a la izquierda (un CIF no debe llevar ceros delante),
  y cambia el formato de las fechas según la configuración regional. Revisa el archivo después de
  guardarlo.
- No cambies los nombres de las columnas: el programa los busca literalmente
  (`cliente,cif,importe,concepto,fecha`).

## Antes de volver a ejecutar

- **Cierra los .docx en Word** si los vas a regenerar: Word bloquea el archivo y el programa no
  podrá sobrescribirlo.
- Vacía `salida\` si no quieres mezclar documentos de ejecuciones distintas. El script no borra nada
  por su cuenta.

## Qué esperar

- 12 documentos, 0 detenidos, y una línea por cliente con su importe y su nombre de fichero.
- Si añades un cliente sin CIF, el programa **se detiene antes de escribir su documento**, avisa con
  `DETENIDO: falta cif` y termina con código de salida 2. De ese cliente no queda ningún fichero.
