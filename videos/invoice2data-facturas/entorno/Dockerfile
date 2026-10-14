# Máquina de pruebas del material: Python con invoice2data dentro.
FROM python:3.13-slim

# Versiones fijadas a propósito: la demo tiene que seguir dando el mismo
# resultado dentro de un año. pdfminer.six es el motor que lee la capa de texto
# del PDF; invoice2data es la herramienta que extrae los campos.
RUN pip install --no-cache-dir invoice2data==1.0.1 pdfminer.six==20260107

# Los comandos de la demo son relativos, así que da igual desde dónde se
# ejecuten; aquí todo el trabajo ocurre dentro de /trabajo.
WORKDIR /trabajo

CMD ["bash"]
