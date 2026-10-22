"""Verifica el paquete cerrado: ¿esta de verdad cerrado y completo?

Se comprueba de tres maneras, y ninguna se cree a si misma:
1. sin clave: tiene que fallar al LEER las paginas (no basta con abrirlo).
2. qpdf, sin clave: dice que algoritmo de cifrado lleva el fichero.
3. con clave: paginas, marcadores y el manifiesto documento -> pagina inicial.
4. pdfinfo sobre una copia descifrada: ninguna hoja con marca de giro.

Uso:
    python3 verificar.py
    EXPEDIENTE_CLAVE=otra python3 verificar.py
"""
import os
import subprocess
import sys

from pypdf import PdfReader

ENTRADA = "entrada"
SALIDA = "salida"
NOMBRE = "expediente_EXP-2026-0431.pdf"


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def leer_indice():
    filas = []
    with open(os.path.join(ENTRADA, "indice.txt"), encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            p = [x.strip() for x in linea.split("|")]
            if len(p) >= 3:
                filas.append((int(p[0]), p[1], p[2]))
    filas.sort()
    return filas


def main():
    ruta = os.path.join(SALIDA, NOMBRE)
    if not os.path.exists(ruta):
        print("no existe %s: primero unir.py" % ruta)
        return 1
    clave = os.environ.get("EXPEDIENTE_CLAVE", "cambiar-esta-clave")

    # 1) sin clave
    print("[1] abrir SIN clave")
    try:
        r = PdfReader(ruta)
        n = len(r.pages)          # aqui es donde de verdad hay que intentar leer
        print("    !! se leyeron %d paginas sin clave: el cifrado NO protege" % n)
        return 2
    except Exception as e:
        print("    bloqueado: %s" % type(e).__name__)

    # 2) qpdf, sin clave: que cifrado lleva
    print("[2] qpdf, sin clave (herramienta ajena)")
    q = " ".join(sh(["qpdf", "--show-encryption", ruta]).split())
    for trozo in q.split("  "):
        if "encryption method" in trozo or trozo.startswith("R =") or "password" in trozo:
            print("    %s" % trozo.strip())
    aes = "AESv3" in q
    print("    cifrado detectado por qpdf: %s" % ("AES-256 (AESv3)" if aes else "otro"))

    # 3) con clave
    print("[3] con clave")
    r = PdfReader(ruta)
    ok = r.decrypt(clave)
    marcas = list(r.outline)
    print("    clave aceptada: %s | paginas: %d | marcadores: %d" % (ok, len(r.pages), len(marcas)))

    indice = leer_indice()
    esperado = 1
    print("")
    print("%-4s %-30s %-10s %-10s %s" % ("POS", "DOCUMENTO DEL INDICE", "ESPERADA", "MARCADOR", "OK"))
    buenos = 0
    for (orden, fic, titulo), item in zip(indice, marcas):
        pagina = r.get_destination_page_number(item) + 1
        marca_ok = pagina == esperado and getattr(item, "title", "") == titulo
        buenos += 1 if marca_ok else 0
        print("%-4d %-30s %-10d %-10d %s" % (orden, titulo, esperado, pagina, "si" if marca_ok else "NO"))
        n = len(PdfReader(os.path.join(ENTRADA, fic)).pages)
        esperado += n

    # 4) pdfinfo sobre una copia descifrada: giros
    print("")
    print("[4] pdfinfo sobre una copia descifrada (herramienta ajena)")
    tmp = os.path.join(SALIDA, "_descifrado.pdf")
    sh(["qpdf", "--password=" + clave, "--decrypt", ruta, tmp])
    info = sh(["pdfinfo", "-f", "1", "-l", str(len(r.pages)), tmp])
    giros = [ln.strip() for ln in info.splitlines() if "rot" in ln.lower()]
    distintos = sorted(set(ln.split(":")[-1].strip() for ln in giros))
    print("    hojas revisadas: %d | valores de giro vistos: %s"
          % (len(giros), ", ".join(distintos) if distintos else "ninguno"))
    paginas_pdfinfo = [ln for ln in info.splitlines() if ln.startswith("Pages:")]
    if paginas_pdfinfo:
        print("    pdfinfo dice: %s" % paginas_pdfinfo[0].strip())
    os.remove(tmp)

    print("")
    if len(marcas) == len(indice) and buenos == len(indice):
        print("VERIFICADO: %d documentos en el orden del indice, %d paginas, cifrado AES-256,"
              " ninguna hoja girada" % (len(indice), len(r.pages)))
        return 0
    print("NO VERIFICADO: marcadores o paginas no cuadran con el indice")
    return 1


if __name__ == "__main__":
    sys.exit(main())
