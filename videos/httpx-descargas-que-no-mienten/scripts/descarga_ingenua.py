"""Version INGENUA: lo que hace cualquiera la primera vez.

Descarga los cuatro informes con urllib y da por bueno cualquier fichero que aparezca.
"""
import os
import sys
import urllib.request

if "--servidor-local" in sys.argv:          # demo autocontenida: servidor en hilo
    import servidor
    sys.argv = [a for a in sys.argv if a != "--servidor-local"]
    servidor.arrancar(8765)

if "--timeout" in sys.argv:                 # limite de espera global, como haria cualquiera
    import socket
    i = sys.argv.index("--timeout")
    socket.setdefaulttimeout(float(sys.argv[i + 1]))
    del sys.argv[i:i + 2]

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765"
RUTAS = ["/informe", "/informe-truncado", "/informe-503", "/informe-lento"]
DESTINO = "descargas_viejo"
os.makedirs(DESTINO, exist_ok=True)

if len(sys.argv) > 2:                        # permite probar una sola ruta
    RUTAS = [r for r in RUTAS if r == sys.argv[2]]

for ruta in RUTAS:
    nombre = os.path.join(DESTINO, ruta.strip("/") + ".csv")
    try:
        urllib.request.urlretrieve(BASE + ruta, nombre)
        print(f"{ruta:20s} descargado -> {nombre}")
    except Exception as e:
        print(f"{ruta:20s} ERROR {type(e).__name__}: {e}")

print()
for nombre in sorted(os.listdir(DESTINO)):
    ruta = os.path.join(DESTINO, nombre)
    with open(ruta, "rb") as f:
        datos = f.read()
    lineas = datos.count(b"\n")
    print(f"{nombre:28s} {len(datos):6d} bytes  {lineas:2d} lineas  empieza: {datos[:38]!r}")
