"""filtrar.py — no quiero todas las pruebas, quiero las que cumplen algo.

Qué entra: la base con tres ejecuciones.
Qué sale: solo las que probaron una regularización distinta de 0,1, ordenadas por error.
"""
import os
import mlflow

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))

runs = mlflow.search_runs(
    experiment_names=["pruebas-modelo"],
    filter_string="params.alpha != '0.1'",
    order_by=["metrics.rmse ASC"],
)
print(runs[["tags.mlflow.runName", "params.alpha", "metrics.rmse"]].to_string(index=False))
print()
print(f"filtradas: {len(runs)} de 3 ejecuciones")
