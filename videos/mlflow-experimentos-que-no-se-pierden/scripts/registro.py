"""registro.py — pone nombre a la mejor ejecución y devuelve una versión numerada.

Qué entra: la mejor ejecución por error, ya guardada.
Qué sale: el modelo registrado con su versión, atado al identificador de esa ejecución.
"""
import os
import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))

runs = mlflow.search_runs(experiment_names=["pruebas-modelo"], order_by=["metrics.rmse ASC"])
mejor = runs.iloc[0]
print("mejor ejecución:", mejor["tags.mlflow.runName"], "· rmse", round(float(mejor["metrics.rmse"]), 3))

modelo = mlflow.register_model(runs.iloc[0]["tags.model_uri"], "progresion-diabetes")
print(f"modelo registrado: {modelo.name} · versión {modelo.version}")

cliente = MlflowClient()
for v in cliente.search_model_versions("name='progresion-diabetes'"):
    print(f"  versión {v.version} · run {v.run_id[:8]} · estado {v.status}")
