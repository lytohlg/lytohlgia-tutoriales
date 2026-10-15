#!/usr/bin/env python3
"""Resumen legible del corpus, LEIDO de los ficheros reales (nada inventado)."""
import os
import sqlite3

LIB = os.environ.get('SKILLCORPUS_LIB', '/work/lib')
CORPUS = os.path.join(LIB, 'corpus')
pq = os.path.join(CORPUS, 'skills.parquet')

print('== /work/lib ==')
print('  ' + '  '.join(sorted(os.listdir(LIB))))

print('\n== corpus/ ==')
for f in sorted(os.listdir(CORPUS)):
    p = os.path.join(CORPUS, f)
    print(f'  {f:<22} {os.path.getsize(p)/1024/1024:6.2f} MB')

card = os.path.join(CORPUS, 'README.md')
if os.path.exists(card):
    print('\n== dataset card (README.md) ==')
    for l in [l.rstrip() for l in open(card)][:6]:
        print('  ' + l)

db = os.path.join(LIB, 'index.db')
if os.path.exists(db):
    con = sqlite3.connect(db)
    try:
        import sqlite_vec
        con.enable_load_extension(True)
        sqlite_vec.load(con)
    except Exception as e:
        print('\n(sqlite-vec no cargado: %s)' % type(e).__name__)
    cur = con.cursor()
    print('\n== index.db ==')
    # fetchall() antes de iterar: reusar el cursor dentro del bucle lo reinicia
    tablas = cur.execute("select name from sqlite_master where type='table' order by name").fetchall()
    for (t,) in tablas:
        if t.startswith('vec_skills_') and t != 'vec_skills':
            continue
        try:
            n = cur.execute('select count(*) from "%s"' % t).fetchone()[0]
            print(f'  {t:<20} {n}')
        except Exception as e:
            print(f'  {t:<20} (no legible sin la extension vec0)')

if os.path.exists(pq):
    import pyarrow.parquet as pap
    from collections import Counter
    t = pap.read_table(pq)
    print('\n== skills.parquet ==')
    print(f'  {t.num_rows} filas x {t.num_columns} columnas')
    print('  ' + ', '.join(t.column_names))
    for k, v in Counter(t.column('source').to_pylist()).most_common():
        print(f'    {k:<36} {v}')
    cats = Counter(t.column('category').to_pylist())
    print('  categorias: ' + ', '.join(f'{k}={v}' for k, v in cats.most_common()))
