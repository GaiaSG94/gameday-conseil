"""Rend les écrans du produit (build local) en captures 1440x900 + mesures.

Usage: python tools/preview/capture-produit.py <dossier-sortie> [port]
Le serveur de prévisualisation doit tourner (tools/preview/server.ts).
"""
from __future__ import annotations

import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:{port}"
VIEWPORT = {"width": 1440, "height": 900}

# Sélecteurs importants par écran (présence + position dans la planche 740x640).
KEYS = {
    "jeu": [".meta", ".title", ".rule", ".tag", ".bub", ".motion", ".foot", ".cta"],
    "post": [".meta", ".title", ".rule", ".tag", ".dots", ".stk", ".cta"],
    "fin": [".meta", ".yn", ".score-stk", ".foot-stk", ".cta"],
    "series": [".meta", ".title", ".rule", ".yn", ".stk", ".srow"],
}

MESURES = """
() => {
  const out = {boxes: {}, errors: []};
  const board = document.querySelector('.board');
  if (board) {
    const r = board.getBoundingClientRect();
    out.board = {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
  }
  const names = [...document.querySelectorAll('*')].filter(e => e.className && typeof e.className === 'string');
  const wanted = %s;
  for (const sel of wanted) {
    const els = [...document.querySelectorAll(sel)];
    if (!els.length) { out.boxes[sel] = []; continue; }
    out.boxes[sel] = els.map(e => {
      const r = e.getBoundingClientRect();
      return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
    });
  }
  const canvas = document.querySelector('canvas');
  if (canvas) {
    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    out.webgl = !!gl;
    out.canvas = {w: canvas.width, h: canvas.height};
  }
  return out;
}
"""


def mesurer(page, cle: str) -> dict:
    return page.evaluate(MESURES % json.dumps(KEYS[cle]))


def wait_scene(page) -> None:
    page.wait_for_selector("#root > *", timeout=15000)
    page.wait_for_timeout(2500)


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "captures")
    port = sys.argv[2] if len(sys.argv) > 2 else "5177"
    out.mkdir(parents=True, exist_ok=True)
    base = BASE.format(port=port)
    rapport: dict = {}
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", args=["--use-gl=swiftshader"])
        ctx = nav.new_context(viewport=VIEWPORT, device_scale_factor=1)
        page = ctx.new_page()
        erreurs: list[str] = []
        page.on("console", lambda m: erreurs.append(m.text) if m.type == "error" else None)

        # --- reset : une semaine belie, pas de vote du jour
        page.request.post(base + "/api/reset")

        # --- Post (inline)
        page.goto(base + "/splash.html", wait_until="load")
        wait_scene(page)
        page.screenshot(path=str(out / "produit-02-post.png"))
        rapport["post"] = mesurer(page, "post")

        # --- Jeu
        page.goto(base + "/game.html", wait_until="load")
        wait_scene(page)
        page.screenshot(path=str(out / "produit-01-jeu.png"))
        rapport["jeu"] = mesurer(page, "jeu")

        # --- Carte de fin : on vote, la scene montre le resultat
        page.click(".motion >> nth=1")
        page.wait_for_timeout(700)
        page.click(".foot .cta")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(out / "produit-03-carte-de-fin.png"))
        rapport["fin"] = mesurer(page, "fin")

        # --- Series
        page.goto(base + "/series.html", wait_until="load")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(out / "produit-04-series.png"))
        rapport["series"] = mesurer(page, "series")

        rapport["erreurs_console"] = erreurs[:10]
        ctx.close()
        nav.close()
    (out / "produit-mesures.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    for cle, data in rapport.items():
        if cle == "erreurs_console":
            print(f"erreurs console : {data}")
        else:
            print(f"{cle} : board={data.get('board')} webgl={data.get('webgl')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
