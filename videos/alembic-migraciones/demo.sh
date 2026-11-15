#!/usr/bin/env bash
# Demo del vídeo «Alembic: cambia tu base de datos sin perder datos (tutorial Python)» — @lytohlgIA
# Reproduce, en el mismo orden que el vídeo, el cambio de estructura de una
# base de datos SQLite sin perder las filas que ya había dentro.
# Rutas relativas y sin datos personales: se puede ejecutar en un contenedor limpio.
set -euo pipefail

echo "== 1. PARTIMOS DE CERO: no hay base de datos ni migraciones =="
rm -rf migrations alembic.ini tienda.db
python3 estado.py || true
echo

echo "== 2. ALEMBIC PREPARA EL PROYECTO DE MIGRACIONES =="
alembic init migrations
echo

echo "== 3. LE DECIMOS DÓNDE ESTÁ LA BASE Y DÓNDE ESTÁ EL MODELO =="
sed -i 's|^sqlalchemy.url = .*|sqlalchemy.url = sqlite:///tienda.db|' alembic.ini
sed -i 's|^target_metadata = None|import models\ntarget_metadata = models.Base.metadata|' migrations/env.py
grep -n '^sqlalchemy.url' alembic.ini
grep -n 'target_metadata = ' migrations/env.py
echo

echo "== 4. LA PRIMERA MIGRACIÓN: CREAR LA TABLA (LA ESCRIBE ALEMBIC) =="
alembic revision --autogenerate -m "crear tabla clientes"
head -40 migrations/versions/*crear_tabla_clientes.py
echo

echo "== 5. APLICAR: LA BASE YA TIENE LA TABLA =="
alembic upgrade head
python3 seed.py
python3 estado.py
echo

echo "== 6. CAMBIA EL MODELO: QUEREMOS GUARDAR EL CORREO =="
sed -i 's|^    ciudad = Column(String)|    ciudad = Column(String)\n    email = Column(String, nullable=True)|' models.py
grep -n 'email' models.py
echo

echo "== 7. SEGUNDA MIGRACIÓN: SOLO LA DIFERENCIA, NO LA TABLA ENTERA =="
alembic revision --autogenerate -m "anadir columna email"
cat migrations/versions/*anadir_columna_email.py
echo

echo "== 8. APLICAR SOBRE UNA BASE QUE YA TIENE DATOS =="
alembic upgrade head
python3 estado.py
echo

echo "== 9. HISTORIAL Y VERSIÓN ACTUAL =="
alembic history
alembic current
echo

echo "== 10. VOLVER ATRÁS Y ADELANTE (LA MIGRACIÓN ES REVERSIBLE) =="
alembic downgrade -1
python3 estado.py
alembic upgrade head
python3 estado.py
