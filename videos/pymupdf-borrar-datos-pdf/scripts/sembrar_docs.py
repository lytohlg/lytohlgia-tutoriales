#!/usr/bin/env python3
"""Fabrica cuatro documentos con datos personales INVENTADOS.

Nada de aquí es real: los nombres son de ejemplo y los números siguen el
formato oficial para que los patrones de búsqueda funcionen igual que con
un documento de verdad. Los datos viven en datos.py, en un único sitio.

Además deja en datos_conocidos.txt la lista EXACTA de lo que se ha
sembrado: eso es la verdad de referencia para verificar después, sin
depender del contador del propio script.
"""
import os

import fitz

from datos import (CUENTA_A, DNI_A, DNI_B, DNI_B_PUNTOS, EMAIL_A, EMAIL_B,
                   NOMBRE_A, NOMBRE_B, TELEFONO)

DOCS = [
    ("contrato_alquiler.pdf", "CONTRATO DE ARRENDAMIENTO", [
        "Entre D.ª %s, con DNI %s, y" % (NOMBRE_A, DNI_A),
        "D. %s, con DNI %s, se firma el" % (NOMBRE_B, DNI_B),
        "presente contrato sobre la vivienda de la calle Alcalá 45,",
        "3.º B, 28014 Madrid.",
        "",
        "CLÁUSULA TERCERA. La renta mensual se fija en 780 euros,",
        "pagadera los cinco primeros días de cada mes mediante",
        "transferencia a la cuenta %s." % CUENTA_A,
        "",
        "CLÁUSULA SÉPTIMA. Cualquier aviso se comunicará al",
        "teléfono %s o al correo %s." % (TELEFONO, EMAIL_A),
        "",
        "En Madrid, a 4 de marzo de 2026.",
    ], {"author": NOMBRE_A, "title": "Contrato de arrendamiento",
        "creator": "Gestoría Peñalver", "producer": "Microsoft® Word 2019",
        "subject": "Alcalá 45, 3.º B", "keywords": "alquiler, contrato"}),
    ("nomina_marzo.pdf", "RECIBO DE SALARIOS — MARZO 2026", [
        "Trabajador: %s" % NOMBRE_B,
        "DNI: %s" % DNI_B,
        "Grupo profesional: 3   Antigüedad: 2021-02-01",
        "",
        "Salario base ...................... 1.420,00",
        "Complemento de puesto ............   180,00",
        "Prorrata pagas extras ............   236,67",
        "TOTAL DEVENGADO .................. 1.836,67",
        "",
        "Domiciliación: %s" % CUENTA_A,
        "Teléfono: %s" % TELEFONO,
        "",
        "Titular de la cuenta (según el banco): %s" % DNI_B_PUNTOS,
    ], {"author": "Departamento de nóminas", "title": "Nómina marzo 2026",
        "creator": "A3nom", "producer": "PDFlib 9.1"}),
    ("informe_medico.pdf", "INFORME DE ALTA — CONSULTA DE PSIQUIATRÍA", [
        "Paciente: %s" % NOMBRE_A,
        "DNI: %s   Fecha de nacimiento: 1979-11-02" % DNI_A,
        "",
        "Motivo de consulta: episodio de ansiedad generalizada.",
        "Diagnóstico: trastorno de ansiedad, en seguimiento.",
        "Tratamiento: se ajusta la pauta y se revisa en un mes.",
        "",
        "Datos de contacto para la cita: %s" % TELEFONO,
        "correo %s" % EMAIL_A,
    ], {"author": "Dra. Elena Sanz", "title": "Informe de alta",
        "creator": "Historia clínica", "producer": "iText 5.5"}),
    ("curriculum.pdf", "CURRICULUM VITAE", [
        NOMBRE_B,
        "calle Alcalá 45, 3.º B, 28014 Madrid",
        "Teléfono %s — %s" % (TELEFONO, EMAIL_B),
        "",
        "EXPERIENCIA",
        "2021 - actualidad   Técnico de mantenimiento industrial",
        "2016 - 2021         Operario de línea de producción",
        "",
        "FORMACIÓN",
        "Grado medio en instalaciones electrotécnicas",
    ], {"author": NOMBRE_B, "title": "CV Antonio Vidal",
        "creator": "Canva", "producer": "Skia/PDF m120"}),
]

# Lo que se ha sembrado, tal cual aparece en los documentos: la verdad de
# referencia. Incluye la forma con puntos que el primer patrón no ve.
CONOCIDOS = [DNI_A, DNI_B, DNI_B_PUNTOS, CUENTA_A, TELEFONO, EMAIL_A, EMAIL_B]


def main():
    os.makedirs("entrada", exist_ok=True)
    for nombre, titulo, lineas, meta in DOCS:
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        page.insert_textbox(fitz.Rect(60, 60, 535, 120), titulo,
                            fontsize=14, fontname="hebo", align=0)
        page.insert_textbox(fitz.Rect(60, 130, 535, 760), "\n".join(lineas),
                            fontsize=11, fontname="helv", lineheight=1.6)
        doc.set_metadata(meta)
        ruta = os.path.join("entrada", nombre)
        doc.save(ruta)
        doc.close()
        print("%-24s %5d bytes   1 página   autor: %s"
              % (nombre, os.path.getsize(ruta), meta.get("author", "")))
    with open("datos_conocidos.txt", "w") as f:
        f.write("\n".join(CONOCIDOS) + "\n")
    print("documentos creados: %d | datos sembrados: %d"
          % (len(DOCS), len(CONOCIDOS)))


if __name__ == "__main__":
    main()
