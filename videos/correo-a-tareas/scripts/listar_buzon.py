#!/usr/bin/env python3
"""Lee el buzon por IMAP con imap_tools y ensena lo que hay dentro.

Uso:
    python3 listar_buzon.py              # asunto, remitente, fecha y adjuntos
    python3 listar_buzon.py --adjuntos   # ademas, el contenido del adjunto
    python3 listar_buzon.py --carpetas   # carpetas del buzon
"""
import argparse

from imap_tools import MailBoxUnencrypted

HOST, PORT = "127.0.0.1", 3143
USUARIO_BUZON, PALABRA_BUZON = "compras@example.com", "demo"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adjuntos", action="store_true")
    ap.add_argument("--carpetas", action="store_true")
    args = ap.parse_args()

    with MailBoxUnencrypted(HOST, PORT).login(USUARIO_BUZON, PALABRA_BUZON, "INBOX") as buzon:
        if args.carpetas:
            print("carpetas del buzon:")
            for c in buzon.folder.list():
                print(f"  - {c.name}")
            return

        n = 0
        for m in buzon.fetch():
            n += 1
            adjuntos = ", ".join(a.filename for a in m.attachments) or "-"
            print(f"[{n}] uid={m.uid} {m.date_str}")
            print(f"    de     : {m.from_}")
            print(f"    asunto : {m.subject}")
            print(f"    adjunto: {adjuntos}")
            if args.adjuntos:
                for a in m.attachments:
                    print(f"      --- {a.filename} ({a.content_type}) ---")
                    for linea in a.payload.decode("utf-8", "replace").splitlines()[:4]:
                        print(f"      {linea}")
        print(f"\n{n} correos en la bandeja de entrada")


if __name__ == "__main__":
    main()
