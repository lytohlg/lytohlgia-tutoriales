#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba, campo a campo, lo que ha leido el OCR contra la verdad exacta del corpus.

Esto es lo que separa "mira que bonito" de una prueba: sabemos que numero de factura, que CIF,
que fecha y que total tiene cada documento porque los hemos fabricado nosotros, asi que podemos
contar cuantos campos ha leido bien y cuantos no.

Uso: python3 scripts/comprobar.py
"""
import json
import os
import re
import sqlite3
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DB = os.path.join(RAIZ, 'documentos.db')
VERDAD = os.path.join(RAIZ, 'ground_truth.json')


def sin_tildes(t):
    t = unicodedata.normalize('NFKD', t)
    return ''.join(c for c in t if not unicodedata.combining(c))


def numeros(t):
    """Comillas y espacios que el OCR mete donde no toca: se ignoran al comparar."""
    return re.sub(r'[\s\u00a0]', '', t)


def main():
    if not os.path.exists(DB):
        print(f'No hay indice ({DB}). Ejecuta antes: python3 scripts/indexar.py')
        return 1
    verdad = json.load(open(VERDAD, encoding='utf-8'))
    con = sqlite3.connect(DB)
    filas = con.execute('SELECT archivo, pagina, texto FROM paginas').fetchall()
    con.close()
    texto_por_archivo = {}
    for archivo, _pagina, texto in filas:
        texto_por_archivo.setdefault(archivo, []).append(texto)
    plano = {a: sin_tildes('\n'.join(ts)) for a, ts in texto_por_archivo.items()}
    plano_num = {a: numeros(sin_tildes('\n'.join(ts))) for a, ts in texto_por_archivo.items()}

    total = ok = 0
    detalle = []
    for doc in verdad:
        archivo = doc['archivo']
        if archivo not in plano:
            detalle.append((archivo, 'ARCHIVO', 'no aparece en el indice', ''))
            total += 1
            continue
        campos = []
        if 'numero_factura' in doc:
            campos.append(('numero', doc['numero_factura']))
            campos.append(('cif', doc['cif']))
            campos.append(('fecha', doc['fecha']))
            campos.append(('total', f'{doc["total"]:.2f}'))
        else:
            campos.append(('referencia', doc['referencia']))
            campos.append(('importe', doc['importe_anual']))
        for nombre, valor in campos:
            total += 1
            esperado = numeros(sin_tildes(valor))
            if esperado in plano_num[archivo]:
                ok += 1
            else:
                detalle.append((archivo, nombre, valor, 'no encontrado'))

    print(f'Documentos comprobados: {len(verdad)}')
    print(f'Paginas indexadas:      {len(filas)}')
    print(f'Campos comprobados:     {total}')
    print(f'Campos correctos:       {ok}')
    print(f'Tasa de acierto:        {100.0 * ok / total:.1f} %')
    if detalle:
        print('')
        print('Campos que NO se han encontrado en el texto del OCR:')
        for archivo, nombre, valor, nota in detalle:
            print(f'   - {archivo}  {nombre}={valor}  ({nota})')
    else:
        print('')
        print('Todos los campos comprobados aparecen en el texto extraido.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
