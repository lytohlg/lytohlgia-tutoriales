"""Informe diario de ventas por cliente, en cuatro pasos encadenados."""
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow.decorators import dag, task

# Las rutas se pueden cambiar por entorno para poder reproducir la demo fuera del contenedor:
ENTRADA = Path(os.environ.get("INFORME_ENTRADA", "/work/entrada/ventas.csv"))
SALIDA = Path(os.environ.get("INFORME_SALIDA", "/work/salida/informe.csv"))


@dag(
    dag_id="informe_clientes",
    start_date=datetime(2025, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(seconds=2)},
)
def informe_clientes():

    @task
    def extraer():
        filas = list(csv.DictReader(ENTRADA.open()))
        print(f"leidas {len(filas)} filas de {ENTRADA.name}")
        return filas

    @task
    def limpiar(filas):
        buenas = []
        for f in filas:
            importe = float(f["importe"])
            if importe <= 0:
                raise ValueError(f"importe no valido en {f['cliente']}: {importe}")
            buenas.append({**f, "importe": importe})
        print(f"limpias {len(buenas)} de {len(filas)} filas")
        return buenas

    @task
    def totales(filas):
        por_cliente = {}
        for f in filas:
            por_cliente[f["cliente"]] = por_cliente.get(f["cliente"], 0) + f["importe"]
        print(f"clientes con ventas: {len(por_cliente)}")
        return por_cliente

    @task
    def guardar(por_cliente):
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        with SALIDA.open("w") as fh:
            fh.write("cliente,total\n")
            for cliente, total in sorted(por_cliente.items()):
                fh.write(f"{cliente},{total:.2f}\n")
        print(f"informe escrito: {SALIDA}")

    guardar(totales(limpiar(extraer())))


informe_clientes()
