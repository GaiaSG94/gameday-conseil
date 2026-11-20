"""Rend les planches G-DESIGN v4 en captures 1440x900 (preuve de reference).

Usage: python tools/preview/capture-planches.py <dossier-sortie>
Le HTML est autonome (fonts + three.js en base64) : rendu en file://.
"""
from __future__ import annotations

import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLANCHES = ROOT / "G-DESIGN" / "planches" / "v4"
PAGES = [
    ("01-quartier-3d.html", "planche-01-jeu"),
    ("02-post.html", "planche-02-post"),
    ("03-carte-de-fin.html", "planche-03-carte-de-fin"),
    ("04-series.html", "planche-04-series"),
]


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "captures")
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", args=["--use-gl=swiftshader"])
        for nom, slug in PAGES:
            src = PLANCHES / nom
            url = "file:///" + str(src).replace("\\", "/")
            ctx = nav.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            page = ctx.new_page()
            erreurs: list[str] = []
            page.on("console", lambda m: erreurs.append(m.text) if m.type == "error" else None)
            page.goto(url, wait_until="load")
            page.wait_for_function("document.documentElement.dataset.ready === '1'", timeout=20000)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(out / f"{slug}.png"))
            print(f"{slug}.png  erreurs={erreurs[:3]}")
            ctx.close()
        nav.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
