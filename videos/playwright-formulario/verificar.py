#!/usr/bin/env python3
"""Recorre el formulario como lo haría una persona y dice si sigue funcionando.

Uso:
    python verificar.py                    # comprueba el formulario bueno
    python verificar.py --pagina formulario_roto.html
"""
import argparse
import os
import sys

from playwright.sync_api import TimeoutError as PwTimeout
from playwright.sync_api import sync_playwright

import servidor

AQUI = os.path.dirname(os.path.abspath(__file__))
CAPTURAS = os.path.join(AQUI, "capturas")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pagina", default="formulario.html")
    ap.add_argument("--esperado", default="Gracias, Ana")
    a = ap.parse_args()

    os.makedirs(CAPTURAS, exist_ok=True)
    servidor.arrancar(8000)
    url = f"http://127.0.0.1:8000/{a.pagina}"
    captura = os.path.join(CAPTURAS, a.pagina.replace(".html", ".png"))

    print(f"[1/5] abro {url}", flush=True)
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        # El tope va en el CONTEXTO, no en la página: fill() y click() heredan
        # el timeout del contexto (30 s por defecto), no el de page.
        contexto = navegador.new_context()
        contexto.set_default_timeout(5000)
        pagina = contexto.new_page()
        try:
            pagina.goto(url, wait_until="load")
            print("[2/5] relleno nombre, correo y mensaje", flush=True)
            pagina.fill("#nombre", "Ana")
            pagina.fill("#email", "ana@example.com")
            pagina.fill("#mensaje", "Necesito una factura del pedido 41")
            print('[3/5] pulso "Enviar mensaje"', flush=True)
            pagina.click("#enviar")
            print("[4/5] espero la respuesta del formulario", flush=True)
            pagina.wait_for_selector("#resultado", state="visible", timeout=5000)
            texto = pagina.inner_text("#resultado").strip()
            print(f'[5/5] leo el resultado: "{texto}"', flush=True)
            if a.esperado not in texto:
                print(f"FALLO: esperaba encontrar «{a.esperado}» y no está", flush=True)
                codigo = 1
            else:
                codigo = 0
        except PwTimeout as e:
            print("FALLO: la página no llegó al estado esperado", flush=True)
            print(f"  {type(e).__name__}: {str(e).splitlines()[0]}", flush=True)
            codigo = 1
        pagina.screenshot(path=captura, full_page=True)
        navegador.close()

    tam = os.path.getsize(captura) // 1024 if os.path.exists(captura) else 0
    print(f"  captura guardada: capturas/{os.path.basename(captura)} ({tam} KB)", flush=True)
    print(f"RESULTADO: {'OK' if codigo == 0 else 'FALLO'}  -> código de salida {codigo}", flush=True)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
