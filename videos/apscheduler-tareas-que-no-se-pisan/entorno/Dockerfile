FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1 TZ=Europe/Madrid
RUN pip install --no-cache-dir -q apscheduler==3.11.3 SQLAlchemy
WORKDIR /trabajo
