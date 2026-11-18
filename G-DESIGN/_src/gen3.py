"""Conseil — V3 planches (page Jeu, desktop only), built on the game refs.

One cast of six drawn neighbors shared by the three directions; each direction
changes the world and the rendering, not the cast.
Usage: python3 G-DESIGN/_src/gen3.py G-DESIGN/planches/v3
"""
import math, pathlib, sys

SRC = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
F = {k: (SRC / f"fonts/{k}.b64").read_text() for k in ("archivo", "dmmono-400", "dmmono-500")}

# id, name, role, quote, accessory
CAST = [
    ("ines", "Ines", "bakery, no. 4", "Keep a lane clear for my 6 a.m. deliveries.", "toque"),
    ("theo", "Theo", "dad of three", "The kids need a place that isn't a car park.", "kid"),
    ("ruth", "Ruth", "here since 1984", "Quiet after dark. Last summer was too much.", "cane"),
    ("sam", "Sam", "bike courier", "Somewhere to lock a bike that isn't a lamppost.", "helmet"),
    ("odile", "Odile", "garden waitlist", "Two years waiting for a plot. Two.", "can"),
    ("kofi", "Kofi", "owns no. 12", "Fine by me, as long as owners pay nothing.", "cap"),
]
MOTIONS = [("A", "Community garden", "Plots for the waitlist, gate locked at 9 pm."),
           ("B", "Play court & racks", "Paved court, bike racks, lit till 11 pm."),
           ("C", "Shared lot", "Beds, a play corner, racks. Small owner levy.")]
SESSION, DATE, STREAK, SAT, SEL = 47, "Wed 18 Nov", 6, "1,284", "B"


# =================================================================== the cast
def peg(acc, x, y, s=1.0, fill="#fff", head="#fff", ink="#161616", sw=1.7, flip=False, eyes=True, shade=None):
    """A neighbor: rounded body, round head, one accessory that says who they are.
    Local coords: feet on (0,0), ~44 units tall."""
    w = sw / s
    st = f'stroke="{ink}" stroke-width="{w:.2f}" stroke-linejoin="round" stroke-linecap="round"' if ink else 'stroke="none"'
    body = "M-8.5 0V-15.5Q-8.5 -24 0 -24Q8.5 -24 8.5 -15.5V0Z"
    parts = []
    back, front = [], []
    if acc == "kid":
        back.append(f'<g transform="translate(14 0) scale(.62)"><path d="{body}" fill="{fill}" {st.replace(f"{w:.2f}", f"{w / .62:.2f}")}/>'
                    f'<circle cy="-31" r="7" fill="{head}" {st.replace(f"{w:.2f}", f"{w / .62:.2f}")}/>'
                    + (f'<circle cx="-2.3" cy="-31.5" r="1.1" fill="{ink or "#161616"}"/><circle cx="2.3" cy="-31.5" r="1.1" fill="{ink or "#161616"}"/>' if eyes else "")
                    + '</g>')
    if acc == "cane":
        front.append(f'<path d="M11 0L12.5 -17Q12.8 -21 9.5 -21" fill="none" {st if ink else f"stroke=\"#6b4a2b\" stroke-width=\"{1.8 / s:.2f}\" stroke-linecap=\"round\""}/>')
        back.append(f'<circle cy="-39.5" r="3.6" fill="{head if not ink else "#fff"}" {st}/>')
    if acc == "can":
        front.append(f'<g transform="translate(9 -9)"><path d="M0 0H7V7H0Z" fill="{fill}" {st}/><path d="M7 1.5L12 -3" fill="none" {st}/><path d="M1 0Q3.5 -5 6 0" fill="none" {st}/></g>')
    if acc == "helmet":
        front.append(f'<path d="M-8.5 -14L7 -22" fill="none" {st}/><rect x="4" y="-13" width="7" height="8" rx="1.2" fill="{fill}" {st}/>')
    parts += back
    parts.append(f'<path d="{body}" fill="{fill}" {st}/>')
    if shade:
        parts.append(f'<path d="M2 0V-23.6Q8.5 -22.5 8.5 -15.5V0Z" fill="{shade}" opacity=".22"/>')
    parts.append(f'<circle cy="-31" r="7" fill="{head}" {st}/>')
    if shade:
        parts.append(f'<path d="M1.5 -37.8A7 7 0 0 1 1.5 -24.2A9 9 0 0 0 1.5 -37.8Z" fill="{shade}" opacity=".22"/>')
    if eyes:
        e = ink or "#161616"
        parts.append(f'<circle cx="-2.4" cy="-31.5" r="1.05" fill="{e}"/><circle cx="2.4" cy="-31.5" r="1.05" fill="{e}"/>')
    if acc == "toque":
        parts.append(f'<path d="M-5.8 -36.5Q-10.5 -42 -5 -44.5Q-3 -50 2 -47.5Q7 -50 8 -45Q11.5 -41 5.8 -36.5Z" fill="#fff" {st}/>'
                     f'<path d="M-5.8 -36.5H5.8" fill="none" {st}/>')
    if acc == "helmet":
        parts.append(f'<path d="M-8 -33Q-8 -41.5 0 -41.5Q8 -41.5 8 -33Z" fill="{fill}" {st}/><path d="M-3 -41L-1 -36M3 -41L2 -36" fill="none" {st}/>')
    if acc == "cap":
        parts.append(f'<path d="M-7.2 -34.5Q-6.5 -40.5 0 -40.5Q6.5 -40.5 7.2 -34.5Z" fill="{fill}" {st}/><path d="M6 -35H12.5" fill="none" {st}/>')
    parts += front
    tf = f"translate({x:.1f} {y:.1f}) scale({-s if flip else s} {s})"
    return f'<g transform="{tf}">{"".join(parts)}</g>'


def shadow(x, y, rx=13, ry=3.4, c="#161616", o=.12):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{o}"/>'


