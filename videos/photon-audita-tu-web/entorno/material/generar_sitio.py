#!/usr/bin/env python3
"""Genera el sitio de prueba que se audita en la demo.

Todo es FALSO y de ejemplo: los correos usan el dominio reservado example.com (RFC 2606) y
el token es inventado. Se genera en tiempo de ejecución para que el paquete no tenga que
publicar binarios ni ficheros ejecutables del sitio.

Uso:  python3 generar_sitio.py [directorio_destino]
"""
import pathlib
import sys

DESTINO = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sitio")
for sub in ("", "files", "assets", "admin", "blog"):
    (DESTINO / sub).mkdir(parents=True, exist_ok=True)

index = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Nordika — reformas integrales</title></head><body>
<h1>Nordika</h1>
<p>Reformas integrales en el norte. Presupuesto sin compromiso.</p>
<nav>
<a href="equipo.html">Equipo</a>
<a href="servicios.html">Servicios</a>
<a href="blog.html">Blog</a>
<a href="contacto.html">Contacto</a>
</nav>
<footer>Nordika SL
<a href="admin/panel.html">Panel interno</a>
</footer>
<script src="assets/app.js"></script>
</body></html>"""

equipo = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Equipo</title></head><body>
<h1>Equipo</h1>
<p>Direccion: laura.mendez@example.com</p>
<p>Presupuestos: presupuestos@example.com</p>
<p>Obras: jorge.puente@example.com</p>
<p>Antiguo contacto (no borrar): admin@example.com</p>
<!-- pendiente de borrar antes de publicar: c9K2mQ4tR7yX1zVb3Nw9Hp5L -->
</body></html>"""

servicios = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Servicios</title></head><body>
<h1>Servicios</h1>
<ul>
<li>Reforma de bano</li>
<li>Reforma de cocina</li>
<li>Locales</li>
</ul>
<p>Descarga el dossier:</p>
<a href="files/dossier-2026.pdf">dossier PDF</a>
</body></html>"""

blog = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Blog</title></head><body>
<h1>Blog</h1>
<a href="blog/precios-2026.html">Como calculamos el precio</a>
<a href="blog/permisos.html">Permisos de obra</a>
</body></html>"""

blog1 = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Precios</title></head><body>
<h1>Como calculamos el precio</h1>
<p>Tarifa interna 2026 (provisional).</p>
<a href="files/tarifas-internas-2026.xlsx">tarifas</a>
</body></html>"""

blog2 = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Permisos</title></head><body>
<h1>Permisos de obra</h1><p>Texto de ejemplo.</p>
</body></html>"""

contacto = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Contacto</title></head><body>
<h1>Contacto</h1>
<form action="enviar.php" method="post"><input name="email"><button>Enviar</button></form>
<a href="https://www.linkedin.com/company/ejemplo-reformas">LinkedIn</a>
<a href="https://twitter.com/ejemplo_reformas">Twitter</a>
</body></html>"""

admin = """<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Panel</title></head><body>
<h1>Panel interno</h1><p>Listado de clientes y facturas.</p>
<p>contacto.backup@example.com</p>
</body></html>"""

# El endpoint se compone en dos trozos: el fichero que publicamos no debe llevar rutas
# absolutas sueltas (guardarraíl de privacidad del paquete).
api = "/" + "api/v1/clientes"
appjs = (
    "// cliente de la web\n"
    f'const API = "{api}";\n'
    f'const INTERNA = "{api}?page=1";\n'
    "async function carga(){\n"
    "  const r = await fetch(INTERNA);\n"
    "  return r.json();\n"
    "}\n"
    'document.addEventListener("DOMContentLoaded", carga);\n'
)

ficheros = {
    "index.html": index,
    "equipo.html": equipo,
    "servicios.html": servicios,
    "blog.html": blog,
    "blog/precios-2026.html": blog1,
    "blog/permisos.html": blog2,
    "contacto.html": contacto,
    "admin/panel.html": admin,
    "assets/app.js": appjs,
}
for nombre, texto in ficheros.items():
    (DESTINO / nombre).write_text(texto, encoding="utf-8")

# Ficheros "sensibles" de mentira: solo hacen falta para que el crawler los detecte.
(DESTINO / "files" / "tarifas-internas-2026.xlsx").write_bytes(b"PK\x03\x04ejemplo" + b"0" * 900)
(DESTINO / "files" / "dossier-2026.pdf").write_bytes(b"%PDF-1.4\n" + b"ejemplo\n" * 200)

print(f"sitio de prueba generado en {DESTINO} ({len(ficheros) + 2} ficheros)")
