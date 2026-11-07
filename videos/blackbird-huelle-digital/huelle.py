#!/usr/bin/env python3
"""
huelle.py — convierte la lista cruda de Blackbird en un informe verificado.

Blackbird dice "existe una cuenta con este nombre en esta web", pero eso es una
señal, no una prueba: mucha gente usa el mismo nombre de usuario y muchas webs
responden 200 con una página de "no encontrado".

Este script coge la lista y comprueba cada URL para separar tres cosas:

    probable -> la web responde 200, NO es una página de "no encontrado" y el
                nombre aparece en el <title>: la firma más fiable sin abrir el perfil
    dudoso   -> responde 200 pero el nombre solo aparece en el cuerpo: muro de
                login, plantilla genérica o simplemente otra persona
    caido    -> error HTTP, timeout o página de "no encontrado" con código 200

Uso:
    python3 huelle.py <nombre_de_usuario> [--saltar-busqueda]

Escribe results/informe_<usuario>.md y .csv y lo resume por pantalla.
"""
import argparse
import csv
import glob
import html
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
CABECERAS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
RX_TITULO = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
RX_OG = re.compile(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', re.I)
# Señales de "esta cuenta no existe" servidas con HTTP 200 (soft 404).
NO_ENCONTRADO = (
    "page not found", "user not found", "not found", "no encontrado", "no existe",
    "does not exist", "couldn't find", "could not find", "404", "no such user",
    "perfil no disponible", "cuenta no encontrada", "nothing here",
)
ORDEN = {"caido": 0, "dudoso": 1, "probable": 2}


def buscar(usuario: str) -> str:
    """Ejecuta Blackbird y devuelve la ruta del JSON más reciente."""
    cmd = [sys.executable, "blackbird.py", "-u", usuario, "--no-nsfw",
           "--json", "--timeout", "10", "--no-update"]
    print("$ " + " ".join(cmd), flush=True)
    antes = set(glob.glob(os.path.join(AQUI, "results", "*", "*.json")))
    subprocess.run(cmd, cwd=AQUI, check=True)
    nuevos = sorted(set(glob.glob(os.path.join(AQUI, "results", "*", "*.json"))) - antes,
                    key=os.path.getmtime)
    if not nuevos:
        sys.exit("no se generó ningún JSON: revisa la salida de Blackbird")
    return nuevos[-1]


def verificar(url: str, usuario: str) -> tuple:
    """Una petición por hallazgo. Devuelve (estado_http, veredicto, pista)."""
    try:
        r = requests.get(url, headers=CABECERAS, timeout=12, allow_redirects=True)
    except Exception:
        return 0, "caido", "sin respuesta"
    if r.status_code >= 400:
        return r.status_code, "caido", f"HTTP {r.status_code}"
    cuerpo = r.text
    m = RX_TITULO.search(cuerpo) or RX_OG.search(cuerpo)
    titulo = html.unescape(m.group(1)) if m else ""
    titulo = re.sub(r"\s+", " ", titulo).strip()
    bajo = cuerpo.lower()
    # Una página de "no encontrado" también devuelve 200: sin esto sale todo "probable".
    if any(s in bajo[:6000] for s in NO_ENCONTRADO) and usuario.lower() not in titulo.lower():
        return r.status_code, "caido", "página de no encontrado"
    if usuario.lower() in titulo.lower():
        return r.status_code, "probable", titulo[:60]
    return r.status_code, "dudoso", titulo[:60] or "sin título"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("usuario")
    ap.add_argument("--saltar-busqueda", action="store_true",
                    help="reutiliza el último JSON en vez de lanzar Blackbird")
    args = ap.parse_args()
    usuario = args.usuario.strip()

    if args.saltar_busqueda:
        jsons = sorted(glob.glob(os.path.join(AQUI, "results", "*", "*.json")),
                       key=os.path.getmtime)
        if not jsons:
            sys.exit("no hay resultados previos en results/")
        ruta_json = jsons[-1]
    else:
        ruta_json = buscar(usuario)

    hallazgos = json.load(open(ruta_json, encoding="utf-8"))
    print(f"pistas de Blackbird: {len(hallazgos)}  ({os.path.basename(ruta_json)})")

    # En paralelo: 96 peticiones en serie tardan minutos; así tardan segundos.
    with ThreadPoolExecutor(max_workers=8) as pool:
        resultados = list(pool.map(lambda h: verificar(h["url"], usuario), hallazgos))

    filas = []
    for h, (codigo, veredicto, pista) in zip(hallazgos, resultados):
        filas.append({"web": h["name"], "url": h["url"], "http": codigo or "-",
                      "veredicto": veredicto, "pista": pista})

    resumen = {"probable": 0, "dudoso": 0, "caido": 0}
    for f in filas:
        resumen[f["veredicto"]] += 1
    for f in sorted(filas, key=lambda x: ORDEN[x["veredicto"]]):
        print(f"  {f['veredicto']:<8} {str(f['http']):<3} {f['web']:<24} {f['pista'][:42]}")

    salida = os.path.join(AQUI, "results")
    os.makedirs(salida, exist_ok=True)
    md = os.path.join(salida, f"informe_{usuario}.md")
    with open(md, "w", encoding="utf-8") as fh:
        fh.write(f"# Huella de «{usuario}»\n\n")
        fh.write(f"Pistas de Blackbird: **{len(filas)}** · probables: **{resumen['probable']}** · "
                 f"dudosos: **{resumen['dudoso']}** · caídos: **{resumen['caido']}**\n\n")
        fh.write("| web | estado | veredicto | pista | url |\n|---|---|---|---|---|\n")
        for f in sorted(filas, key=lambda x: ORDEN[x["veredicto"]]):
            fh.write(f"| {f['web']} | {f['http']} | {f['veredicto']} | {f['pista']} | {f['url']} |\n")

    csv_path = os.path.join(salida, f"informe_{usuario}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["web", "url", "http", "veredicto", "pista"])
        w.writeheader()
        w.writerows(filas)

    print(f"\nRESUMEN {usuario}: {len(filas)} pistas -> {resumen['probable']} probables · "
          f"{resumen['dudoso']} dudosos · {resumen['caido']} caidos")
    print(f"informe: {os.path.relpath(md, AQUI)}")
    print("INFORME LISTO")


if __name__ == "__main__":
    inicio = time.time()
    main()
    print(f"tiempo total: {time.time() - inicio:.1f}s")