# =================================================================== shell
BASE = """
@font-face{font-family:"Archivo";src:url(data:font/woff2;base64,__ARCHIVO__) format("woff2");font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:"DM Mono";src:url(data:font/woff2;base64,__DM4__) format("woff2");font-weight:400}
@font-face{font-family:"DM Mono";src:url(data:font/woff2;base64,__DM5__) format("woff2");font-weight:500}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#cfccc5;font-family:"Archivo",sans-serif;color:#161616}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
input[type=radio]{position:absolute;opacity:0;pointer-events:none}
.sheet{width:1440px;transform-origin:0 0}
.screen{width:1440px;height:900px;background:#f4f4f2;position:relative;overflow:hidden}
.gbar{background:#dcdcd8;border-radius:6px;display:block;height:10px}
.d-top{height:56px;background:#fff;border-bottom:1px solid #e2e2df;display:flex;align-items:center;padding:0 20px;gap:16px}
.d-top .mark{width:30px;height:30px;border-radius:8px;background:#d4d4d0}
.d-top .search{margin-left:180px;width:560px;height:38px;border-radius:19px;background:#efefec}
.d-top .dots{margin-left:auto;display:flex;gap:10px}.d-top .dots i{width:30px;height:30px;border-radius:50%;background:#e4e4e1;display:block}
.d-rail{position:absolute;left:0;top:56px;bottom:0;width:240px;border-right:1px solid #e2e2df;padding:24px 20px;display:flex;flex-direction:column;gap:18px}
.d-side{position:absolute;left:1092px;top:80px;width:310px;height:300px;border-radius:12px;background:#fff;border:1px solid #e6e6e3;padding:18px;display:flex;flex-direction:column;gap:12px}
.d-post{position:absolute;left:300px;top:70px;width:760px;background:#fff;border:1px solid #e6e6e3;border-radius:14px;padding:12px 10px 4px}
.ph{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#64625d;padding:0 8px}
.ph .av{width:24px;height:24px;border-radius:50%;background:#cfcfcb}
.ph b{color:#1d1d1b;font-weight:600}
.pt{font-size:18px;font-weight:600;line-height:1.25;padding:5px 8px 9px;color:#1d1d1b}
.pa{display:flex;gap:8px;padding:7px 6px 4px}
.pa span{height:30px;border-radius:15px;background:#f1f1ee;display:flex;align-items:center;gap:8px;padding:0 14px;font-size:12.5px;font-weight:600;color:#4a4844}
.game{width:740px;height:640px;border-radius:8px;overflow:hidden;position:relative}
.kit{background:#f7f6f2;padding:46px 56px 60px;display:grid;grid-template-columns:330px 1fr;gap:28px 56px;border-top:1px solid #d9d6cf}
.kit .k{font:500 11px/1.3 "DM Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:#7a766d}
.kit h2{font-weight:900;font-stretch:100%;font-size:46px;line-height:.95;letter-spacing:-.02em;margin-top:8px}
.kit .why{font-size:14.5px;line-height:1.55;color:#34322e;margin-top:16px;max-width:330px}
.kit .why b{font-weight:650}
.kit .cols{display:grid;grid-template-columns:1.25fr 1fr 1fr 1fr;gap:26px}
.kit .cell .k{margin-bottom:12px}
.kit .note{font-size:12.5px;line-height:1.45;color:#4a4740;margin-top:10px}
.sw{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.sw i{width:42px;height:42px;border-radius:3px;display:block;flex:none;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.sw b{display:block;font-size:13px;font-weight:650}
.sw span{font:400 11px/1.3 "DM Mono",monospace;color:#6b675f}
.castrow{display:flex;gap:4px;align-items:flex-end}
.castrow figure{text-align:center;font:500 10px/1.2 "DM Mono",monospace;color:#4a4740;text-transform:uppercase;letter-spacing:.04em}
"""
UP = '<svg width="14" height="14" viewBox="0 0 14 14"><path d="M7 2 2.5 7.5H5.5V12h3V7.5h3z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'


def chrome(game):
    rail = "".join(f'<span class="gbar" style="width:{w}px"></span>' for w in (120, 96, 140, 80, 130, 110, 90))
    side = "".join(f'<span class="gbar" style="width:{w}px"></span>' for w in (150, 260, 240, 200, 120, 230))
    return f'''<div class="screen">
<div class="d-top"><span class="mark"></span><span class="gbar" style="width:70px"></span><span class="search"></span><span class="dots"><i></i><i></i><i></i></span></div>
<div class="d-rail">{rail}</div>
<div class="d-post"><div class="ph"><span class="av"></span><b>r/conseil_daily</b><span>· 3 h</span></div>
<div class="pt">Council session #{SESSION}: the empty lot on Alder Street</div>
<div class="game">{game}</div>
<div class="pa"><span>{UP} 214</span><span>38 comments</span><span>Share</span></div></div>
<div class="d-side">{side}</div></div>'''


