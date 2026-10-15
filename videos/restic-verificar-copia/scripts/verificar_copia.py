#!/usr/bin/env python3
"""Comprueba que la copia de seguridad SIRVE.

Que hace, en este orden:
  1. pregunta a restic cual es el ultimo snapshot del repositorio;
  2. lo restaura ENTERO en un directorio de trabajo;
  3. compara la copia restaurada con los datos actuales, fichero a fichero
     (tamano + sha256), y tambien al contrario: que hay en la copia que hoy ya no
     esta;
  4. escribe un informe en JSON y termina con 0 (OK) o 1 (FALLO).
     El codigo de salida es lo que mira el cron: si un dia hay que restaurar de
     verdad, ya lo sabes antes.

Uso:
  python3 verificar_copia.py [--repo RUTA_DEL_REPO] [--datos RUTA_DE_LOS_DATOS]
                             [--destino RUTA_DE_LA_RESTAURACION] [--informe RUTA_DEL_INFORME]

Sin argumentos se usan las carpetas por defecto: TRABAJO (variable de entorno, o ./ si no
esta definida) mas copias/repo, datos, verificacion e informe_verificacion.json.

La contrasena del repositorio se lee de RESTIC_PASSWORD_FILE (o RESTIC_PASSWORD).
No se pasa por la linea de comandos: ahi quedaria escrita en el historial del shell
y en la lista de procesos.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def manifiesto(raiz: Path) -> dict:
    """{ruta relativa: (tamano, sha256)} de todos los ficheros bajo `raiz`."""
    out = {}
    for p in sorted(raiz.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(raiz))] = (p.stat().st_size, sha256(p))
    return out


def restic(repo: str, *args: str, timeout: int = 900) -> subprocess.CompletedProcess:
    cmd = ["restic", "--repo", repo, *args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica que la copia se puede restaurar de verdad.")
    raiz = os.environ.get("TRABAJO", ".")
    ap.add_argument("--repo", default=os.path.join(raiz, "copias", "repo"))
    ap.add_argument("--datos", default=os.path.join(raiz, "datos"))
    ap.add_argument("--destino", default=os.path.join(raiz, "verificacion"))
    ap.add_argument("--informe", default=os.path.join(raiz, "informe_verificacion.json"))
    a = ap.parse_args()

    if not os.environ.get("RESTIC_PASSWORD_FILE") and not os.environ.get("RESTIC_PASSWORD"):
        print("ERROR: falta RESTIC_PASSWORD_FILE (o RESTIC_PASSWORD).", file=sys.stderr)
        return 2

    t0 = time.time()
    datos = Path(a.datos).resolve()
    destino = Path(a.destino).resolve()
    informe = {"fecha": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "repositorio": a.repo, "datos": str(datos)}

    # 1. ultimo snapshot
    p = restic(a.repo, "snapshots", "--latest", "1", "--json")
    if p.returncode != 0:
        print("ERROR: no puedo listar los snapshots:\n" + (p.stderr or p.stdout), file=sys.stderr)
        return 2
    snaps = json.loads(p.stdout or "[]")
    if not snaps:
        informe["resultado"] = "FALLO"
        informe["motivo"] = "el repositorio no tiene ningun snapshot"
        Path(a.informe).write_text(json.dumps(informe, indent=1, ensure_ascii=False))
        print("FALLO: el repositorio no tiene ningun snapshot")
        return 1
    snap = snaps[0]
    informe["snapshot"] = {"id": snap["short_id"], "hora": snap["time"],
                           "rutas": snap.get("paths", []), "etiquetas": snap.get("tags", [])}
    print(f"ultimo snapshot : {snap['short_id']}  ({snap['time']})")

    # 2. restauracion real (completa, en un directorio limpio)
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True, exist_ok=True)
    p = restic(a.repo, "restore", snap["id"], "--target", str(destino))
    if p.returncode != 0:
        informe["resultado"] = "FALLO"
        informe["motivo"] = "la restauracion ha fallado"
        Path(a.informe).write_text(json.dumps(informe, indent=1, ensure_ascii=False))
        print("FALLO: la restauracion ha fallado:\n" + (p.stderr or p.stdout))
        return 1
    print(f"restaurado en   : {destino}")

    # 3. comparacion fichero a fichero
    cand = [d for d in destino.rglob(datos.name) if d.is_dir()]
    if not cand:
        informe["resultado"] = "FALLO"
        informe["motivo"] = f"la copia restaurada no contiene la carpeta {datos.name}"
        Path(a.informe).write_text(json.dumps(informe, indent=1, ensure_ascii=False))
        print("FALLO: la copia restaurada no contiene " + datos.name)
        return 1
    raiz_copia = max(cand, key=lambda d: sum(1 for _ in d.rglob("*")))

    orig = manifiesto(datos)
    copia = manifiesto(raiz_copia)
    identicos = [k for k in orig if k in copia and copia[k] == orig[k]]
    distintos = [k for k in orig if k in copia and copia[k] != orig[k]]
    faltan = [k for k in orig if k not in copia]          # en los datos, no en la copia
    sobran = [k for k in copia if k not in orig]          # en la copia, ya no en los datos

    informe.update({
        "raiz_restaurada": str(raiz_copia),
        "ficheros_original": len(orig),
        "ficheros_en_copia": len(copia),
        "identicos": len(identicos),
        "distintos": distintos[:20],
        "faltan_en_copia": faltan[:20],
        "sobran_en_copia": sobran[:20],
        "segundos": round(time.time() - t0, 1),
    })
    ok = not distintos and not faltan
    informe["resultado"] = "OK" if ok else "FALLO"

    print(f"ficheros        : {len(orig)} en los datos, {len(copia)} en la copia")
    print(f"identicos       : {len(identicos)}")
    print(f"distintos       : {len(distintos)}")
    print(f"faltan en copia : {len(faltan)}")
    print(f"sobran en copia : {len(sobran)}")
    print(f"resultado       : {informe['resultado']}  ({informe['segundos']} s)")

    Path(a.informe).write_text(json.dumps(informe, indent=1, ensure_ascii=False))
    print(f"informe         : {a.informe}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
