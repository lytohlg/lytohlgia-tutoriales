"""Prueba: ¿qué pasa si el modelo pide una herramienta que el driver NO implementa?"""
from anthropic.types.beta import BetaToolUseBlock
from anthropic.tools import ToolError
from anthropic.tools.browser import BetaURLContext, BetaURLPolicy

from cdp_browser import CdpBrowser


def policy(_c: BetaURLContext, url: str) -> None:
    if not url.startswith("about:"):
        raise ToolError("blocked: nada de red en esta prueba")


b = CdpBrowser(headless=True, url_policy=policy)
with b:
    print("prueba de herramientas no implementadas:")
    for nombre, entrada in (("take_screenshot", {}),
                            ("navigate", {"url": "http://localhost:1/"}),
                            ("wait", {"duration": 2})):
        uso = BetaToolUseBlock(type="tool_use", id="toolu_x", name=nombre,
                               input=entrada, toolset_name="browser")
        r = b.tool_result(uso)
        print(f"\n{nombre} -> is_error={r.get('is_error')}")
        print("  ", r.get("content"))
