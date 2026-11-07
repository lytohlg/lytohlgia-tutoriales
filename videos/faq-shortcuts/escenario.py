#!/usr/bin/env python3
"""Genera el escenario de la demo: un historial SINTÉTICO con el formato exacto
que dejan Claude Code, Codex y Cursor en una carpeta personal.

No hay datos de nadie: las peticiones son inventadas y la credencial que aparece
en el vídeo es falsa (se compone por partes para que no parezca una clave real).

Uso:  python3 escenario.py
Crea: entrada/home/...            carpeta personal simulada
      entrada/proyecto-facturas/  el proyecto sobre el que se pregunta
"""
import json
import shutil
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENTRADA = BASE / "entrada"
PROJ = str(ENTRADA / "proyecto-facturas")          # ruta REAL dentro del contenedor
HOME = ENTRADA / "home"

# Peticiones del día a día de un proyecto de facturas (todas inventadas).
P = [
    ("2026-08-12", "revisa el csv de facturas de agosto y dime que filas no cuadran"),
    ("2026-08-13", "revisa el csv de facturas de agosto y dime que filas no cuadran"),
    ("2026-08-19", "revisa el csv de facturas de agosto y dime que filas no cuadran"),
    ("2026-08-21", "genera el pdf de la factura 2026-101 con el logo nuevo"),
    ("2026-08-24", "resume los cambios del ultimo commit en dos lineas"),
    ("2026-08-26", "revisa el csv de facturas de agosto y dime que filas no cuadran"),
    ("2026-08-28", "busca los clientes sin nif en la base de datos"),
    ("2026-09-01", "genera el pdf de la factura 2026-104 con el logo nuevo"),
    ("2026-09-02", "revisa el csv de facturas de septiembre y dime que filas no cuadran"),
    ("2026-09-03", "prepara el correo de recordatorio para las facturas vencidas"),
    ("2026-09-04", "resume los cambios del ultimo commit en dos lineas"),
    ("2026-09-07", "genera el pdf de la factura 2026-107 con el logo nuevo"),
    ("2026-09-08", "revisa el csv de facturas de septiembre y dime que filas no cuadran"),
    ("2026-09-10", "busca los clientes sin nif en la base de datos"),
    ("2026-09-11", "prepara el correo de recordatorio para las facturas vencidas"),
    ("2026-09-14", "genera el pdf de la factura 2026-110 con el logo nuevo"),
    ("2026-09-15", "revisa el csv de facturas de septiembre y dime que filas no cuadran"),
    ("2026-09-17", "resume los cambios del ultimo commit en dos lineas"),
    ("2026-09-18", "genera el pdf de la factura 2026-113 con el logo nuevo"),
    ("2026-09-21", "revisa el csv de facturas de septiembre y dime que filas no cuadran"),
    ("2026-09-22", "prepara el correo de recordatorio para las facturas vencidas"),
    ("2026-09-24", "genera el pdf de la factura 2026-116 con el logo nuevo"),
    ("2026-09-25", "busca los clientes sin nif en la base de datos"),
    ("2026-09-28", "revisa el csv de facturas de septiembre y dime que filas no cuadran"),
    ("2026-09-29", "resume los cambios del ultimo commit en dos lineas"),
    ("2026-10-01", "genera el pdf de la factura 2026-119 con el logo nuevo"),
    ("2026-10-02", "prepara el correo de recordatorio para las facturas vencidas"),
    ("2026-10-05", "revisa el csv de facturas de septiembre y dime que filas no cuadran"),
    ("2026-10-06", "resume los cambios del ultimo commit en dos lineas"),
    ("2026-10-07", "genera el pdf de la factura 2026-122 con el logo nuevo"),
    ("2026-10-08", "busca los clientes sin nif en la base de datos"),
    ("2026-10-09", "prepara el correo de recordatorio para las facturas vencidas"),
]

# Credencial FALSA, montada por trozos: el literal completo nunca está en disco.
CREDENCIAL = "sk-" + "proj-" + "EJEMPLO" + "deClaveFalsa" + "1234567890"
SECRETO = "conecta con la api de facturacion usando " + CREDENCIAL + " y prueba el envio"
RUIDO = ["/model opus", "[Pasted text #1 +40 lines]", "/clear"]


