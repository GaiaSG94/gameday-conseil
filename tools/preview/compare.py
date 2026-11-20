"""Compare planche (locked design) and product (local build), page by page.

For each page: the 740x640 board of both sides, a side-by-side contact sheet,
and the measured deltas (position, size) of the key elements.

Usage: python tools/preview/compare.py <dossier-sortie> [port]
"""
from __future__ import annotations

import json
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

APP = pathlib.Path(__file__).resolve().parents[2]
PLANCHES = APP / "G-DESIGN" / "planches" / "v4"

# (planche selector, index dans la planche, selecteur produit, index produit)
PAIRES = {
    "01-jeu": [
        (".q .meta", 0, ".meta", 0),
        (".q h1", 0, ".title", 0),
        (".q .rule", 0, ".rule", 0),
        (".q .bub", 0, ".bub", 0),
        (".q .bub", 1, ".bub", 1),
        (".q .bub", 2, ".bub", 2),
        (".q .bub", 3, ".bub", 3),
        (".q .bub", 4, ".bub", 4),
        (".q .bub", 5, ".bub", 5),
        (".q .mo", 0, ".motion", 0),
        (".q .mo", 1, ".motion", 1),
        (".q .mo", 2, ".motion", 2),
        (".q .foot", 0, ".foot", 0),
        (".q .tag", 0, ".tag", 0),
    ],
    "02-post": [
        (".q .meta", 0, ".meta", 0),
        (".q h1", 0, ".title", 0),
        (".q .rule", 0, ".rule", 0),
        (".q .dots", 0, ".dots", 0),
        (".q .dots", 1, ".dots", 1),
        (".q .dots", 2, ".dots", 2),
        (".q .dots", 3, ".dots", 3),
        (".q .dots", 4, ".dots", 4),
        (".q .dots", 5, ".dots", 5),
        (".q .stk", 0, ".post-stk", 0),
        (".q .cta", 0, ".cta", 0),
        (".q .tag", 0, ".tag", 0),
    ],
    "03-carte-de-fin": [
        (".q .meta", 0, ".meta", 0),
        (".q .yn", 0, ".yn", 0),
        (".q .yn", 1, ".yn", 1),
        (".q .yn", 2, ".yn", 2),
        (".q .yn", 3, ".yn", 3),
        (".q .yn", 4, ".yn", 4),
        (".q .yn", 5, ".yn", 5),
        (".q .stk", 0, ".score-stk", 0),
        (".q .stk", 1, ".foot-stk", 0),
        (".q .cta", 0, ".cta", 0),
    ],
    "04-series": [
        (".q .meta", 0, ".meta", 0),
        (".q h1", 0, ".title", 0),
        (".q .rule", 0, ".rule", 0),
        (".q .yn", 0, ".yn", 0),
        (".q .yn", 1, ".yn", 1),
        (".q .yn", 2, ".yn", 2),
        (".q .yn", 3, ".yn", 3),
        (".q .yn", 4, ".yn", 4),
        (".q .yn", 5, ".yn", 5),
        (".q .stk", 0, ".streak-stk", 0),
        (".q .stk", 1, ".days-stk", 0),
    ],
}

FICHIERS = {
    "01-jeu": "01-quartier-3d.html",
    "02-post": "02-post.html",
    "03-carte-de-fin": "03-carte-de-fin.html",
    "04-series": "04-series.html",
}

URLS = {
    "01-jeu": "/game.html",
    "02-post": "/splash.html",
    "03-carte-de-fin": "/game.html",
    "04-series": "/series.html",
}


def board_box(page) -> dict:
    for sel in (".q", ".board"):
        if page.locator(sel).count():
            box = page.locator(sel).first.bounding_box()
            if box:
                return {k: round(v) for k, v in box.items()}
    return {"x": 0, "y": 0, "width": 740, "height": 640}


def shot_board(page, path: pathlib.Path, box: dict) -> None:
    page.screenshot(
        path=str(path),
        clip={
            "x": box["x"],
            "y": box["y"],
            "width": box["width"],
            "height": box["height"],
        },
    )


def compose(planche: pathlib.Path, produit: pathlib.Path, cible: pathlib.Path) -> None:
    a = Image.open(planche)
    b = Image.open(produit)
    hauteur = max(a.height, b.height)
    toile = Image.new("RGB", (a.width + b.width + 24, hauteur), (245, 243, 238))
    toile.paste(a, (0, 0))
    toile.paste(b, (a.width + 24, 0))
    toile.save(cible)