def page(num, slug, title, css, game, kit):
    base = BASE.replace("__ARCHIVO__", F["archivo"]).replace("__DM4__", F["dmmono-400"]).replace("__DM5__", F["dmmono-500"])
    (OUT / f"{num}-{slug}.html").write_text(f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conseil · Jeu V3 · {num} {title}</title>
<style>{base}{css}</style></head>
<body><div class="sheet" id="sheet">{chrome(game)}{kit}</div>
<script>(function(){{var s=document.getElementById("sheet");function f(){{var k=Math.min(1,innerWidth/1440);s.style.transform="scale("+k+")";document.body.style.height=s.offsetHeight*k+"px"}}addEventListener("resize",f);f()}})();</script>
</body></html>''')


def kit(num, title, why, cells):
    cols = "".join(f'<div class="cell"><p class="k">{k}</p>{b}</div>' for k, b in cells)
    return f'''<section class="kit"><div><p class="k">Conseil · page Jeu · V3 · direction {num}/03</p><h2>{title}</h2><p class="why">{why}</p></div><div class="cols">{cols}</div></section>'''


def sw(c, n, h, r):
    return f'<div class="sw"><i style="background:{c}"></i><div><b>{n}</b><span>{h} · {r}</span></div></div>'


def cast_row(**kw):
    figs = "".join(f'<figure><svg width="58" height="78" viewBox="-29 -62 58 78">{shadow(0, 0, 12, 3)}{peg(acc, 0, 0, 1.25, **kw)}</svg><figcaption>{n}</figcaption></figure>'
                   for _, n, _, _, acc in CAST)
    return f'<div class="castrow">{figs}</div>'


# isometric helper
def iso(x, y, z=0, s=1.0, ox=0.0, oy=0.0):
    return (ox + (x - y) * 0.866 * s, oy + (x + y) * 0.5 * s - z * s)


def poly(pts):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)


# =================================================================== 01 FOULE (ink crowd)
INK, PAPER, OR = "#161616", "#f4f1e9", "#ef5b26"
GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' seed='3'/>"
         "<feColorMatrix values='0 0 0 0 .3 0 0 0 0 .28 0 0 0 0 .22 0 0 0 .13 0'/></filter><rect width='200' height='200' filter='url(%23n)'/></svg>")

CSS1 = f"""
.c1{{--ink:{INK};--paper:{PAPER};--or:{OR};width:100%;height:100%;position:relative;background:var(--paper);color:var(--ink)}}
.c1:before{{content:"";position:absolute;inset:0;background:url("{GRAIN}");mix-blend-mode:multiply;pointer-events:none;z-index:0}}
.c1>*{{position:relative;z-index:1}}
.c1 .meta{{position:absolute;left:26px;top:20px;right:26px;display:flex;justify-content:space-between;font:500 11px/1 "DM Mono",monospace;letter-spacing:.06em;text-transform:uppercase}}
.c1 .meta b{{font-weight:500;background:var(--ink);color:var(--paper);padding:3px 6px;border-radius:3px}}
.c1 h1{{position:absolute;left:0;right:0;top:36px;text-align:center;font-weight:900;font-stretch:108%;font-size:52px;line-height:.9;letter-spacing:-.035em;text-transform:uppercase}}
.c1 .rule{{position:absolute;left:0;right:0;top:88px;text-align:center;font-size:14.5px;font-weight:500}}
.c1 .rule b{{font-weight:800}}
.c1 svg.scene{{position:absolute;left:0;top:110px}}
.c1 .bub{{position:absolute;width:184px;background:#fff;border:1.8px solid var(--ink);border-radius:14px;padding:7px 11px 7px;font-size:13px;line-height:1.24;font-weight:520}}
.c1 .bub:after{{content:"";position:absolute;top:17px;width:12px;height:12px;background:#fff;border:1.8px solid var(--ink);border-top:0;border-left:0}}
.c1 .bub.l:after{{right:-7.5px;transform:rotate(-45deg)}} .c1 .bub.r:after{{left:-7.5px;transform:rotate(135deg)}}
.c1 .bub em{{display:block;font:500 9.5px/1 "DM Mono",monospace;font-style:normal;letter-spacing:.06em;text-transform:uppercase;opacity:.6;margin-top:4px}}
.c1 .ov{{opacity:0;transition:opacity .25s}}
.c1:has(#c1A:checked) .ovA,.c1:has(#c1B:checked) .ovB,.c1:has(#c1C:checked) .ovC{{opacity:1}}
.c1:has(input:checked) .ov0{{opacity:0}}
.c1 .mos{{position:absolute;left:26px;right:26px;bottom:76px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.c1 .mo{{display:block;cursor:pointer;background:#fff;border:2px solid var(--ink);border-radius:16px;padding:9px 14px 10px;box-shadow:4px 4px 0 var(--ink);transition:transform .12s,box-shadow .12s,background .12s;position:relative}}
.c1 .mo:hover{{transform:translate(-1px,-1px);box-shadow:5px 5px 0 var(--ink)}}
.c1 .mo b{{font-weight:900;font-stretch:100%;font-size:17px;letter-spacing:-.01em;display:flex;align-items:center;gap:8px}}
.c1 .mo b i{{font-style:normal;width:22px;height:22px;border-radius:50%;border:2px solid var(--ink);display:grid;place-items:center;font-size:12px}}
.c1 .mo span{{display:block;font-size:12.5px;line-height:1.3;margin-top:4px;font-weight:450}}
.c1 .mo:has(input:checked){{background:var(--or);transform:translate(2px,2px);box-shadow:2px 2px 0 var(--ink)}}
.c1 .mo:has(input:checked) b i{{background:var(--ink);color:var(--or)}}
.c1 .foot{{position:absolute;left:26px;right:26px;bottom:18px;display:flex;justify-content:space-between;align-items:center}}
.c1 .foot p{{font:500 11px/1.3 "DM Mono",monospace;letter-spacing:.05em;text-transform:uppercase}}
.c1 .cta{{height:44px;padding:0 26px;border-radius:22px;background:var(--ink);color:var(--paper);font-weight:850;font-size:15px;letter-spacing:.06em;text-transform:uppercase;box-shadow:4px 4px 0 var(--or)}}
"""


def lot_iso(ox, oy, s, W=10, D=6):
    return lambda x, y, z=0: iso(x, y, z, s, ox, oy)


def scene1():
    W, H = 740, 360
    P = lot_iso(370, 172, 15)
    L, D = 10, 6
    # lot shifted so its centre sits at the scene centre
    def p(x, y, z=0):
        return P(x - L / 2, y - D / 2, z)
    corners = [p(0, 0), p(L, 0), p(L, D), p(0, D)]
    out = [f'<polygon points="{poly(corners)}" fill="#e9e3d3" stroke="{INK}" stroke-width="1.8" stroke-dasharray="5 4" stroke-linejoin="round"/>']
    # weeds + a crate + a puddle: the lot today
    import random
    r = random.Random(5)
    for _ in range(22):
        x, y = r.uniform(.6, L - .6), r.uniform(.6, D - .6)
        a, b = p(x, y)
        out.append(f'<path class="ov ov0" style="opacity:1" d="M{a - 3:.1f} {b:.1f}l1.5 -6M{a:.1f} {b:.1f}l0 -8M{a + 3:.1f} {b:.1f}l-1.5 -5" stroke="{INK}" stroke-width="1.2" fill="none" stroke-linecap="round"/>')
    # overlays: what the chosen motion would put on the lot (orange)
    A = []
    for row in range(3):
        for col in range(5):
            a, b = p(1.2 + col * 1.9, 1.1 + row * 1.9)
            A.append(f'<ellipse cx="{a:.1f}" cy="{b:.1f}" rx="11" ry="6" fill="{OR}" stroke="{INK}" stroke-width="1.4"/>'
                     f'<path d="M{a:.1f} {b - 3:.1f}q-3 -7 -7 -8M{a:.1f} {b - 3:.1f}q3 -8 8 -8" stroke="{INK}" stroke-width="1.3" fill="none" stroke-linecap="round"/>')
    B = [f'<polygon points="{poly([p(1, .8), p(7.4, .8), p(7.4, 5.2), p(1, 5.2)])}" fill="{OR}" stroke="{INK}" stroke-width="1.6"/>',
         f'<polyline points="{poly([p(4.2, .8), p(4.2, 5.2)])}" stroke="{INK}" stroke-width="1.4" fill="none"/>']
    a, b = p(4.2, 3)
    B.append(f'<ellipse cx="{a:.1f}" cy="{b:.1f}" rx="13" ry="7.5" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    for i in range(5):
        a, b = p(8.6, .8 + i * 1.05)
        B.append(f'<path d="M{a - 4:.1f} {b:.1f}v-9a4 4 0 0 1 8 0v9" stroke="{INK}" stroke-width="1.6" fill="none"/>')
    C = []
    for row in range(3):
        for col in range(2):
            a, b = p(1.1 + col * 1.9, 1.1 + row * 1.9)
            C.append(f'<ellipse cx="{a:.1f}" cy="{b:.1f}" rx="10" ry="5.5" fill="{OR}" stroke="{INK}" stroke-width="1.4"/>')
    C.append(f'<polygon points="{poly([p(4.6, .8), p(7.6, .8), p(7.6, 5.2), p(4.6, 5.2)])}" fill="{OR}" stroke="{INK}" stroke-width="1.6"/>')
    for i in range(4):
        a, b = p(8.8, 1 + i * 1.2)
        C.append(f'<path d="M{a - 4:.1f} {b:.1f}v-9a4 4 0 0 1 8 0v9" stroke="{INK}" stroke-width="1.6" fill="none"/>')
    out.append(f'<g class="ov ovA">{"".join(A)}</g><g class="ov ovB">{"".join(B)}</g><g class="ov ovC">{"".join(C)}</g>')
    # neighbors around the lot, three each side
    spots = [(240, 118, False), (222, 228, False), (240, 338, False), (500, 118, True), (518, 228, True), (500, 338, True)]
    for (cid, n, role, q, acc), (x, y, fl) in zip(CAST, spots):
        out.append(shadow(x, y, 15, 3.8))
        out.append(peg(acc, x, y, 1.45, flip=fl))
    # a few passers-by, the rest of the neighborhood (smaller, faded)
    for x, y, acc in [(318, 338, ""), (420, 344, "cap"), (40, 352, ""), (704, 356, "")]:
        out.append(f'<g opacity=".38">{shadow(x, y, 9, 2.4)}{peg(acc, x, y, .85)}</g>')
    # hand arrow: where to look (Gapsy, used once)
    out.append(f'<text x="300" y="94" font-family="DM Mono" font-size="11" letter-spacing=".6" fill="{INK}">THE LOT, TODAY</text>'
               f'<path d="M402 90q24 -2 20 22" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round"/><path d="M416 104l6 9 6 -9" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return f'<svg class="scene" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(out)}</svg>', spots


def game1():
    svg, spots = scene1()
    bubs = ""
    for (cid, n, role, q, acc), (x, y, fl) in zip(CAST, spots):
        top = 110 + y - 45 - 24
        if not fl:
            left = x - 22 - 184
            bubs += f'<p class="bub l" style="left:{max(12, left)}px;top:{top}px">{q}<em>{n} · {role}</em></p>'
        else:
            left = x + 22
            bubs += f'<p class="bub r" style="left:{min(740 - 196, left)}px;top:{top}px">{q}<em>{n} · {role}</em></p>'
    mos = "".join(f'<label class="mo"><input type="radio" id="c1{l}" name="c1"{" checked" if l == SEL else ""}><b><i>{l}</i>{t}</b><span>{d}</span></label>' for l, t, d in MOTIONS)
    return f'''<div class="c1">
<div class="meta"><span>Session {SESSION} · {DATE}</span><span><b>{STREAK}-day streak</b></span></div>
<h1>The empty lot</h1>
<p class="rule">Six neighbors, one lot. <b>Pick the motion most of them will back.</b></p>
{svg}{bubs}
<div class="mos">{mos}</div>
<div class="foot"><p>{SAT} neighbors have voted today</p><button class="cta">Call the vote</button></div></div>'''


def kit1():
    tile = (f'<svg width="100%" height="150" viewBox="0 0 300 150" style="background:{PAPER};border-radius:3px">'
            f'{shadow(70, 112, 16, 4)}{peg("toque", 70, 112, 1.7)}'
            f'<g transform="translate(130 30)"><rect width="140" height="50" rx="12" fill="#fff" stroke="{INK}" stroke-width="1.8"/>'
            f'<text x="12" y="22" font-family="Archivo" font-weight="520" font-size="13">Keep a lane clear</text><text x="12" y="38" font-family="Archivo" font-weight="520" font-size="13">for my deliveries.</text></g></svg>')
    return kit("01", "Foule",
               "Inspirée de <b>Don't Look Up</b> et de <b>Gapsy</b>. Le quartier est une foule de petits personnages au trait. Les six voisins du jour se tiennent "
               "autour du terrain et <b>parlent dans des bulles</b>, et le reste du quartier passe en gris. Choisir une motion la <b>dessine sur le terrain</b> "
               "en orange : on voit ce qu'on propose avant de passer au vote.",
               [("Le casting (commun aux 3 directions)", cast_row() + '<p class="note">Six voisins, chacun reconnaissable à un seul détail : toque, enfant, canne et chignon, casque et sacoche, arrosoir, casquette. Mêmes proportions, mêmes deux points pour les yeux.</p>'),
                ("Couleur", sw(PAPER, "Papier", PAPER, "fond, grain léger") + sw(INK, "Encre", INK, "trait, texte, ombres pleines") + sw(OR, "Orange chantier", OR, "la motion, rien d'autre") + '<p class="note">Une scène en noir et blanc : l’orange n’apparaît que sur ce que le joueur propose.</p>'),
                ("Typo", '<p style="font-weight:900;font-stretch:108%;font-size:40px;line-height:.9;letter-spacing:-.035em;text-transform:uppercase">The empty lot</p><p style="font-size:13px;font-weight:520;margin-top:10px">Keep a lane clear for my 6 a.m. deliveries.</p><p class="note">Archivo 900, largeur 108 %, approche serrée pour le titre ; Archivo 520 dans les bulles ; DM Mono pour les étiquettes.</p>'),
                ("Motifs", tile + '<p class="note">Bulle à contour plein, ombre pleine décalée sur les boutons, flèche au trait (une seule par écran), terrain en pointillé tant que rien n’est choisi.</p>')])


# =================================================================== 02 MAQUETTE (diorama, wooden figurines)
SAND, SAND2, WOODH, NAVY, OR2 = "#efe4cf", "#e3d3b4", "#e8c99a", "#1f3a5f", "#e5672e"
PAINT = {"ines": "#c9553a", "theo": "#3d6b8e", "ruth": "#8a6aa0", "sam": "#2f7a5f", "odile": "#c99a2e", "kofi": "#5b5f66"}

CSS2 = f"""
.c2{{--sand:{SAND};--navy:{NAVY};--or:{OR2};width:100%;height:100%;position:relative;background:var(--sand);color:var(--navy);overflow:hidden}}
.c2 .light{{position:absolute;left:-120px;top:-180px;width:640px;height:640px;border-radius:50%;background:#fff;opacity:.35;filter:blur(70px)}}
.c2 .meta{{position:absolute;left:26px;top:20px;font:500 11px/1 "DM Mono",monospace;letter-spacing:.06em;text-transform:uppercase}}
.c2 h1{{position:absolute;left:26px;top:38px;font-weight:900;font-stretch:72%;font-size:50px;line-height:.86;letter-spacing:-.015em;text-transform:uppercase}}
.c2 .rule{{position:absolute;left:26px;top:186px;width:200px;font-size:14.5px;line-height:1.3;font-weight:500}}
.c2 .rule b{{font-weight:800}}
.c2 .streak{{position:absolute;left:26px;top:270px;display:flex;align-items:center;gap:10px;font:500 11px/1.2 "DM Mono",monospace;letter-spacing:.05em;text-transform:uppercase}}
.c2 .streak i{{display:block;width:11px;height:11px;border-radius:50%;background:var(--navy)}}
.c2 .streak i.o{{background:none;border:1.5px dashed var(--navy)}}
.c2 svg.dio{{position:absolute;left:176px;top:-6px}}
.c2 .ov{{opacity:0;transform:translateY(-14px);transition:opacity .2s,transform .35s cubic-bezier(.3,1.5,.5,1)}}
.c2:has(#c2A:checked) .ovA,.c2:has(#c2B:checked) .ovB,.c2:has(#c2C:checked) .ovC{{opacity:1;transform:none}}
.c2 .shelf{{position:absolute;left:0;right:0;bottom:0;height:238px;background:{SAND2};border-top:2px solid rgba(31,58,95,.18)}}
.c2 .says{{position:absolute;left:22px;right:22px;top:14px;display:grid;grid-template-columns:repeat(6,1fr);gap:10px}}
.c2 .say{{font-size:12.2px;line-height:1.25;font-weight:520}}
.c2 .say svg{{display:block;margin:0 auto 2px}}
.c2 .say b{{display:block;font:500 9.5px/1 "DM Mono",monospace;letter-spacing:.06em;text-transform:uppercase;margin-bottom:3px}}
.c2 .pieces{{position:absolute;left:22px;right:22px;bottom:16px;display:grid;grid-template-columns:1fr 1fr 1fr 170px;gap:10px;align-items:stretch}}
.c2 .pc{{background:var(--sand);border-radius:10px;padding:7px 10px 7px 64px;cursor:pointer;position:relative;min-height:56px;border:2px solid transparent;transition:border-color .12s,background .12s}}
.c2 .pc svg{{position:absolute;left:6px;top:50%;margin-top:-22px}}
.c2 .pc b{{display:block;font-weight:850;font-stretch:80%;font-size:15px;text-transform:uppercase;line-height:1.05}}
.c2 .pc span{{display:block;font-size:11.5px;line-height:1.25;margin-top:2px;font-weight:450}}
.c2 .pc:hover{{border-color:rgba(31,58,95,.35)}}
.c2 .pc:has(input:checked){{border-color:var(--navy);background:#fff}}
.c2 .cta{{border-radius:10px;background:var(--or);color:#fff;font-weight:900;font-stretch:80%;font-size:18px;text-transform:uppercase;letter-spacing:.02em;line-height:1.05;padding:0 12px;box-shadow:0 3px 0 #a9461b}}
.c2 .cta small{{display:block;font:500 9.5px/1.2 "DM Mono",monospace;letter-spacing:.04em;text-transform:none;opacity:.9;margin-top:3px}}
"""


def box(ox, oy, s, x, y, w, d, h, top, left, right, ink=None):
    P = lambda a, b, c=0: iso(a, b, c, s, ox, oy)
    st = f' stroke="{ink}" stroke-width=".8"' if ink else ""
    return (f'<polygon points="{poly([P(x, y + d, 0), P(x + w, y + d, 0), P(x + w, y + d, h), P(x, y + d, h)])}" fill="{left}"{st}/>'
            f'<polygon points="{poly([P(x + w, y, 0), P(x + w, y + d, 0), P(x + w, y + d, h), P(x + w, y, h)])}" fill="{right}"{st}/>'
            f'<polygon points="{poly([P(x, y, h), P(x + w, y, h), P(x + w, y + d, h), P(x, y + d, h)])}" fill="{top}"{st}/>')


def roof(ox, oy, s, x, y, w, d, h, rh, c1, c2):
    P = lambda a, b, c=0: iso(a, b, c, s, ox, oy)
    return (f'<polygon points="{poly([P(x, y + d, h), P(x + w, y + d, h), P(x + w, y + d / 2, h + rh), P(x, y + d / 2, h + rh)])}" fill="{c1}"/>'
            f'<polygon points="{poly([P(x + w, y, h), P(x + w, y + d, h), P(x + w, y + d / 2, h + rh)])}" fill="{c2}"/>')


def diorama():
    W, H = 590, 402
    ox, oy, s = 268, 112, 21
    P = lambda a, b, c=0: iso(a, b, c, s, ox, oy)
    o = []
    # the block: soil sides + pavement top
    o.append(box(ox, oy, s, 0, 0, 12, 9, -1.4, "#d9cdb6", "#9b7a55", "#7f6245"))
    o.append(f'<polygon points="{poly([P(0, 0, 0), P(12, 0, 0), P(12, 9, 0), P(0, 9, 0)])}" fill="#d6cbb5"/>')
    # street along the front edge
    o.append(f'<polygon points="{poly([P(0, 7.4), P(12, 7.4), P(12, 9), P(0, 9)])}" fill="#b9b2a4"/>')
    for i in range(6):
        o.append(f'<polygon points="{poly([P(.6 + i * 2, 8.15), P(1.6 + i * 2, 8.15), P(1.6 + i * 2, 8.3), P(.6 + i * 2, 8.3)])}" fill="#f2ede2"/>')
    # houses at the back (left wall row), bakery with an awning
    o.append(box(ox, oy, s, 0, 0, 3, 2.4, 3.2, "#efe7d6", "#e4d6bb", "#cdb894") + roof(ox, oy, s, 0, 0, 3, 2.4, 3.2, 1.2, "#b5523b", "#8f3f2d"))
    o.append(box(ox, oy, s, 3.2, 0, 2.6, 2.4, 2.6, "#efe7d6", "#dfe4e6", "#c2cbcf") + roof(ox, oy, s, 3.2, 0, 2.6, 2.4, 2.6, 1, "#5b6b7a", "#45525e"))
    o.append(box(ox, oy, s, 9, 0, 3, 2.4, 3.6, "#efe7d6", "#eadcc0", "#d4bf98") + roof(ox, oy, s, 9, 0, 3, 2.4, 3.6, 1.1, "#6d5a49", "#56463a"))
    # bakery awning stripes
    for i in range(5):
        a = P(.2 + i * .55, 2.4, 1.8); b = P(.2 + i * .55 + .5, 2.4, 1.8); c = P(.2 + i * .55 + .5, 2.9, 1.5); d = P(.2 + i * .55, 2.9, 1.5)
        o.append(f'<polygon points="{poly([a, b, c, d])}" fill="{"#c9553a" if i % 2 == 0 else "#f6efe2"}"/>')
    # windows
    for (x0, y0, h0) in [(3.6, 2.4, 1.4), (4.6, 2.4, 1.4), (9.5, 2.4, 2.2), (10.6, 2.4, 2.2)]:
        o.append(f'<polygon points="{poly([P(x0, y0, h0), P(x0 + .6, y0, h0), P(x0 + .6, y0, h0 + .8), P(x0, y0, h0 + .8)])}" fill="#3d4b5a" opacity=".75"/>')
    # the lot: fenced, dashed, empty — the slot where a motion lands
    lx, ly, lw, ld = 3.2, 2.9, 5.6, 4.0
    o.append(f'<polygon points="{poly([P(lx, ly), P(lx + lw, ly), P(lx + lw, ly + ld), P(lx, ly + ld)])}" fill="#cbbf9f" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    for t in range(9):
        a = P(lx + .3 + t * .62, ly + ld)
        o.append(f'<path d="M{a[0]:.1f} {a[1]:.1f}v-10" stroke="#8d8a82" stroke-width="1.4"/>')
    # model pieces that drop on the lot
    gx = []
    for r in range(3):
        for c in range(3):
            gx.append(box(ox, oy, s, lx + .4 + c * 1.8, ly + .35 + r * 1.25, 1.4, .9, .45, "#6f8f45", "#7a5a3c", "#654a31"))
            a = P(lx + 1.1 + c * 1.8, ly + .8 + r * 1.25, .45)
            gx.append(f'<circle cx="{a[0]:.1f}" cy="{a[1] - 3:.1f}" r="4" fill="#8fb35a"/>')
    a1 = P(lx + lw - .3, ly + .3, 0)
    court = [box(ox, oy, s, lx + .3, ly + .3, 3.8, ld - .6, .15, OR2, "#a9461b", "#933b16"),
             f'<polyline points="{poly([P(lx + 2.2, ly + .3, .15), P(lx + 2.2, ly + ld - .3, .15)])}" stroke="#fff" stroke-width="1.6" fill="none"/>',
             f'<polygon points="{poly([P(lx + .6, ly + .6, .15), P(lx + 3.8, ly + .6, .15), P(lx + 3.8, ly + ld - .6, .15), P(lx + .6, ly + ld - .6, .15)])}" fill="none" stroke="#fff" stroke-width="1.3"/>']
    for i in range(4):
        a = P(lx + 4.7, ly + .5 + i * .9, 0)
        court.append(f'<path d="M{a[0] - 4:.1f} {a[1]:.1f}v-9a4 4 0 0 1 8 0v9" stroke="{NAVY}" stroke-width="2" fill="none"/>')
    mix = [box(ox, oy, s, lx + 3, ly + .3, 2.3, ld - .6, .15, OR2, "#a9461b", "#933b16")]
    for r in range(3):
        mix.append(box(ox, oy, s, lx + .4, ly + .35 + r * 1.25, 1.1, .9, .45, "#6f8f45", "#7a5a3c", "#654a31"))
        mix.append(box(ox, oy, s, lx + 1.7, ly + .35 + r * 1.25, 1.1, .9, .45, "#6f8f45", "#7a5a3c", "#654a31"))
    o.append(f'<g class="ov ovA">{"".join(gx)}</g><g class="ov ovB">{"".join(court)}</g><g class="ov ovC">{"".join(mix)}</g>')
    # figurines around the lot (painted wood), back-to-front for overlap
    spots = [("ines", 1.6, 3.4), ("ruth", 1.2, 5.6), ("odile", 2.2, 7.0), ("sam", 10.0, 3.4), ("kofi", 10.6, 5.2), ("theo", 9.6, 6.9)]
    spots.sort(key=lambda t: t[1] + t[2])
    acc = {c[0]: c[4] for c in CAST}
    for cid, x, y in spots:
        a = P(x, y)
        o.append(shadow(a[0] + 4, a[1], 14, 3.6, "#3a2a1a", .25))
        o.append(peg(acc[cid], a[0], a[1], 1.45, fill=PAINT[cid], head=WOODH, ink=None, shade="#000", flip=x > 6))
    return f'<svg class="dio" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(o)}</svg>'


def piece_icon(l):
    ox, oy, s = 28, 18, 6
    if l == "A":
        g = box(ox, oy, s, 0, 0, 4, 3, .5, "#6f8f45", "#7a5a3c", "#654a31") + f'<circle cx="28" cy="16" r="5" fill="#8fb35a"/>'
    elif l == "B":
        g = box(ox, oy, s, 0, 0, 4, 3, .3, OR2, "#a9461b", "#933b16") + f'<path d="M24 22h8" stroke="#fff" stroke-width="1.4"/>'
    else:
        g = box(ox, oy, s, 0, 0, 2, 3, .5, "#6f8f45", "#7a5a3c", "#654a31") + box(ox, oy, s, 2, 0, 2, 3, .3, OR2, "#a9461b", "#933b16")
    return f'<svg width="56" height="44" viewBox="0 0 56 44">{g}</svg>'


def game2():
    says = ""
    for cid, n, role, q, acc in CAST:
        says += (f'<div class="say"><svg width="34" height="46" viewBox="-17 -46 34 50">{shadow(2, 0, 9, 2.4, "#3a2a1a", .2)}'
                 f'{peg(acc, 0, 0, .95, fill=PAINT[cid], head=WOODH, ink=None, shade="#000")}</svg><b>{n}</b>“{q}”</div>')
    pcs = "".join(f'<label class="pc"><input type="radio" id="c2{l}" name="c2"{" checked" if l == SEL else ""}>{piece_icon(l)}<b>{t}</b><span>{d}</span></label>' for l, t, d in MOTIONS)
    dots = "".join(f'<i class="{"" if i < STREAK else "o"}"></i>' for i in range(7))
    return f'''<div class="c2"><i class="light"></i>
{diorama()}
<p class="meta">Session {SESSION} · {DATE}</p>
<h1>The<br>empty<br>lot</h1>
<p class="rule">Six neighbors stand around it. <b>Set down the piece most of them will back.</b></p>
<div class="streak">{dots}<span>{STREAK} days</span></div>
<div class="shelf"><div class="says">{says}</div>
<div class="pieces">{pcs}<button class="cta">Call the vote<small>{SAT} votes today</small></button></div></div></div>'''


def kit2():
    acc = {c[0]: c[4] for c in CAST}
    row = "".join(f'<figure><svg width="58" height="78" viewBox="-29 -62 58 78">{shadow(3, 0, 12, 3, "#3a2a1a", .25)}{peg(acc[c], 0, 0, 1.25, fill=PAINT[c], head=WOODH, ink=None, shade="#000")}</svg><figcaption>{n}</figcaption></figure>' for c, n, *_ in CAST)
    pal = "".join(f'<i style="display:inline-block;width:22px;height:22px;border-radius:50%;background:{PAINT[c]};margin-right:4px"></i>' for c, *_ in CAST)
    return kit("02", "Maquette",
               "Inspirée de <b>Dairy Food</b>, de <b>Matchball</b> et de la lumière de <b>Raben Rifaie</b>. Le pâté de maisons est une petite maquette posée sur la table "
               "du conseil : la boulangerie, la rue, et au milieu le terrain vide en pointillé. Les voisins sont des <b>figurines en bois peint</b>. "
               "Les motions sont des <b>pièces de maquette</b> ; celle qu'on choisit tombe sur le terrain avec un petit rebond.",
               [("Le casting, en bois peint", f'<div class="castrow">{row}</div><p class="note">Le même casting, peint à la main : une couleur de vêtement par voisin, tête en bois brut, ombre portée chaude.</p>'),
                ("Couleur", sw(SAND, "Sable", SAND, "table, fond") + sw(NAVY, "Marine", NAVY, "texte") + sw(OR2, "Orange", OR2, "action, terrain de jeu") + f'<p class="note">Peinture des figurines (les seules couleurs en plus, toujours sur un personnage) : <br>{pal}</p>'),
                ("Typo", f'<p style="font-weight:900;font-stretch:72%;font-size:44px;line-height:.86;text-transform:uppercase;color:{NAVY}">The<br>empty lot</p><p class="note">Archivo 900, largeur 72 %, en colonne à gauche : le titre fait contrepoids à la maquette.</p>'),
                ("Motifs", f'<div style="display:flex;gap:10px;align-items:center">{piece_icon("A")}{piece_icon("B")}{piece_icon("C")}</div><p class="note">Pièces de maquette en iso, emplacement en pointillé, série en pastilles (pleine = jour joué, pointillée = aujourd’hui).</p>')])


# =================================================================== 03 STICKERS
CREAM, INK3, OR3 = "#f3eee2", "#151515", "#ff5a1f"
GRAIN3 = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='3' seed='8'/>"
          "<feColorMatrix values='0 0 0 0 .35 0 0 0 0 .3 0 0 0 0 .2 0 0 0 .16 0'/></filter><rect width='200' height='200' filter='url(%23n)'/></svg>")
TINT = {"ines": "#f6c9b5", "theo": "#bfd6e8", "ruth": "#d9cdea", "sam": "#bfe0cc", "odile": "#f3dc9a", "kofi": "#d5d6d8"}

CSS3 = f"""
.c3{{--cream:{CREAM};--ink:{INK3};--or:{OR3};width:100%;height:100%;position:relative;background:var(--cream);color:var(--ink)}}
.c3:before{{content:"";position:absolute;inset:0;background:url("{GRAIN3}");mix-blend-mode:multiply;pointer-events:none}}
.c3>*{{position:relative}}
.c3 .meta{{position:absolute;left:28px;top:22px;right:28px;display:flex;justify-content:space-between;font:500 11px/1 "DM Mono",monospace;letter-spacing:.06em;text-transform:uppercase}}
.c3 h1{{position:absolute;left:28px;top:42px;font-weight:900;font-stretch:100%;font-size:52px;line-height:.92;letter-spacing:-.03em;text-transform:uppercase}}
.c3 h1 .sel{{position:relative;display:inline-block;padding:0 6px}}
.c3 h1 .sel:before{{content:"";position:absolute;inset:2px -2px -2px -2px;border:1.5px solid var(--or)}}
.c3 .hd{{position:absolute;width:8px;height:8px;background:#fff;border:1.5px solid var(--or)}}
.c3 .rule{{position:absolute;left:30px;top:146px;font-size:14.5px;font-weight:500}}
.c3 .rule b{{font-weight:800}}
.c3 .grid{{position:absolute;left:22px;right:22px;top:186px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:30px 14px}}
.c3 .st{{display:grid;grid-template-columns:90px 1fr;align-items:center;gap:6px}}
.c3 .st svg{{filter:drop-shadow(0 2px 2px rgba(0,0,0,.18))}}
.c3 .st p{{font-size:13.5px;line-height:1.24;font-weight:550;background:#fff;border-radius:12px;padding:7px 10px;position:relative;box-shadow:0 1px 0 rgba(0,0,0,.06)}}
.c3 .st p:before{{content:"";position:absolute;left:-6px;top:50%;margin-top:-6px;border:6px solid transparent;border-right-color:#fff;border-left:0}}
.c3 .st p em{{display:block;font:500 9.5px/1 "DM Mono",monospace;font-style:normal;letter-spacing:.06em;text-transform:uppercase;opacity:.55;margin-top:4px}}
.c3 .mos{{position:absolute;left:28px;right:28px;bottom:78px;display:flex;gap:16px;justify-content:space-between}}
.c3 .mo{{flex:1;position:relative;cursor:pointer;background:#fff;border-radius:999px;padding:11px 18px 11px 54px;box-shadow:0 0 0 5px #fff,0 3px 8px rgba(0,0,0,.18);transition:transform .15s}}
.c3 .mo:nth-child(1){{transform:rotate(-1.5deg)}} .c3 .mo:nth-child(2){{transform:rotate(1deg)}} .c3 .mo:nth-child(3){{transform:rotate(-.6deg)}}
.c3 .mo:hover{{transform:rotate(0) translateY(-2px)}}
.c3 .mo i{{position:absolute;left:12px;top:50%;margin-top:-16px;width:32px;height:32px;border-radius:50%;background:var(--ink);color:var(--cream);font-style:normal;font-weight:900;font-size:16px;display:grid;place-items:center}}
.c3 .mo b{{display:block;font-weight:850;font-size:15px;letter-spacing:-.01em;line-height:1.1}}
.c3 .mo span{{display:block;font-size:11.5px;line-height:1.25;margin-top:2px}}
.c3 .mo .box{{position:absolute;inset:-12px -10px;border:1.5px solid var(--or);border-radius:4px;opacity:0;pointer-events:none}}
.c3 .mo .box s{{position:absolute;width:8px;height:8px;background:#fff;border:1.5px solid var(--or)}}
.c3 .mo .cur{{position:absolute;right:-16px;bottom:-22px;opacity:0}}
.c3 .mo:has(input:checked){{transform:rotate(0) scale(1.04);z-index:2}}
.c3 .mo:has(input:checked) i{{background:var(--or);color:#fff}}
.c3 .mo:has(input:checked) .box,.c3 .mo:has(input:checked) .cur{{opacity:1}}
.c3 .foot{{position:absolute;left:28px;right:28px;bottom:18px;display:flex;justify-content:flex-end;align-items:center;gap:14px}}
.c3 .foot p{{font-size:13px;font-weight:600}}
.c3 .foot p b{{font-weight:900}}
.c3 .cta{{height:46px;padding:0 24px;border-radius:23px;background:var(--ink);color:#fff;font-weight:850;font-size:15px;letter-spacing:.02em;border:2px solid var(--ink);box-shadow:0 4px 0 #000}}
"""


def sticker_face(cid, acc, size=74):
    """Head-and-shoulders sticker: the peg close up, die-cut with a white border."""
    inner = peg(acc, 0, 0, 1, fill="#fff", head="#fff", ink=INK3, sw=1.5)
    blob = f'<circle cx="0" cy="-22" r="26" fill="{TINT[cid]}"/>'
    clip = f'<clipPath id="cp{cid}"><circle cx="0" cy="-22" r="26"/></clipPath>'
    return (f'<svg width="{size}" height="{size}" viewBox="-37 -59 74 74"><defs>{clip}</defs>'
            f'<circle cx="0" cy="-22" r="33" fill="#fff"/>{blob}<g clip-path="url(#cp{cid})"><g transform="translate(0 19) scale(1.22)">{inner}</g></g></svg>')


def game3():
    sts = "".join(f'<div class="st">{sticker_face(cid, acc, 90)}<p>{q}<em>{n} · {role}</em></p></div>' for cid, n, role, q, acc in CAST)
    handles = "".join(f'<s style="{p}"></s>' for p in ("left:-5px;top:-5px", "right:-5px;top:-5px", "left:-5px;bottom:-5px", "right:-5px;bottom:-5px"))
    cur = f'<svg class="cur" width="22" height="26" viewBox="0 0 22 26"><path d="M2 2l16 10-7 1.5 4 8-3 1.5-4-8-6 5z" fill="{INK3}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>'
    mos = "".join(f'<label class="mo"><input type="radio" id="c3{l}" name="c3"{" checked" if l == SEL else ""}><i>{l}</i><b>{t}</b><span>{d}</span><span class="box">{handles}</span>{cur}</label>' for l, t, d in MOTIONS)
    return f'''<div class="c3">
<div class="meta"><span>Session {SESSION} · {DATE}</span><span>{STREAK}-day streak</span></div>
<h1>Tonight: the<br><span class="sel">empty lot</span></h1>
<p class="rule">Six neighbors have their say. <b>Stick with the motion most of them will back.</b></p>
<div class="grid">{sts}</div>
<div class="mos">{mos}</div>
<div class="foot"><p><b>{SAT}</b> neighbors voted today</p><button class="cta">Call the vote</button></div></div>'''


def kit3():
    row = "".join(f'<figure>{sticker_face(cid, acc, 62)}<figcaption>{n}</figcaption></figure>' for cid, n, _, _, acc in CAST)
    return kit("03", "Stickers",
               "Inspirée de <b>Gemeos</b>. Chaque voisin est un <b>sticker découpé</b> : la tête du personnage sur une pastille de couleur, avec un bord blanc. Les motions sont des stickers "
               "en pilule, posés un peu de travers. Celle qu'on choisit se redresse et prend un <b>cadre de sélection</b> orange avec ses poignées, "
               "comme un objet sélectionné dans un éditeur.",
               [("Le casting, en stickers", f'<div class="castrow">{row}</div><p class="note">Le même casting en gros plan. Chaque voisin a une pastille pâle, qui sert à le reconnaître sans ajouter d’accent.</p>'),
                ("Couleur", sw(CREAM, "Crème", CREAM, "fond granuleux") + sw(INK3, "Encre", INK3, "texte, traits") + sw(OR3, "Orange sélection", OR3, "cadre, choix") + '<p class="note">Les pastilles des voisins sont des tons pâles, jamais saturés ; l’orange reste la seule couleur vive.</p>'),
                ("Typo", '<p style="font-weight:900;font-size:40px;line-height:.92;letter-spacing:-.03em;text-transform:uppercase">Tonight:<br>empty lot</p><p class="note">Archivo 900, largeur 100 %, approche très serrée ; DM Mono pour la méta.</p>'),
                ("Motifs", f'<div style="position:relative;display:inline-block;padding:8px 14px;border:1.5px solid {OR3};font-weight:850">Selected<s style="position:absolute;left:-5px;top:-5px;width:8px;height:8px;background:#fff;border:1.5px solid {OR3}"></s><s style="position:absolute;right:-5px;bottom:-5px;width:8px;height:8px;background:#fff;border:1.5px solid {OR3}"></s></div><p class="note">Bord blanc découpé, sticker légèrement tourné, cadre de sélection à poignées, curseur.</p>')])


if __name__ == "__main__":
    page("01", "foule", "Foule", CSS1, game1(), kit1())
    page("02", "maquette", "Maquette", CSS2, game2(), kit2())
    page("03", "stickers", "Stickers", CSS3, game3(), kit3())
    print("ok")
