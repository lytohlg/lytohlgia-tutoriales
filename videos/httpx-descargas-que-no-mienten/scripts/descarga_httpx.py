"""Version que SI comprueba: httpx + timeout + reintentos + validacion.

Un informe solo se da por bueno si:
  - la respuesta es 200 (reintentando los fallos transitorios)
  - llegan tantos bytes como declara Content-Length
  - el CSV trae la cabecera esperada y al menos una fila
Si algo falla, no se archiva nada: el .part se borra y queda anotado en el informe.
"""
import json
import os
import sys
import time

import httpx

if "--servidor-local" in sys.argv:          # demo autocontenida: servidor en hilo
    import servidor
    sys.argv = [a for a in sys.argv if a != "--servidor-local"]
    servidor.arrancar(8765)

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765"
RUTAS = ["/informe", "/informe-truncado", "/informe-503", "/informe-lento"]
CABECERA = "fecha;concepto;importe"
INTENTOS = 3
DESTINO = "descargas"
os.makedirs(DESTINO, exist_ok=True)

if len(sys.argv) > 2:                        # permite probar una sola ruta
    RUTAS = [r for r in RUTAS if r == sys.argv[2]]

timeout = httpx.Timeout(connect=2.0, read=2.0, write=2.0, pool=2.0)
transporte = httpx.HTTPTransport(retries=2)      # solo conexiones, NO codigos 503
informe = []

with httpx.Client(timeout=timeout, transport=transporte, follow_redirects=True) as cliente:
    for ruta in RUTAS:
        final = os.path.join(DESTINO, ruta.strip("/") + ".csv")
        parcial = final + ".part"
        resultado = {"ruta": ruta, "estado": "fallo", "bytes": 0,
                     "esperado": 0, "intentos": 0, "motivo": ""}
        for intento in range(1, INTENTOS + 1):
            resultado["intentos"] = intento
            recibido = 0
            try:
                with cliente.stream("GET", BASE + ruta) as r:
                    resultado["esperado"] = int(r.headers.get("Content-Length", 0))
                    if r.status_code >= 500:                 # 503: transitorio -> reintentar
                        espera = float(r.headers.get("Retry-After", 1))
                        resultado["motivo"] = f"HTTP {r.status_code}"
                        if intento < INTENTOS:
                            print(f"  {ruta:18s} HTTP {r.status_code} -> reintento "
                                  f"{intento} en {espera:.0f}s")
                            time.sleep(espera)
                            continue
                        break
                    r.raise_for_status()
                    with open(parcial, "wb") as f:
                        for trozo in r.iter_bytes():
                            f.write(trozo)
                            recibido += len(trozo)
                resultado["bytes"] = recibido
                if resultado["esperado"] and recibido != resultado["esperado"]:
                    resultado["motivo"] = (f"faltan datos: {recibido} de "
                                           f"{resultado['esperado']} bytes")
                    break
                with open(parcial, "r", encoding="utf-8") as f:
                    filas = f.read().splitlines()
                if not filas or filas[0] != CABECERA or len(filas) < 2:
                    resultado["motivo"] = "el contenido no es el informe esperado"
                    break
                os.replace(parcial, final)
                resultado.update(estado="ok", motivo=f"{len(filas) - 1} filas")
                break
            except httpx.RemoteProtocolError:
                resultado["bytes"] = recibido
                resultado["motivo"] = (f"conexion cortada: {recibido} de "
                                       f"{resultado['esperado']} bytes")
                break
            except httpx.ReadTimeout:
                resultado["bytes"] = recibido
                resultado["motivo"] = "se agoto el timeout de lectura (2s sin datos)"
                break
            except httpx.HTTPStatusError as e:
                resultado["motivo"] = f"HTTP {e.response.status_code}"
                break
            except httpx.HTTPError as e:
                resultado["motivo"] = type(e).__name__
                break
        if resultado["estado"] != "ok" and os.path.exists(parcial):
            os.remove(parcial)                               # nada a medias en la carpeta
        informe.append(resultado)
        print(f"  {ruta:18s} {resultado['estado'].upper():5s} intentos={resultado['intentos']} "
              f"{resultado['bytes']:5d}/{resultado['esperado']:5d} bytes  {resultado['motivo']}")

with open("informe_descarga.json", "w", encoding="utf-8") as f:
    json.dump(informe, f, indent=2, ensure_ascii=False)
buenos = sum(1 for x in informe if x["estado"] == "ok")
print(f"\n{buenos} de {len(informe)} informes validos -> informe_descarga.json")
