#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Busca un texto dentro de los documentos ya indexados y dice en que fichero y pagina esta.

Uso:  python3 scripts/buscar.py "F-2026-0443"
      python3 scripts/buscar.py --db documentos.db "TOTAL A PAGAR"
"""
import os
import sqlite3
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def normalizar(t):
    t = unicodedata.normalize('NFKD', t.lower())
    return ''.join(c for c in t if not unicodedata.combining(c))


def main():
    args = sys.argv[1:]
    db = os.path.join(RAIZ, 'documentos.db')
    if args and args[0] == '--db':
        db, args = args[1], args[2:]
    if not args:
        print('Uso: python3 scripts/buscar.py "<texto a buscar>"')
        return 1
    consulta = args[0]

    if not os.path.exists(db):
        print(f'No hay indice todavia ({db}). Ejecuta antes: python3 scripts/indexar.py')
        return 1

    con = sqlite3.connect(db)
    filas = con.execute('SELECT archivo, pagina, texto FROM paginas').fetchall()
    con.close()

    objetivo = normalizar(consulta)
    encontrados = []
    for archivo, pagina, texto in filas:
        for linea in texto.splitlines():
            if objetivo in normalizar(linea):
                encontrados.append((archivo, pagina, linea.strip()))

    print(f'Busqueda: "{consulta}"   (paginas indexadas: {len(filas)})')
    if not encontrados:
        print('   0 coincidencias.')
        return 0
    print(f'   {len(encontrados)} coincidencia(s):')
    for archivo, pagina, linea in encontrados:
        print(f'   - {archivo}  pagina {pagina}')
        print(f'     {linea}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