def mesure(page, sel: str, index: int, origine: dict) -> dict | None:
    loc = page.locator(sel)
    if loc.count() <= index:
        return None
    box = loc.nth(index).bounding_box()
    if not box:
        return None
    return {
        "x": round(box["x"] - origine["x"]),
        "y": round(box["y"] - origine["y"]),
        "w": round(box["width"]),
        "h": round(box["height"]),
    }


def rendre_planche(nav, slug: str, out: pathlib.Path) -> tuple[dict, dict]:
    ctx = nav.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    page.goto(
        "file:///" + str(PLANCHES / FICHIERS[slug]).replace("\\", "/"),
        wait_until="load",
    )
    page.wait_for_function(
        "document.documentElement.dataset.ready === '1'", timeout=20000
    )
    page.wait_for_timeout(1200)
    box = board_box(page)
    shot_board(page, out / f"{slug}-planche.png", box)
    mesures = {f"{sel}#{i}": mesure(page, sel, i, box) for sel, i, _, _ in PAIRES[slug]}
    ctx.close()
    return box, mesures


def rendre_produit(nav, slug: str, out: pathlib.Path, base: str) -> tuple[dict, dict]:
    ctx = nav.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    page.request.post(base + "/api/reset")
    page.goto(base + URLS[slug], wait_until="load")
    page.wait_for_selector("#root > *", timeout=15000)
    page.wait_for_timeout(2500)
    if slug == "03-carte-de-fin":
        page.click(".motion >> nth=1")
        page.wait_for_timeout(600)
        page.click(".foot .cta")
        page.wait_for_timeout(2200)
    box = board_box(page)
    shot_board(page, out / f"{slug}-produit.png", box)
    mesures = {f"{sel}#{i}": mesure(page, sel, i, box) for _, _, sel, i in PAIRES[slug]}
    ctx.close()
    return box, mesures


def comparer(paires, mesure_p: dict, mesure_q: dict) -> list:
    lignes = []
    for sel_p, i_p, sel_q, i_q in paires:
        item_p = mesure_p[f"{sel_p}#{i_p}"]
        item_q = mesure_q[f"{sel_q}#{i_q}"]
        ligne = {
            "planche_sel": sel_p,
            "produit_sel": sel_q,
            "planche": item_p,
            "produit": item_q,
        }
        if item_p and item_q:
            ligne["delta"] = {
                "dx": item_q["x"] - item_p["x"],
                "dy": item_q["y"] - item_p["y"],
                "dw": item_q["w"] - item_p["w"],
                "dh": item_q["h"] - item_p["h"],
            }
        lignes.append(ligne)
    return lignes


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "captures")
    port = sys.argv[2] if len(sys.argv) > 2 else "5177"
    out.mkdir(parents=True, exist_ok=True)
    base = f"http://127.0.0.1:{port}"
    rapport: dict = {}
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", args=["--use-gl=swiftshader"])
        for slug in PAIRES:
            box_p, mesure_p = rendre_planche(nav, slug, out)
            box_q, mesure_q = rendre_produit(nav, slug, out, base)
            compose(
                out / f"{slug}-planche.png",
                out / f"{slug}-produit.png",
                out / f"{slug}-cote-a-cote.png",
            )
            rapport[slug] = {
                "paires": comparer(PAIRES[slug], mesure_p, mesure_q),
                "board": {"planche": box_p, "produit": box_q},
            }
        nav.close()
    (out / "ecarts.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    for slug, data in rapport.items():
        print(f"\n== {slug} ==")
        for ligne in data["paires"]:
            p = ligne["planche"]
            q = ligne["produit"]
            d = ligne.get("delta")
            if p is None or q is None:
                print(f"  {ligne['planche_sel']} / {ligne['produit_sel']} : ABSENT ({p} / {q})")
                continue
            print(
                f"  {ligne['planche_sel']:<12} planche x={p['x']:>4} y={p['y']:>4} "
                f"w={p['w']:>4} h={p['h']:>3}  |  produit x={q['x']:>4} y={q['y']:>4} "
                f"w={q['w']:>4} h={q['h']:>3}  |  dx={d['dx']:>4} dy={d['dy']:>4} "
                f"dw={d['dw']:>4} dh={d['dh']:>4}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
