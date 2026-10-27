"""entrenar.py — tres configuraciones del mismo modelo, cada una registrada en MLflow.

Qué entra: un dataset pequeño que viene con scikit-learn (diabetes) y tres
valores del mismo hiperparámetro (la regularización).
Qué sale: tres "runs" en la base de MLflow (parámetros, métrica rmse, modelo
guardado en disco), más por pantalla la línea de cada run con su id y su error.
"""
import os
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

RAIZ = os.environ.get("MLFLOW_ARTIFACT_ROOT", "file://" + os.path.abspath("mlartifacts"))
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))

try:
    mlflow.create_experiment("pruebas-modelo", artifact_location=RAIZ)
    print(f"experimento creado · artefactos en {RAIZ}")
except Exception:
    pass
mlflow.set_experiment("pruebas-modelo")

X, y = load_diabetes(return_X_y=True)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=42)

CONFIGS = [{"alpha": 0.1}, {"alpha": 1.0}, {"alpha": 10.0}]

for cfg in CONFIGS:
    with mlflow.start_run(run_name=f"ridge-alpha-{cfg['alpha']}"):
        model = Ridge(**cfg)
        model.fit(X_train, y_train)
        pred = model.predict(X_val)
        rmse = float(np.sqrt(mean_squared_error(y_val, pred)))
        mlflow.log_params(cfg)
        mlflow.log_metric("rmse", rmse)
        info = mlflow.sklearn.log_model(model, name="modelo")
        # la ruta del modelo se guarda como etiqueta: así el guion puede mostrarla
        mlflow.set_tag("model_uri", info.model_uri)
        run_id = mlflow.active_run().info.run_id
        print(f"run {run_id[:8]}  alpha={cfg['alpha']:<5}  rmse={rmse:.3f}  {info.model_uri}")
