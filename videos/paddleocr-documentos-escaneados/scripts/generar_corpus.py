#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el corpus de prueba: documentos "escaneados" (imagen dentro de un PDF, sin capa de
texto) más su verdad exacta (ground_truth.json).

Todos los datos son INVENTADOS: no hay información de ninguna persona ni empresa real.
La idea es tener documentos cuyo contenido conocemos letra a letra para poder COMPROBAR
lo que devuelve el OCR, en lugar de mirarlo y decir "parece que está bien".
"""
import json
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALIDA = os.path.join(RAIZ, 'documentos')
# Carpeta aparte: una factura que «acaba de llegar» y todavía no está en el índice.
# Sirve para enseñar que indexar es incremental: solo se lee lo nuevo.
SALIDA_NUEVAS = os.path.join(RAIZ, 'documentos_nuevos')
FUENTE = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FUENTE_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

CLIENTES = [
    ('Ferreteria Vega S.L.', 'B12345674', 'Calle Mayor 14, 3B'),
    ('Talleres Rios S.A.', 'A87654321', 'Poligono Norte, nave 7'),
    ('Suministros Norte S.L.', 'B45678912', 'Avenida del Puerto 22'),
    ('Panaderia El Trigal', 'B33445566', 'Plaza Vieja 3'),
    ('Clinica Dental Sonrisa', 'B99887766', 'Calle Salud 9, 1A'),
    ('Muebles Arce S.L.', 'B11223344', 'Camino del Rio 108'),
    ('Talleres Perez e Hijos', 'B55667788', 'Calle Industria 45'),
]

CONCEPTOS = [
    ('Mantenimiento anual', 1, 240.00),
    ('Reparacion de motor', 1, 385.50),
    ('Suministro de material', 12, 18.75),
    ('Servicio de limpieza', 4, 95.00),
    ('Revision de instalacion', 1, 162.30),
    ('Horas de asistencia tecnica', 6, 47.50),
    ('Portes y embalaje', 1, 38.00),
    ('Consultoria fiscal', 3, 110.00),
]


def fuente(ruta, tam):
    return ImageFont.truetype(ruta, tam)


def escanear(img):
    """Convierte una imagen limpia en algo con pinta de escaneo real: giro leve, ruido y JPEG."""
    img = img.rotate(random.uniform(-1.1, 1.1), expand=True, fillcolor='white')
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    px = img.load()
    an, al = img.size
    for _ in range(int(an * al * 0.0008)):
        x, y = random.randrange(an), random.randrange(al)
        v = random.randint(120, 210)
        px[x, y] = (v, v, v)
    return img


def factura(num, cliente, cif, direccion, concepto, cantidad, precio, fecha, serie):
    importe = round(cantidad * precio, 2)
    iva = round(importe * 0.21, 2)
    total = round(importe + iva, 2)
    lineas = [
        ('b', 'FACTURA'),
        ('b', f'Numero: {num}   Serie: {serie}'),
        ('', f'Fecha: {fecha}'),
        ('', ''),
        ('b', 'Datos del cliente'),
        ('', cliente),
        ('', f'CIF: {cif}'),
        ('', direccion),
        ('', ''),
        ('b', 'Detalle'),
        ('', 'Concepto                       Cantidad    Precio     Importe'),
        ('', f'{concepto:<30} {cantidad:>6}   {precio:>8.2f}  {importe:>9.2f}'),
        ('', ''),
        ('', f'Base imponible: {importe:.2f} EUR'),
        ('', f'IVA 21%: {iva:.2f} EUR'),
        ('b', f'TOTAL A PAGAR: {total:.2f} EUR'),
        ('', ''),
        ('', 'Forma de pago: transferencia a 30 dias.'),
        ('', 'Documento generado para pruebas. Datos ficticios.'),
    ]
    return lineas, importe, iva, total


def contrato(paginas_texto):
    lineas = []
    for i, bloque in enumerate(paginas_texto):
        if i:
            lineas.append(('s', None))
        for j, l in enumerate(bloque):
            lineas.append(('b', l) if j == 0 else ('', l))
    return lineas


def render(lineas, ancho=1240):
    """Dibuja las lineas en una o varias imagenes (A4 aprox a 150 dpi)."""
    alto = 1754
    margen = 70
    imgs = []
    pagina = Image.new('RGB', (ancho, alto), 'white')
    d = ImageDraw.Draw(pagina)
    y = margen
    for tipo, texto in lineas:
        if tipo == 's':                       # salto de pagina
            imgs.append(pagina)
            pagina = Image.new('RGB', (ancho, alto), 'white')
            d = ImageDraw.Draw(pagina)
            y = margen
            continue
        if texto is None:
            continue
        f = fuente(FUENTE_B if tipo == 'b' else FUENTE, 26 if tipo == 'b' else 24)
        d.text((margen, y), texto, fill=(20, 20, 20), font=f)
        y += 36
    imgs.append(pagina)
    return imgs


def main():
    random.seed(20261016)
    os.makedirs(SALIDA, exist_ok=True)
    verdad = []

    # --- 5 facturas de una pagina -------------------------------------------------
    for i, (cliente, cif, direccion) in enumerate(CLIENTES[:5], start=1):
        concepto, cantidad, precio = CONCEPTOS[(i - 1) % len(CONCEPTOS)]
        num = f'F-2026-{440 + i:04d}'
        serie = f'SER-{i:03d}'
        fecha = f'{random.randint(1, 28):02d}/0{random.randint(1, 9)}/2026'
        lineas, base, iva, total = factura(num, cliente, cif, direccion, concepto, cantidad,
                                           precio, fecha, serie)
        imgs = [escanear(p) for p in render(lineas)]
        ruta = os.path.join(SALIDA, f'factura_{i:02d}_{num}.pdf')
        imgs[0].save(ruta, 'PDF', resolution=150.0)
        texto = '\n'.join(t for _, t in lineas if t)
        verdad.append({
            'archivo': os.path.basename(ruta), 'paginas': 1,
            'numero_factura': num, 'cliente': cliente, 'cif': cif, 'fecha': fecha,
            'base_imponible': base, 'iva': iva, 'total': total,
            'texto': texto,
        })

    # --- 1 contrato de 2 paginas --------------------------------------------------
    bloque = [
        'CONTRATO DE MANTENIMIENTO ANUAL',
        'Referencia del contrato: MANT-2026-03',
        'Entre: Suministros Norte S.L. (CIF B45678912)',
        'Y: Mantenimientos Ordoñez (CIF B77889900)',
        'Fecha de firma: 03/05/2026',
        'Duracion: doce meses, prorrogable.',
        'Importe anual: 4.800,00 EUR mas IVA.',
        'El mantenimiento incluye dos visitas trimestrales,',
        'reposicion de piezas de desgaste y asistencia remota',
        'en horario de oficina. No incluye obra civil.',
        'Las averias se comunican al telefono XXX XXX XXX',
        'o por correo a soporte@example.com.',
        'Ninguna de las partes cede este contrato a terceros.',
    ]
    firmas = [
        'Firmado por la parte contratante,',
        'en la fecha indicada en la primera pagina.',
        'Documento de prueba con datos ficticios.',
    ]
    lineas = contrato([bloque, firmas])
    imgs = [escanear(p) for p in render(lineas)]
    ruta = os.path.join(SALIDA, 'contrato_mantenimiento_2026.pdf')
    imgs[0].save(ruta, 'PDF', resolution=150.0, save_all=True, append_images=imgs[1:])
    verdad.append({
        'archivo': os.path.basename(ruta), 'paginas': len(imgs),
        'referencia': 'MANT-2026-03', 'importe_anual': '4.800,00',
        'texto': '\n'.join(t for _, t in lineas if t),
    })

    # --- 1 factura que «acaba de llegar»: va a otra carpeta ------------------------
    # No está en documentos/ todavía: la escena del índice la copia y enseña que
    # solo se lee lo nuevo (lo ya indexado no se repite).
    cliente, cif, direccion = CLIENTES[5]
    concepto, cantidad, precio = CONCEPTOS[5]
    num = 'F-2026-0446'
    lineas, base, iva, total = factura(num, cliente, cif, direccion, concepto, cantidad,
                                       precio, '12/10/2026', 'SER-006')
    os.makedirs(SALIDA_NUEVAS, exist_ok=True)
    imgs = [escanear(p) for p in render(lineas)]
    ruta = os.path.join(SALIDA_NUEVAS, f'factura_06_{num}.pdf')
    imgs[0].save(ruta, 'PDF', resolution=150.0)
    verdad.append({
        'archivo': os.path.basename(ruta), 'paginas': 1,
        'numero_factura': num, 'cliente': cliente, 'cif': cif, 'fecha': '12/10/2026',
        'base_imponible': base, 'iva': iva, 'total': total,
        'texto': '\n'.join(t for _, t in lineas if t),
    })

    # --- 1 documento MAL escaneado (para la escena de limites) --------------------
    lineas, base, iva, total = factura('F-2026-0999', 'Cliente Borroso S.L.', 'B00000000',
                                       'Calle Sin Numero 1', 'Reparacion urgente', 2, 133.33,
                                       '30/09/2026', 'SER-999')
    mala = render(lineas)[0].resize((420, 594)).filter(ImageFilter.GaussianBlur(1.6))
    mala.save(os.path.join(SALIDA, 'factura_mal_escaneada.jpg'), 'JPEG', quality=22)

    with open(os.path.join(RAIZ, 'ground_truth.json'), 'w', encoding='utf-8') as f:
        json.dump(verdad, f, ensure_ascii=False, indent=2)

    print(f'corpus generado en {SALIDA}')
    a_indexar = [v for v in verdad if not v['archivo'].startswith('factura_mal')]
    print(f'  documentos: {len(a_indexar)} ficheros, '
          f'{sum(v["paginas"] for v in a_indexar)} paginas')
    for v in a_indexar:
        carpeta = SALIDA_NUEVAS if v['archivo'].startswith('factura_06') else SALIDA
        print(f'   - {os.path.basename(carpeta)}/{v["archivo"]} ({v["paginas"]} pag.)')
    print('  factura_mal_escaneada.jpg NO se indexa: es el caso de limite')


if __name__ == '__main__':
    main()
