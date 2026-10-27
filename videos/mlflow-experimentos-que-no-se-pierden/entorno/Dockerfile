FROM python:3.13-slim

# Entorno mínimo del material: Python 3.13 + MLflow 3 + scikit-learn.
# Sin GPU, sin servicios externos y sin claves: todo ocurre en una carpeta local.
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GIT_PYTHON_REFRESH=quiet

RUN pip install --no-cache-dir -q "mlflow>=3,<4" scikit-learn

WORKDIR /trabajo
