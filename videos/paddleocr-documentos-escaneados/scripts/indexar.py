#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Índice local: pasa cada página de cada PDF por OCR y guarda el texto en SQLite.

Es incremental: si un documento ya está en el índice y NO ha cambiado de tamaño, no se vuelve a
leer. Así reindexar una carpeta grande no cuesta el trabajo de la primera vez.

Uso:
    python3 scripts/indexar.py [carpeta]        # por defecto: documentos/
    python3 scripts/indexar.py --refrescar      # ignora lo ya indexado y rehace el índice
"""
import os
import sqlite3
import sys
import time

import numpy as np
import pypdfium2 as pdfium
from paddleocr import PaddleOCR

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DB = os.path.join(RAIZ, 'documentos.db')
CARPETA = os.path.join(RAIZ, 'documentos')


def paginas_del_pdf(ruta, escala=2.0):
    """Cada página del PDF como imagen (numpy) lista para el OCR."""
    pdf = pdfium.PdfDocument(ruta)
    for i in range(len(pdf)):
        yield np.array(pdf[i].render(scale=escala).to_pil().convert('RGB'))


def ya_indexados():
    """{archivo: tamaño_en_bytes} de lo que ya está en el índice."""
    if not os.path.exists(DB):
        return {}
    try:
        con = sqlite3.connect(DB)
        filas = con.execute(
            'SELECT archivo, max(bytes) FROM paginas GROUP BY archivo').fetchall()
        con.close()
        return dict(filas)
    except sqlite3.Error:
        return {}


def main():
    argumentos = [a for a in sys.argv[1:] if a != '--refrescar']
    carpeta = argumentos[0] if argumentos else CARPETA
    refrescar = '--refrescar' in sys.argv[1:]

    if not os.path.isdir(carpeta):
        print(f'No existe la carpeta {carpeta}')
        return 1

    pdfs = sorted(f for f in os.listdir(carpeta) if f.lower().endswith('.pdf'))
    if not pdfs:
        print(f'No hay PDFs en {carpeta}')
        return 1

    if refrescar and os.path.exists(DB):
        os.remove(DB)
        print('--refrescar: se ha borrado el índice anterior')

    hechos = ya_indexados()
    pendientes = []
    for nombre in pdfs:
        ruta = os.path.join(carpeta, nombre)
        if hechos.get(nombre) == os.path.getsize(ruta):
            continue
        pendientes.append((nombre, ruta))

    total_hechos = len(hechos)
    print(f'Documentos en {os.path.basename(carpeta)}/: {len(pdfs)}')
    if total_hechos:
        print(f'Ya indexados (no se repiten): {len(pdfs) - len(pendientes)}')
    print(f'Por leer ahora: {len(pendientes)}')
    if not pendientes:
        print(f'')
        print(f'Nada nuevo que indexar: los {len(pdfs)} documentos ya estaban en el índice.')
        return 0

    t0 = time.time()
    print('')
    print('Cargando el modelo de OCR...')
    # enable_mkldnn=False: el backend oneDNN de PaddlePaddle 3.3.1 falla en esta CPU
    # (ConvertPirAttribute2RuntimeAttribute). Medido el 16-oct-2026.
    ocr = PaddleOCR(lang='es', use_doc_orientation_classify=False,
                    use_doc_unwarping=False, use_textline_orientation=False,
                    enable_mkldnn=False)
    print(f'Modelo listo en {time.time() - t0:.1f} s')

    con = sqlite3.connect(DB)
    con.execute('CREATE TABLE IF NOT EXISTS paginas ('
                'archivo TEXT, pagina INTEGER, texto TEXT, bytes INTEGER)')
    n_paginas = 0
    n_nuevos = 0
    for nombre, ruta in pendientes:
        tam = os.path.getsize(ruta)
        n_nuevos += 1
        for i, pagina in enumerate(paginas_del_pdf(ruta), start=1):
            res = list(ocr.predict(pagina))
            lineas = []
            for r in res:
                lineas.extend(r.get('rec_texts', []) or [])
            con.execute('INSERT INTO paginas VALUES (?, ?, ?, ?)',
                        (nombre, i, '\n'.join(lineas), tam))
            con.commit()
            n_paginas += 1
            print(f'   {nombre} pagina {i}: {len(lineas)} lineas')

    dentro = con.execute('SELECT count(*) FROM paginas').fetchone()[0]
    docs = con.execute('SELECT count(DISTINCT archivo) FROM paginas').fetchone()[0]
    con.close()
    seg = time.time() - t0
    print('')
    print(f'Documentos nuevos indexados: {n_nuevos}')
    print(f'Paginas leidas ahora: {n_paginas}')
    print(f'Tiempo real de OCR: {seg:.1f} s ({seg / max(n_paginas, 1):.1f} s por pagina)')
    print(f'Indice: {docs} documentos, {dentro} paginas en total')
    return 0


if __name__ == '__main__':
    sys.exit(main())
