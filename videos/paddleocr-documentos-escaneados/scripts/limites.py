#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ensenna los limites con un documento mal escaneado (baja resolucion y borroso).

No hay trampa: se pasa el mismo OCR con la misma configuracion y se compara con la verdad.
Uso: python3 scripts/limites.py
"""
import io
import os
import re
import sys

import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MALO = os.path.join(RAIZ, 'documentos', 'factura_mal_escaneada.jpg')

VERDAD = {
    'numero': 'F-2026-0999',
    'cif': 'B00000000',
    'fecha': '30/09/2026',
    'total': '323,88',
}


def main():
    if not os.path.exists(MALO):
        print(f'Falta {MALO}. Ejecuta antes: python3 scripts/generar_corpus.py')
        return 1
    imagen = np.array(Image.open(MALO).convert('RGB'))
    alto, ancho = imagen.shape[:2]
    print(f'Documento: {os.path.basename(MALO)}  ({ancho}x{alto} px, '
          f'{os.path.getsize(MALO)} bytes)')
    # enable_mkldnn=False: mismo motivo que en indexar.py (backend oneDNN de PaddlePaddle 3.3.1).
    ocr = PaddleOCR(lang='es', use_doc_orientation_classify=False,
                    use_doc_unwarping=False, use_textline_orientation=False,
                    enable_mkldnn=False)
    lineas = []
    for r in ocr.predict(imagen):
        lineas.extend(r['rec_texts'])
    print(f'Lineas detectadas: {len(lineas)}')
    for l in lineas:
        print(f'   {l}')
    plano = re.sub(r'\s', '', ''.join(lineas))
    print('')
    print('Contra la verdad exacta del documento:')
    aciertos = 0
    for nombre, valor in VERDAD.items():
        bien = re.sub(r'\s', '', valor) in plano
        aciertos += int(bien)
        print(f'   {nombre:>8}: {valor:<14} {"leido" if bien else "NO leido"}')
    print(f'   campos leidos: {aciertos}/{len(VERDAD)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
