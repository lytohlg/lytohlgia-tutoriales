# Entorno de pruebas del vídeo «SkillCorpus: 222 skills de agente filtradas y buscables con Python»
# — @lytohlgIA
# ---------------------------------------------------------------------------
# Esta es la máquina donde se probó el material (la misma que se ve en el vídeo). Se construye con:
#     docker --context default build -t repro-skillcorpus:local entorno
# Reglas: versiones fijadas donde importa (imagen base y COMMIT del repositorio que se clona), nada
# de datos personales dentro, y el contenedor preparado para correr SIN privilegios (usuario
# 1000:1000), que es como se prueba: por eso los directorios que la demo escribe quedan a nombre del
# usuario 1000 y no de root.
FROM python:3.13-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore

# git para clonar el repositorio y ca-certificates para HTTPS.
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Dependencias del repositorio (CPU, sin GPU): las mismas que quedan instaladas en el vídeo antes de
# `pip install -e .`. Se dejan en la imagen para que la demo no pierda minutos bajándolas.
RUN pip install --no-cache-dir -q pyyaml numpy click faiss-cpu sqlite-vec openai pyarrow zstandard

# El repositorio REAL de SkillCorpus, FIJADO por commit: la revisión que se usó al grabar
# (main del 2026-09-17). Sin el pin, mañana este material enseñaría otra cosa, porque el repositorio
# sigue cambiando y el recuento de skills ya no cuadraría con el del vídeo.
ARG SKILLCORPUS_COMMIT=7b3a0eaec5594b7f6cb301189c3d626f15409ed0
RUN git clone -q https://github.com/EverMind-AI/SkillCorpus /opt/skillcorpus \
 && git -C /opt/skillcorpus checkout -q "${SKILLCORPUS_COMMIT}" \
 && git -C /opt/skillcorpus log -1 --format='SkillCorpus fijado en %h (%ad)' --date=short \
 && pip install --no-cache-dir --no-deps -q -e /opt/skillcorpus

# Los ficheros de la demo (config, registro de fuentes e informe) van a /opt/deploy, con la MISMA
# ruta que en el vídeo: así ninguno de los comandos del vídeo cambia una coma.
COPY deploy /opt/deploy

# /work/lib es donde se construye el corpus; /opt/deploy se escribe al arrancar la demo.
RUN mkdir -p /work/lib \
 && chown -R 1000:1000 /work /opt/deploy

# El contenedor de prueba corre como usuario 1000 y la demo ejecuta `pip install -e .` dentro (es uno
# de los comandos del vídeo): eso escribe en el árbol de Python de la imagen y en /usr/local/bin, así
# que esos dos sitios se dejan a nombre del usuario 1000. Sin esto, `pip install -e .` falla con
# «Permission denied» y la demo no reproduce el vídeo tal cual.
RUN chown -R 1000:1000 /usr/local/lib/python3.13/site-packages /usr/local/bin

WORKDIR /work
