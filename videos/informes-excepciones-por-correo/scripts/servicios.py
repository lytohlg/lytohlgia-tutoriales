#!/usr/bin/env python3
"""Utilidades de los dos servidores de prueba: el correo y el S3 local.

Se llama desde los scripts de shell, que solo miran el código de salida:

    python3 scripts/servicios.py puerto 8025   -> 0 si el puerto ya responde
    python3 scripts/servicios.py s3            -> deja listo el bucket del informe
    python3 scripts/servicios.py vaciar        -> vacía el buzón de pruebas
"""
import socket
import sys
import urllib.request

DIRECCION = "127.0.0.1"
BUZON = f"http://{DIRECCION}:8025"
S3 = f"http://{DIRECCION}:5000"


def puerto(numero: str) -> int:
    """0 si algo escucha ya en ese puerto (para no arrancar dos veces lo mismo)."""
    with socket.socket() as conexion:
        conexion.settimeout(1)
        return 0 if conexion.connect_ex((DIRECCION, int(numero))) == 0 else 1


def s3() -> int:
    """Crea el bucket donde la herramienta publica el informe.

    Las credenciales son de mentira: el S3 es local y no sale de la máquina.
    """
    import boto3
    from botocore.client import Config

    cliente = boto3.client(
        "s3",
        endpoint_url=S3,
        aws_access_key_id="demo",
        aws_secret_access_key="demo-local",
        region_name="us-east-1",
        config=Config(signature_version="v4"),
    )
    try:
        cliente.create_bucket(Bucket="informes")
    except cliente.exceptions.BucketAlreadyOwnedByYou:
        pass
    return 0


def vaciar() -> int:
    """Vacía el buzón: así los recuentos de correos son de esta ejecución."""
    peticion = urllib.request.Request(BUZON + "/api/v1/messages", method="DELETE")
    urllib.request.urlopen(peticion, timeout=15).read()
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "puerto":
        sys.exit(puerto(sys.argv[2]))
    sys.exit({"s3": s3, "vaciar": vaciar}[sys.argv[1]]())
