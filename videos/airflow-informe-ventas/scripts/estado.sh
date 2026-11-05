#!/bin/bash
# Tabla corta: la tarea y su estado, sin columnas de fechas.
airflow tasks states-for-dag-run informe_clientes "$1" |
  awk -F' *\\| *' 'NR>2 && NF>3 {printf "%-9s %s\n", $3, $4}'
