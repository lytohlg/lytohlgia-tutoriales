#!/usr/bin/env python3
"""Crea los datos de la demo: la contabilidad de una gestoria pequena.

Determinista: la misma version del script produce siempre los mismos ficheros
(misma semilla), asi que el manifiesto y los hashes del video se pueden repetir.

Uso: python3 crear_datos.py [--base CARPETA]

La carpeta por defecto es la subcarpeta datos de TRABAJO (y de la carpeta actual si TRABAJO
no esta definida).
"""
import argparse
import hashlib
import os
import random
from pathlib import Path

PROVEEDORES = [
    "Suministros Arenal S.L.", "Transportes Vega S.A.", "Papeleria Duero",
    "Mantenimiento Olmo", "Informatica Rigel", "Seguros Peninsular",
    "Limpiezas Norte", "Gestoria Roble", "Hosteleria Mar", "Talleres Cierzo",
]
CLIENTES = [
    "Clinica Aurora", "Estudio Prado", "Hotel Mino", "Panaderia Sur",
    "Ferreteria Lobos", "Optica Cierzo", "Cafes Roble", "Academia Sal",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def factura_csv(rnd: random.Random, numero: int, mes: str) -> str:
    prov = rnd.choice(PROVEEDORES)
    base = round(rnd.uniform(40, 1800), 2)
    iva = round(base * 0.21, 2)
    filas = ["concepto;importe", "servicio mensual;%.2f" % base]
    if rnd.random() < 0.4:
        filas.append("material;%.2f" % round(base * 0.2, 2))
    total = round(base + iva, 2)
    return (f"proveedor;{prov}\n"
            f"numero;F-{mes.replace('-', '')}-{numero:04d}\n"
            f"fecha;{mes}-{rnd.randint(1, 28):02d}\n"
            f"base;{base}\niva;{iva}\ntotal;{total}\n"
            + "\n".join(filas) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.path.join(os.environ.get("TRABAJO", "."), "datos"))
    a = ap.parse_args()

    base = Path(a.base)
    rnd = random.Random(20261013)  # semilla fija: demo reproducible

    (base / "facturas" / "2026-09").mkdir(parents=True, exist_ok=True)
    (base / "facturas" / "2026-10").mkdir(parents=True, exist_ok=True)
    (base / "contratos").mkdir(parents=True, exist_ok=True)
    (base / "notas").mkdir(parents=True, exist_ok=True)

    # clientes
    lineas = ["cliente;cif;alta;cuota"]
    for i, c in enumerate(CLIENTES, 1):
        lineas.append(f"{c};B{rnd.randint(10000000, 99999999)};2026-0{rnd.randint(1, 9)}-1{i%9};{rnd.choice([60, 90, 120])}")
    (base / "clientes.csv").write_text("\n".join(lineas) + "\n")

    # facturas: 40 en septiembre, 22 en octubre (octubre va a medias: es el mes en curso)
    for mes, n in (("2026-09", 40), ("2026-10", 22)):
        for i in range(1, n + 1):
            (base / "facturas" / mes / f"factura_{i:04d}.csv").write_text(factura_csv(rnd, i, mes))

    # contratos: 12 documentos con texto de verdad
    for i in range(1, 13):
        c = rnd.choice(CLIENTES)
        (base / "contratos" / f"contrato_{i:03d}.md").write_text(
            f"# Contrato de servicio {i:03d}\n\n"
            f"Cliente: {c}\n"
            f"Alta: 2026-{rnd.randint(1, 9):02d}-{rnd.randint(1, 28):02d}\n"
            f"Cuota mensual: {rnd.choice([60, 90, 120])} EUR\n"
            f"Renovacion: automatica si no hay aviso con 30 dias.\n")

    # notas
    for i in range(1, 6):
        (base / "notas" / f"nota_{i:02d}.md").write_text(
            f"Nota interna {i}\n\n"
            f"- Revisar {rnd.choice(PROVEEDORES)}\n"
            f"- Pendiente: {'llamar' if i % 2 else 'escribir'} antes del dia {rnd.randint(1, 28)}\n")

    ficheros = sorted(p for p in base.rglob("*") if p.is_file())
    total = sum(p.stat().st_size for p in ficheros)
    # manifiesto: sha256 de cada fichero, en orden -> permite comparar sin volver a leer todo
    manifiesto = {str(p.relative_to(base)): sha256(p) for p in ficheros}
    suma = hashlib.sha256("\n".join(f"{k} {v}" for k, v in sorted(manifiesto.items())).encode()).hexdigest()

    print(f"datos creados en {base}")
    print(f"  ficheros : {len(ficheros)}")
    print(f"  tamano   : {total / 1024:.1f} KB")
    print(f"  sha256 del manifiesto: {suma[:16]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
