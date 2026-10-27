"""comparar.py — lee las ejecuciones guardadas y ordena por error de validación.

Qué entra: la base que dejó entrenar.py (sin volver a entrenar nada).
Qué sale: tabla con las tres ejecuciones ordenadas por rmse y el id de la ganadora.
"""
import os
import mlflow

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))

runs = mlflow.search_runs(
    experiment_names=["pruebas-modelo"],
    order_by=["metrics.rmse ASC"],
)
cols = ["tags.mlflow.runName", "params.alpha", "metrics.rmse", "run_id"]
tabla = runs[cols].copy()
tabla["run_id"] = tabla["run_id"].str[:8]
tabla.columns = ["run", "alpha", "rmse", "id"]
print(tabla.to_string(index=False))
print()
print("GANADORA:", tabla.iloc[0]["run"], "· rmse", round(float(tabla.iloc[0]["rmse"]), 3),
      "· id", tabla.iloc[0]["id"])
