#!/bin/bash
# Lupa del log: deja solo las lineas utiles y quita el sello de tiempo.
airflow dags test "$@" 2>&1 |
  sed -E 's/^\[[^]]*\] \{[a-z_.]+:[0-9]+\} [A-Z_]+ - //; s/ map_index=-1//' |
  grep -E "^\[DAG TEST\] starting|^Marking task|^ValueError|^leidas|^limpias|^clientes con ventas|^informe escrito" |
  uniq
