#!/usr/bin/env python3
"""Convierte los correos del buzon en TAREAS CON VENCIMIENTO.

Que hace, en orden:
  1. se conecta al buzon por IMAP (imap_tools),
  2. para cada correo busca una REGLA por remitente,
  3. saca la fecha limite de una fecha explicita dd/mm/aaaa que aparezca
     en una frase con "vence" / "antes del",
  4. guarda la tarea en SQLite usando el Message-ID como clave unica:
     si el mismo correo se procesa dos veces, NO se duplica,
  5. mueve el correo ya convertido a la carpeta Procesados.

Uso:
    python3 reglas.py                 # procesa y mueve a Procesados
    python3 reglas.py --no-mover      # procesa y deja los correos en la entrada
    python3 reglas.py --db /tmp/x.db  # otra base de datos
"""
import argparse
import re
import sqlite3
from datetime import date, datetime

from imap_tools import MailBoxUnencrypted

HOST, PORT = "127.0.0.1", 3143
USUARIO_BUZON, PALABRA_BUZON = "compras@example.com", "demo"
DB = "tareas.db"
CARPETA_PROCESADOS = "Procesados"

# ── Las reglas: remitente -> tarea. Es un diccionario, se cambia sin tocar el resto.
REGLAS = [
    {"nombre": "facturas", "remitente": "facturacion@",
     "tarea": "Revisar y pagar la factura", "tipo": "pago"},
    {"nombre": "presupuestos", "remitente": "pedidos@",
     "tarea": "Responder al presupuesto", "tipo": "respuesta"},
]

PALABRAS_FECHA = ("vence", "antes del", "fecha limite", "fecha límite")
RE_FECHA = re.compile(r"(\d{1,2})/(\d{1,2})/(\d{4})")


def crear_tabla(con):
    con.execute("""CREATE TABLE IF NOT EXISTS tareas (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        mensaje_id   TEXT UNIQUE,
        asunto       TEXT NOT NULL,
        remitente    TEXT NOT NULL,
        tarea        TEXT NOT NULL,
        tipo         TEXT NOT NULL,
        vencimiento  TEXT,
        origen       TEXT NOT NULL,
        creada       TEXT NOT NULL)""")


def regla_para(remitente):
    bajo = remitente.lower()
    for regla in REGLAS:
        if regla["remitente"] in bajo:
            return regla
    return None


def sacar_vencimiento(texto):
    """Devuelve 'AAAA-MM-DD' si hay una fecha explicita en una frase de plazo."""
    for trozo in re.split(r"(?<=[.!?])\s+|\n", texto):
        bajo = trozo.lower()
        if any(p in bajo for p in PALABRAS_FECHA):
            m = RE_FECHA.search(trozo)
            if m:
                dia, mes, anio = (int(g) for g in m.groups())
                try:
                    return date(anio, mes, dia).isoformat()
                except ValueError:
                    return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--no-mover", action="store_true")
    args = ap.parse_args()

    con = sqlite3.connect(args.db)
    crear_tabla(con)

    nuevas = repetidas = sin_regla = 0
    with MailBoxUnencrypted(HOST, PORT).login(USUARIO_BUZON, PALABRA_BUZON, "INBOX") as buzon:
        try:
            if not buzon.folder.exists(CARPETA_PROCESADOS):
                buzon.folder.create(CARPETA_PROCESADOS)
        except Exception:
            pass

        for m in buzon.fetch():
            regla = regla_para(m.from_)
            print(f"correo  {m.from_}  |  {m.subject}")
            if not regla:
                sin_regla += 1
                print("        -> sin regla: se queda en la entrada sin tocar")
                continue

            mensaje_id = (m.headers.get("message-id") or [""])[0] or f"uid-{m.uid}"
            vencimiento = sacar_vencimiento(f"{m.subject}\n{m.text or ''}")
            cur = con.execute(
                "INSERT OR IGNORE INTO tareas (mensaje_id, asunto, remitente, tarea,"
                " tipo, vencimiento, origen, creada) VALUES (?,?,?,?,?,?,?,?)",
                (mensaje_id, m.subject, m.from_, regla["tarea"], regla["tipo"],
                 vencimiento, f"IMAP uid {m.uid}",
                 datetime.now().isoformat(timespec="seconds")))

            if cur.rowcount:
                nuevas += 1
                print(f"        -> TAREA: {regla['tarea']} | tipo {regla['tipo']} | "
                      f"vence {vencimiento or 'SIN FECHA'}")
            else:
                repetidas += 1
                print("        -> ya tenia tarea (mismo Message-ID): no se duplica")

            if not args.no_mover:
                buzon.move(m.uid, CARPETA_PROCESADOS)

    con.commit()
    total = con.execute("SELECT COUNT(*) FROM tareas").fetchone()[0]
    print(f"\ncorreos leidos: {nuevas + repetidas + sin_regla} | tareas nuevas: {nuevas} | "
          f"sin duplicar: {repetidas} | sin regla: {sin_regla}")
    print(f"tareas en la base de datos: {total}")


if __name__ == "__main__":
    main()
