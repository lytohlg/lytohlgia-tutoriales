"""panel.py — el proceso largo en una sola pantalla que se redibuja.

Mismo trabajo que lote_print.py (procesar.procesar), pero en vez de escupir una
línea por fichero, la pantalla se repinta: lo hecho, lo que va ahora, lo que
falta y lo que falló, cada cosa en su sitio. Los fallos se quedan a la vista
aunque la tabla siga avanzando.

Uso:  python3 panel.py [--pausa 0.02] [--espera-final 6]
"""
import argparse
import time

from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, ProgressBar, Static

import procesar

CSS = """
Screen {
    background: #10131a;
    color: #cfd6e3;
}
#cabecera {
    height: 3;
    padding: 0 1;
    background: #1a2030;
    color: #8be9c0;
    text-style: bold;
}
#cuerpo { height: 1fr; }
#tabla { width: 2fr; border: round #3a4a66; }
#lateral { width: 1fr; padding: 0 1; }
#hechos { height: 3; color: #8be9c0; }
#fallos { height: 1fr; color: #ff9d9d; }
#barra { height: 1; margin: 0 1; }
#pie { height: 1; padding: 0 1; background: #1a2030; }
"""


class Panel(App):
    CSS = CSS
    TITLE = "CONVERSIÓN DE EXTRACTOS"

    def __init__(self, pausa: float = 0.02, espera_final: float = 6.0):
        super().__init__()
        self.pausa = pausa
        self.espera_final = espera_final
        self.hechos = 0
        self.errores = 0
        self.lista_fallos: list[str] = []

    def compose(self) -> ComposeResult:
        yield Static("CONVERSIÓN DE EXTRACTOS · 1 JSON por fichero", id="cabecera")
        with Horizontal(id="cuerpo"):
            yield DataTable(id="tabla")
            with Vertical(id="lateral"):
                yield Static("HECHOS  0", id="hechos")
                yield Static("", id="fallos")
        yield ProgressBar(total=100, show_eta=False, id="barra")
        yield Static("", id="pie")

    def on_mount(self) -> None:
        tabla = self.query_one("#tabla", DataTable)
        tabla.add_column("#", key="n", width=4)
        tabla.add_column("fichero", key="f")
        tabla.add_column("filas", key="filas", width=6)
        tabla.add_column("importe", key="imp", width=10)
        tabla.add_column("estado", key="est", width=8)
        tabla.cursor_type = "none"
        self.query_one("#fallos", Static).update(Text("FALLOS  0", style="bold #ff9d9d"))
        self.procesar_lote()

    @work(thread=True, exclusive=True)
    def procesar_lote(self) -> None:
        """El bucle de trabajo. En un hilo aparte: la pantalla sigue respondiendo."""
        pendientes = procesar.ficheros()
        total = len(pendientes)
        self.call_from_thread(self.query_one("#barra", ProgressBar).update, total=total, progress=0)
        for i, ruta in enumerate(pendientes, 1):
            try:
                filas, importe = procesar.procesar(ruta)
                self.call_from_thread(self.anadir, i, ruta.name, str(filas), f"{importe:,.2f}",
                                      "ok", i, total)
            except Exception as e:              # noqa: BLE001 — el fallo se pinta, no se tapa
                self.call_from_thread(self.anadir, i, ruta.name, "-", "-", "ERROR", i, total)
                self.call_from_thread(self.anotar_fallo, ruta.name, str(e))
            time.sleep(self.pausa)
        self.call_from_thread(self.cerrar)

    def anadir(self, n: int, nombre: str, filas: str, importe: str, estado: str, i: int, total: int) -> None:
        tabla = self.query_one("#tabla", DataTable)
        tabla.add_row(f"{n:03d}", nombre, filas, importe, estado,
                      key=f"f{n}", height=1)
        tabla.scroll_end(animate=False)
        self.hechos += 1
        if estado != "ok":
            self.query_one("#tabla", DataTable).update_cell(f"f{n}", "est", "ERROR")
        self.query_one("#hechos", Static).update(f"HECHOS  {self.hechos - self.errores}")
        self.query_one("#barra", ProgressBar).update(progress=i)
        self.query_one("#pie", Static).update(
            f"{i}/{total} ficheros · {self.hechos - self.errores} ok · {self.errores} con error "
            f"· quedan {total - i}")

    def anotar_fallo(self, nombre: str, motivo: str) -> None:
        self.errores += 1
        self.lista_fallos.append(nombre)
        texto = Text()
        texto.append(f"FALLOS  {self.errores}\n", style="bold #ff9d9d")
        for f in self.lista_fallos:
            texto.append(f"✗ {f}\n", style="#ff9d9d")
        texto.append("\nse quedan aquí,\nno se van con el scroll", style="dim")
        self.query_one("#fallos", Static).update(texto)

    def cerrar(self) -> None:
        self.query_one("#cabecera", Static).update(
            f"LISTO · {self.hechos - self.errores} correctos · {self.errores} con error")
        self.query_one("#pie", Static).update(
            f"{self.hechos} JSON en salida/ · los {self.errores} fallos, a la vista")
        # Repintado completo antes de quedarse quieto: sin esto quedan celdas
        # sueltas del layout anterior (los primeros frames) pegadas en el borde.
        self.screen.refresh(repaint=True, layout=True)
        self.set_timer(self.espera_final, self.exit)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pausa", type=float, default=0.02)
    ap.add_argument("--espera-final", type=float, default=6.0)
    a = ap.parse_args()
    Panel(pausa=a.pausa, espera_final=a.espera_final).run(mouse=False)