def main():
    if ENTRADA.exists():
        shutil.rmtree(ENTRADA)
    HOME.mkdir(parents=True)
    proj = Path(PROJ)
    proj.mkdir()

    (proj / "facturas_2026.csv").write_text(
        "id;cliente;importe;iva\n101;ACME;1200,00;21\n104;Beta SL;980,50;21\n107;ACME;0,00;21\n",
        encoding="utf-8")
    (proj / "generar_pdf.py").write_text(
        '"""Genera el PDF de una factura con el logo de la empresa."""\n\n'
        'def generar(numero, salida="facturas/"):\n'
        '    print(numero, salida)\n', encoding="utf-8")

    # ---- Claude Code: transcripción de 2 sesiones + history.jsonl
    slug = PROJ.replace("/", "-")
    d = HOME / ".claude" / "projects" / slug
    d.mkdir(parents=True)
    ses = ["a1b2c3d4-0000-4000-8000-000000000001", "a1b2c3d4-0000-4000-8000-000000000002"]
    with (d / (ses[0] + ".jsonl")).open("w", encoding="utf-8") as fh:
        for i, (day, txt) in enumerate(P[:16]):
            fh.write(json.dumps({"type": "user", "sessionId": ses[0],
                                 "timestamp": "%sT09:%02d:00.000Z" % (day, 10 + i % 40),
                                 "message": {"role": "user", "content": txt}},
                                ensure_ascii=False) + "\n")
            fh.write(json.dumps({"type": "assistant", "sessionId": ses[0],
                                 "timestamp": "%sT09:%02d:40.000Z" % (day, 10 + i % 40),
                                 "message": {"role": "assistant",
                                             "content": [{"type": "text", "text": "Voy a revisarlo."}]}},
                                ensure_ascii=False) + "\n")
    with (HOME / ".claude" / "history.jsonl").open("w", encoding="utf-8") as fh:
        for i, (day, txt) in enumerate(P[16:]):
            fh.write(json.dumps({"display": txt, "project": PROJ, "sessionId": ses[1],
                                 "timestamp": "%sT18:%02d:00.000Z" % (day, 5 + i % 50)},
                                ensure_ascii=False) + "\n")
        for r in RUIDO:
            fh.write(json.dumps({"display": r, "project": PROJ, "sessionId": ses[1],
                                 "timestamp": "2026-10-09T19:00:00.000Z"},
                                ensure_ascii=False) + "\n")
        fh.write(json.dumps({"display": SECRETO, "project": PROJ, "sessionId": ses[1],
                             "timestamp": "2026-10-09T19:10:00.000Z"},
                            ensure_ascii=False) + "\n")
        fh.write(json.dumps({"display": "esto es de otro proyecto y no debe aparecer",
                             "project": str(ENTRADA / "proyecto-ajeno"), "sessionId": "zz",
                             "timestamp": "2026-10-09T19:11:00.000Z"},
                            ensure_ascii=False) + "\n")

    # ---- Codex
    cdir = HOME / ".codex" / "sessions" / "2026" / "10" / "01"
    cdir.mkdir(parents=True)
    with (cdir / "rollout-2026-10-01T09-00-00-0000000000aa.jsonl").open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"type": "session_meta", "payload": {
            "cwd": PROJ, "source": "cli", "originator": "codex_cli"}}) + "\n")
        for i, (day, txt) in enumerate(P[4:12]):
            fh.write(json.dumps({"type": "response_item", "timestamp": "%sT10:%02d:00.000Z" % (day, i),
                                 "payload": {"role": "user",
                                             "content": [{"type": "input_text", "text": txt}]}},
                                ensure_ascii=False) + "\n")
            fh.write(json.dumps({"type": "response_item", "payload": {"role": "assistant",
                                 "content": [{"type": "output_text", "text": "Hecho."}]}}) + "\n")
    with (cdir / "rollout-otro.jsonl").open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"type": "session_meta", "payload": {
            "cwd": str(ENTRADA / "otro"), "source": "cli", "originator": "codex_cli"}}) + "\n")
    with (cdir / "rollout-agente.jsonl").open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"type": "session_meta", "payload": {
            "cwd": PROJ, "source": "cli", "originator": "Claude Code"}}) + "\n")

    # ---- Cursor (SQLite de verdad)
    db = HOME / ".config" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
    db.parent.mkdir(parents=True)
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE cursorDiskKV (key TEXT PRIMARY KEY, value BLOB)")
    cid = "composer-facturas"
    conn.execute("INSERT INTO cursorDiskKV VALUES (?,?)", ("composerData:" + cid, json.dumps({
        "composerId": cid, "workspaceIdentifier": {"uri": {"fsPath": PROJ}},
        "createdAt": 1789000000000})))
    for i, (day, txt) in enumerate(P[10:16]):
        conn.execute("INSERT INTO cursorDiskKV VALUES (?,?)",
                     ("bubbleId:%s:%d" % (cid, i), json.dumps(
                         {"type": 1, "text": txt, "createdAt": 1789000000000 + i * 86400000})))
        conn.execute("INSERT INTO cursorDiskKV VALUES (?,?)",
                     ("bubbleId:%s:a%d" % (cid, i), json.dumps({"type": 2, "text": "respuesta"})))
    conn.commit()
    conn.close()

    n = sum(1 for f in ENTRADA.rglob("*") if f.is_file())
    print("escenario listo: %d ficheros en entrada/" % n)
    print("  proyecto:", PROJ)
    print("  home    :", HOME)


if __name__ == "__main__":
    main()
