"""recuperar.py — carga EXACTAMENTE el modelo de la ejecución ganadora y predice.

Qué entra: la base de MLflow (se busca la mejor ejecución por métrica, no a mano)
y cuatro casos nuevos.
Qué sale: la ruta del artefacto cargado y las cuatro predicciones.
"""
import os
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_diabetes

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))

runs = mlflow.search_runs(experiment_names=["pruebas-modelo"], order_by=["metrics.rmse ASC"])
mejor = runs.iloc[0]
run_id = mejor["run_id"]
print("ejecución elegida:", mejor["tags.mlflow.runName"], "· rmse", round(float(mejor["metrics.rmse"]), 3))

modelo = mlflow.sklearn.load_model(mejor["tags.model_uri"])
print("artefacto cargado: ", mejor["tags.model_uri"])

X, _ = load_diabetes(return_X_y=True)
for i, p in enumerate(modelo.predict(X[:4]), 1):
    print(f"caso {i}: progresión estimada {p:.1f}")
