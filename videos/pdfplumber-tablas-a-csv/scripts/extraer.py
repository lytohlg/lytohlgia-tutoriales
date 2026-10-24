#!/usr/bin/env python3
"""Extrae la tabla de un albaran PDF y la ensena en pantalla.

Tres formas, y la diferencia es el video:

  lines     la de por defecto. Busca LINEAS DIBUJADAS y las usa como rejilla.
            Si el PDF no trae lineas (muchos ERPs no las pintan), no ve tabla.
  text      usa las PALABRAS como rejilla y adivina donde empieza cada columna.
            Encuentra "algo", pero se traga la cabecera del documento y corta
            columnas donde no toca: peor que nada, porque parece que funciona.
  columnas  no adivina: recorta la zona de la tabla, mide los bordes de columna
            sobre la cabecera y reparte cada palabra por su posicion.
            Una fila de tabla = una linea de texto (se agrupan por altura).

Uso:
    python3 extraer.py --pdf entrada/albaran_0310.pdf
    python3 extraer.py --pdf entrada/albaran_0320.pdf --estrategia text
    python3 extraer.py --pdf entrada/albaran_0320.pdf --estrategia columnas
"""
import argparse

import pdfplumber

# Cabecera de la tabla, tal cual la imprime el proveedor.
TITULOS = ("REF", "DESCRIPCION", "CANT", "PRECIO", "IMPORTE")

# Altura (en puntos) dentro de la cual dos palabras son la misma linea.
TOLERANCIA_FILA = 3.0
# Separacion (en puntos) a partir de la cual hay un espacio real entre dos palabras.
TOLERANCIA_ESPACIO = 1.2


def ajustes(estrategia):
    if estrategia == "lines":
        return {}
    if estrategia == "text":
        return {"vertical_strategy": "text", "horizontal_strategy": "text", "text_y_tolerance": 3}
    raise ValueError(estrategia)


def zona_y_columnas(pagina):
    """Devuelve (recorte de la tabla, bordes de columna) medidos sobre la cabecera."""
    palabras = pagina.extract_words()
    titulos = {}
    for w in palabras:
        if w["text"] in TITULOS:
            titulos.setdefault(w["text"], w)
    faltan = [t for t in TITULOS if t not in titulos]
    if faltan:
        raise SystemExit("no encuentro la cabecera de la tabla: faltan %s" % ", ".join(faltan))

    limites = [
        titulos["REF"]["x0"] - 8,
        titulos["DESCRIPCION"]["x0"] - 8,
        titulos["CANT"]["x0"] - 25,
        titulos["PRECIO"]["x0"] - 15,
        titulos["IMPORTE"]["x0"] - 15,
        titulos["IMPORTE"]["x1"] + 15,
    ]
    arriba = titulos["REF"]["top"] - 6
    cortes = [w["top"] for w in palabras if w["text"].startswith(("TOTAL", "LINEAS"))]
    abajo = (min(cortes) - 4) if cortes else pagina.height
    return pagina.crop((0, arriba, pagina.width, abajo)), limites


def unir(palabras):
    """Junta las palabras de una celda: espacio solo donde de verdad lo hay."""
    texto = ""
    anterior = None
    for w in palabras:
        if anterior is not None and w["x0"] - anterior["x1"] > TOLERANCIA_ESPACIO:
            texto += " "
        texto += w["text"]
        anterior = w
    return texto.strip()


def repartir(palabras, limites):
    """Una palabra pertenece a la columna en la que cae el centro de su caja."""
    celdas = [[] for _ in range(len(limites) - 1)]
    for w in sorted(palabras, key=lambda x: x["x0"]):
        centro = (w["x0"] + w["x1"]) / 2
        for i in range(len(limites) - 1):
            if limites[i] <= centro < limites[i + 1]:
                celdas[i].append(w)
                break
    return [unir(c) for c in celdas]


def filas_por_palabras(zona, limites):
    """Agrupa por altura y reparte. Una fila de tabla = una linea de texto."""
    lineas = {}
    for w in zona.extract_words():
        clave = round(((w["top"] + w["bottom"]) / 2) / TOLERANCIA_FILA)
        lineas.setdefault(clave, []).append(w)
    filas = [repartir(lineas[k], limites) for k in sorted(lineas)]
    return [f for f in filas if any(f)]


def fusionar(tabla):
    """Une las filas que son continuacion de la descripcion anterior (sin referencia).

    Una celda que ocupa dos lineas sale como dos filas. Se ve en el original: la
    segunda fila no trae REF. Eso no es un fallo de pdfplumber, es como esta escrito
    el PDF; aqui se deshace.
    """
    filas = []
    for fila in tabla[1:]:  # la primera es la cabecera
        celdas = ["" if c is None else " ".join(str(c).split()) for c in fila]
        if not celdas[0] and filas and celdas[1]:
            filas[-1][1] = (filas[-1][1] + " " + celdas[1]).strip()
            continue
        filas.append(celdas)
    return filas


def extraer(pdf, estrategia="columnas"):
    """Devuelve (tabla, pagina, info). tabla es lista de listas o None."""
    with pdfplumber.open(pdf) as doc:
        pagina = doc.pages[0]
        if estrategia == "columnas":
            zona, limites = zona_y_columnas(pagina)
            tabla = filas_por_palabras(zona, limites)
            info = {"limites": limites, "area": "recortada a la tabla"}
        else:
            aj = ajustes(estrategia)
            tablas = pagina.extract_tables(table_settings=aj) if aj else pagina.extract_tables()
            tabla = tablas[0] if tablas else None
            info = {"ajustes": aj or "por defecto (lineas dibujadas)", "area": "pagina completa"}
        return tabla, pagina, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--estrategia", choices=["lines", "text", "columnas"], default="lines")
    a = ap.parse_args()
    tabla, pagina, info = extraer(a.pdf, a.estrategia)
    print("pdf: %s" % a.pdf)
    print("estrategia: %s | zona: %s" % (a.estrategia, info["area"]))
    if a.estrategia == "columnas":
        print("bordes de columna (x): %s" % [round(c, 1) for c in info["limites"]])
    else:
        print("ajustes: %s" % (info["ajustes"],))
    if not tabla:
        print("tablas encontradas: 0")
        print("RESULTADO: 0 tablas.")
        return
    print("tabla encontrada: %d filas x %d columnas" % (len(tabla), len(tabla[0])))
    for fila in tabla[:4]:
        print("   " + " | ".join("" if c is None else c.replace("\n", " ") for c in fila))
    if len(tabla) > 4:
        print("   ... (%d filas mas)" % (len(tabla) - 4))


if __name__ == "__main__":
    main()
