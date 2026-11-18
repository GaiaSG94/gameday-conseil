"""Conseil — V2 planches (page Jeu, desktop only).

Each planche = the 1440x900 desktop screen (post in the feed), then below it the
identity kit for that direction: material, palette, type, motifs.
Usage: python3 G-DESIGN/_src/gen2.py G-DESIGN/planches/v2
"""
import math, pathlib, random, sys

SRC = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
F = {k: (SRC / f"fonts/{k}.b64").read_text() for k in ("archivo", "dmmono-400", "dmmono-500")}

OPINIONS = [
    ("Ines", "bakery, no. 4", "Keep a lane clear for my 6 a.m. deliveries."),
    ("Theo", "dad of three", "The kids need a place that isn't a car park."),
    ("Ruth", "here since 1984", "Quiet after dark. Last summer was too much."),
    ("Sam", "bike courier", "Somewhere to lock a bike that isn't a lamppost."),
    ("Odile", "garden waitlist", "Two years waiting for a plot. Two."),
    ("Kofi", "owns no. 12", "Fine by me, as long as owners pay nothing."),
]
MOTIONS = [
    ("A", "Community garden", "Plots for the waitlist. Gate locked at 9 pm."),
    ("B", "Play court & bike racks", "Paved court, racks along the lane, lit till 11 pm."),
    ("C", "Shared lot", "Beds, a play corner and racks. Small owner levy."),
]
SESSION, DATE, STREAK, SAT = 47, "Wed 18 Nov", 6, "1,284"
SEL = "B"

# ------------------------------------------------------------- hand-drawn marks
def _smooth(pts, closed=False):
    """Catmull-Rom -> cubic bezier path."""
    if closed: pts = pts[-1:] + pts + pts[:2]
    else: pts = pts[:1] + pts + pts[-1:]
    d = f"M{pts[1][0]:.1f} {pts[1][1]:.1f}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


def loop(cx, cy, rx, ry, seed=1, turns=1.12):
    """A marker circle that overshoots its start, like a hand ring."""
    r = random.Random(seed); n = 14; pts = []
    a0 = r.uniform(-2.4, -1.8)
    for i in range(n + 1):
        t = a0 + turns * 2 * math.pi * i / n
        k = 1 + r.uniform(-.05, .05) + .06 * i / n
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))
    return _smooth(pts)


def wobble(x1, y1, x2, y2, seed=1, amp=1.6, n=5):
    r = random.Random(seed); pts = []
    for i in range(n + 1):
        t = i / n; nx, ny = -(y2 - y1), (x2 - x1); L = math.hypot(nx, ny) or 1
        j = r.uniform(-amp, amp) * math.sin(math.pi * t)
        pts.append((x1 + (x2 - x1) * t + nx / L * j, y1 + (y2 - y1) * t + ny / L * j))
    return _smooth(pts)


def scribble(w, h, step=5.5, seed=2):
    """Marker fill: tight zigzag strokes, as when you colour in a box."""
    r = random.Random(seed); d = f"M{r.uniform(0, 3):.1f} {h - 1:.1f}"; x = 0; up = True
    while x < w + step:
        x += step
        d += f" L{x + r.uniform(-1, 1):.1f} {(r.uniform(-2, 2) if up else h + r.uniform(-2, 2)):.1f}"
        up = not up
    return d


def tally_marks(n, h=18, gap=5, seed=4):
    r = random.Random(seed); ds = []; x = 2
    for i in range(n):
        if i % 5 == 4:
            ds.append(wobble(x - 4 * gap - 3, h * .8, x + 1, h * .25, seed + i, .6, 2)); x += gap + 6; continue
        ds.append(wobble(x + r.uniform(-.6, .6), 2 + r.uniform(0, 2), x + r.uniform(-1, 1), h - r.uniform(0, 2), seed + i, .5, 2)); x += gap
    return ds, x + 4


# ------------------------------------------------------------- shared page shell
BASE = """
@font-face{font-family:"Archivo";src:url(data:font/woff2;base64,__ARCHIVO__) format("woff2");font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:"DM Mono";src:url(data:font/woff2;base64,__DM4__) format("woff2");font-weight:400}
@font-face{font-family:"DM Mono";src:url(data:font/woff2;base64,__DM5__) format("woff2");font-weight:500}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#cfccc5;font-family:"Archivo",sans-serif;color:#1d1d1b}
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
/* identity kit */
.kit{background:#f7f6f2;padding:46px 56px 60px;display:grid;grid-template-columns:330px 1fr;gap:28px 56px;border-top:1px solid #d9d6cf}
.kit .k{font:500 11px/1.3 "DM Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:#7a766d}
.kit h2{font-weight:800;font-stretch:80%;font-size:46px;line-height:.95;letter-spacing:-.01em;margin-top:8px}
.kit .why{font-size:14.5px;line-height:1.55;color:#34322e;margin-top:16px;max-width:330px}
.kit .why b{font-weight:650}
.kit .cols{display:grid;grid-template-columns:repeat(4,1fr);gap:26px}
.kit .cell .k{margin-bottom:12px}
.kit .note{font-size:12.5px;line-height:1.45;color:#4a4740;margin-top:10px}
.sw{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.sw i{width:42px;height:42px;border-radius:3px;display:block;flex:none;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.sw b{display:block;font-size:13px;font-weight:650}
.sw span{font:400 11px/1.3 "DM Mono",monospace;color:#6b675f}
.tile{width:100%;height:150px;border-radius:3px;position:relative;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)}
.motifs{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.motifs>*{flex:none}
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
    html = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conseil · Jeu V2 · {num} {title}</title>
<style>{base}{css}</style></head>
<body><div class="sheet" id="sheet">{chrome(game)}{kit}</div>
<script>(function(){{var s=document.getElementById("sheet");function f(){{var k=Math.min(1,innerWidth/1440);s.style.transform="scale("+k+")";document.body.style.height=s.offsetHeight*k+"px"}}addEventListener("resize",f);f()}})();</script>
</body></html>'''
    (OUT / f"{num}-{slug}.html").write_text(html)


def kit(num, title, why, cells):
    cols = "".join(f'<div class="cell"><p class="k">{k}</p>{body}</div>' for k, body in cells)
    return f'''<section class="kit"><div><p class="k">Conseil · page Jeu · V2 · direction {num}/03</p><h2>{title}</h2><p class="why">{why}</p></div>
<div class="cols">{cols}</div></section>'''


def sw(color, name, hexv, role):
    return f'<div class="sw"><i style="background:{color}"></i><div><b>{name}</b><span>{hexv} · {role}</span></div></div>'


# =============================================================== 01 FEUTRE (flipchart)
NAVY, ORANGE = "#1f3a5f", "#e8622a"
PAPER1 = "#efece4"
NOISE1 = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
          "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.012 .9' numOctaves='3' seed='7'/>"
          "<feColorMatrix values='0 0 0 0 .42 0 0 0 0 .40 0 0 0 0 .36 0 0 0 .16 0'/></filter>"
          "<rect width='220' height='220' filter='url(%23n)'/></svg>")
GRID1 = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='50' height='50'>"
         "<path d='M50 0V50M0 50H50' stroke='%2393a9c4' stroke-opacity='.38' stroke-width='1' fill='none'/></svg>")

CSS1 = f"""
.f1{{--navy:{NAVY};--orange:{ORANGE};--paper:{PAPER1};width:100%;height:100%;position:relative;background:#cbc6ba;color:var(--navy)}}
.f1 .clamp{{position:absolute;left:0;right:0;top:0;height:24px;background:#34373c;box-shadow:0 3px 0 rgba(0,0,0,.18);z-index:3}}
.f1 .clamp i{{position:absolute;top:7px;width:10px;height:10px;border-radius:50%;background:#7d8188;box-shadow:inset -1px -1px 0 #4d5056}}
.f1 .stubs{{position:absolute;left:0;right:0;top:24px;height:12px;z-index:2}}
.f1 .pad{{position:absolute;left:0;right:0;top:24px;bottom:0;background:var(--paper) url("{GRID1}") 18px 6px/50px 50px;}}
.f1 .pad:before{{content:"";position:absolute;inset:0;background:url("{NOISE1}");mix-blend-mode:multiply;pointer-events:none}}
.f1 .in{{position:absolute;inset:16px 30px 18px 34px;display:flex;flex-direction:column}}
.f1 .mk{{filter:url(#marker)}}
.f1 .top{{display:flex;justify-content:space-between;align-items:center;font:500 12px/1 "DM Mono",monospace;letter-spacing:.06em;text-transform:uppercase}}
.f1 .top .st{{display:flex;align-items:center;gap:8px}}
.f1 h1{{font-weight:850;font-stretch:64%;font-size:62px;line-height:.86;text-transform:uppercase;letter-spacing:.005em;margin-top:14px;position:relative}}
.f1 h1 svg{{position:absolute;left:-6px;top:50px}}
.f1 .rule{{font-size:15px;font-weight:500;font-stretch:92%;margin-top:14px}}
.f1 .rule b{{font-weight:750}}
.f1 .ops{{display:grid;grid-template-columns:1fr 1fr;gap:12px 34px;margin-top:16px}}
.f1 .op{{display:grid;grid-template-columns:22px 1fr;align-items:start}}
.f1 .op svg{{margin-top:8px}}
.f1 .q{{font-size:16.5px;line-height:1.22;font-weight:520;font-stretch:90%}}
.f1 .who{{font:500 10.5px/1 "DM Mono",monospace;letter-spacing:.05em;text-transform:uppercase;margin-top:4px;opacity:.72}}
.f1 .who b{{font-weight:500;opacity:1;color:var(--navy)}}
.f1 .div{{margin:14px -6px 0}}
.f1 .mos{{display:grid;grid-template-columns:1fr 1fr 1fr;position:relative;margin-top:2px;flex:1}}
.f1 .mos .vl{{position:absolute;top:6px;bottom:6px}}
.f1 .mo{{position:relative;padding:8px 16px 0 14px;cursor:pointer;display:block}}
.f1 .mo:first-child{{padding-left:0}}
.f1 .ml{{font-weight:900;font-stretch:62%;font-size:40px;line-height:.9;display:inline-block;position:relative}}
.f1 .ml svg{{position:absolute;left:-14px;top:-9px;opacity:0}}
.f1 .mt{{display:block;font-weight:780;font-stretch:72%;font-size:20px;line-height:1;text-transform:uppercase;margin-top:4px}}
.f1 .md{{display:block;font-size:13px;line-height:1.3;font-weight:470;font-stretch:92%;margin-top:4px;max-width:190px}}
.f1 .target{{position:absolute;right:14px;top:8px;width:34px;height:34px;border-radius:50%;border:1.6px dashed rgba(31,58,95,.45)}}
.f1 .dot{{position:absolute;right:13px;top:7px;width:36px;height:36px;border-radius:50%;background:var(--orange);
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.08),inset 4px 5px 0 -2px rgba(255,255,255,.18),1px 2px 1px rgba(60,30,10,.35);transform:rotate(-8deg) scale(.4);opacity:0;transition:transform .22s cubic-bezier(.3,1.6,.5,1),opacity .1s}}
.f1 .mo:hover .target{{border-color:var(--navy)}}
.f1 .mo:has(input:checked) .dot{{opacity:1;transform:rotate(-8deg) scale(1)}}
.f1 .mo:has(input:checked) .target{{opacity:0}}
.f1 .mo:has(input:checked) .ml svg{{opacity:1}}
.f1 .foot{{display:flex;justify-content:space-between;align-items:center}}
.f1 .cnt{{font:500 11px/1.35 "DM Mono",monospace;letter-spacing:.05em;text-transform:uppercase}}
.f1 .cnt i{{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--orange);vertical-align:-1px;margin-right:6px}}
.f1 .cta{{position:relative;height:50px;padding:0 30px;font-weight:850;font-stretch:66%;font-size:23px;text-transform:uppercase;color:var(--paper);letter-spacing:.02em}}
.f1 .cta svg{{position:absolute;inset:0;z-index:0}}
.f1 .cta span{{position:relative}}
"""


def game1():
    seed = 10
    # torn stubs of the previous sheets under the clamp
    r = random.Random(3); pts = "0,0 740,0 "; x = 740
    while x > 0:
        x -= r.uniform(6, 16); pts += f"{x:.0f},{r.uniform(3, 11):.1f} "
    stubs = f'<svg class="stubs" width="740" height="12"><polygon points="{pts}0,0" fill="#e2ded3"/><polyline points="{pts}" fill="none" stroke="#c9c3b5" stroke-width=".8"/></svg>'
    t, w = tally_marks(STREAK)
    tally = f'<svg class="mk" width="{w}" height="18">' + "".join(f'<path d="{d}" stroke="{NAVY}" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for d in t) + "</svg>"
    under = f'<svg class="mk" width="430" height="16"><path d="{wobble(4, 10, 420, 6, 5, 2.2, 6)}" stroke="{ORANGE}" stroke-width="0" fill="none"/><path d="{wobble(2, 11, 404, 7, 5, 2.4, 6)}" stroke="{NAVY}" stroke-width="3.4" fill="none" stroke-linecap="round"/></svg>'
    ops = ""
    for i, (n, role, q) in enumerate(OPINIONS):
        dash = f'<svg class="mk" width="14" height="6"><path d="{wobble(1, 3, 12, 3, 20 + i, .8, 2)}" stroke="{NAVY}" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>'
        ops += f'<div class="op">{dash}<div><p class="q">“{q}”</p><p class="who"><b>{n}</b> · {role}</p></div></div>'
    div = f'<svg class="mk div" width="690" height="8"><path d="{wobble(2, 4, 686, 5, 31, 1.4, 8)}" stroke="{NAVY}" stroke-width="2" fill="none" stroke-linecap="round"/></svg>'
    vls = "".join(f'<svg class="mk vl" style="left:{x}px" width="6" height="118"><path d="{wobble(3, 2, 3, 114, 40 + x, 1.2, 4)}" stroke="{NAVY}" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>' for x in (222, 450))
    mos = ""
    for l, tt, d in MOTIONS:
        ring = f'<svg class="mk" width="52" height="56"><path d="{loop(26, 28, 21, 23, ord(l))}" stroke="{NAVY}" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>'
        chk = " checked" if l == SEL else ""
        mos += (f'<label class="mo"><input type="radio" name="f1"{chk}><span class="ml">{l}{ring}</span>'
                f'<span class="mt">{tt}</span><span class="md">{d}</span><i class="target"></i><i class="dot"></i></label>')
    cta_fill = f'<svg class="mk" width="100%" height="50" viewBox="0 0 220 50" preserveAspectRatio="none"><path d="{scribble(220, 50, 4.2, 9)}" stroke="{NAVY}" stroke-width="7" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>'
    return f'''<div class="f1">
<svg width="0" height="0" style="position:absolute"><filter id="marker" x="-5%" y="-20%" width="110%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="4" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="1.8"/></filter><filter id="markerT"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="1" seed="6" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale=".8"/></filter></svg>
<div class="pad"></div>{stubs}<div class="clamp"><i style="left:120px"></i><i style="right:120px"></i></div>
<div class="in" style="top:44px">
<div class="top"><span>Session {SESSION} · {DATE}</span><span class="st">{tally} {STREAK} days in the chair</span></div>
<h1 style="filter:url(#markerT)">Alder St. lot:<br>what do we do?</h1>
<p class="rule">Six neighbors spoke. <b>Put your dot on the motion most of them will back.</b></p>
<div class="ops">{ops}</div>{div}
<div class="mos">{vls}{mos}</div>
<div class="foot"><span class="cnt"><i></i>{SAT} dots placed today · one dot each</span><button class="cta">{cta_fill}<span>Call the vote →</span></button></div>
</div></div>'''


def kit1():
    tile_paper = f'<div class="tile" style="background:{PAPER1} url(&quot;{GRID1}&quot;) 0 0/50px 50px"><div style="position:absolute;inset:0;background:url(&quot;{NOISE1}&quot;);mix-blend-mode:multiply"></div></div>'
    t, w = tally_marks(7)
    tally = f'<svg class="mk" width="{w}" height="18">' + "".join(f'<path d="{d}" stroke="{NAVY}" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for d in t) + "</svg>"
    ring = f'<svg class="mk" width="60" height="60"><path d="{loop(30, 30, 24, 24, 77)}" stroke="{NAVY}" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>'
    dot = f'<span style="width:36px;height:36px;border-radius:50%;background:{ORANGE};display:block;box-shadow:inset 4px 5px 0 -2px rgba(255,255,255,.18),1px 2px 1px rgba(60,30,10,.35)"></span>'
    target = '<span style="width:34px;height:34px;border-radius:50%;border:1.6px dashed rgba(31,58,95,.5);display:block"></span>'
    fill = f'<svg class="mk" width="90" height="34"><path d="{scribble(90, 34, 4, 3)}" stroke="{NAVY}" stroke-width="6" fill="none" stroke-linejoin="round"/></svg>'
    return kit("01", "Feutre",
               "Le <b>paperboard</b> de l'idée pris au pied de la lettre : le bloc de feuilles quadrillées sur son chevalet, à la salle des fêtes. "
               "Le joueur vote comme dans une vraie réunion, avec une <b>gommette</b> (le vote par gommettes). Tout ce qui est « écrit à la main » "
               "est tracé au feutre, avec un trait qui tremble un peu ; le reste est composé en Archivo très condensé.",
               [("Matière", tile_paper + '<p class="note">Papier journal 60 g, gris chaud, fibres horizontales. Quadrillage bleu pâle de 25 mm imprimé sur le bloc. En haut, la pince du chevalet et les restes des feuilles arrachées.</p>'),
                ("Couleur", sw(PAPER1, "Bloc", PAPER1, "fond") + sw(NAVY, "Feutre marine", NAVY, "tout le texte") + sw(ORANGE, "Gommette", ORANGE, "le vote, rien d'autre") + sw("#34373c", "Chevalet", "#34373c", "pince") + '<p class="note">Deux encres sur papier. L’orange n’apparaît que là où un voisin ou le joueur a voté.</p>'),
                ("Typo", '<p style="font-weight:850;font-stretch:64%;font-size:44px;line-height:.86;text-transform:uppercase;color:#1f3a5f">Alder St.<br>lot</p><p style="font-size:15px;font-weight:520;font-stretch:90%;margin-top:10px;color:#1f3a5f">“Two years waiting for a plot.”</p><p style="font:500 11px/1 DM Mono,monospace;letter-spacing:.05em;margin-top:8px;color:#1f3a5f">ODILE · GARDEN WAITLIST</p><p class="note">Archivo 850, largeur 64 % pour les titres ; Archivo 520, 90 % pour les avis ; DM Mono pour les petites mentions.</p>'),
                ("Motifs", f'<div class="motifs">{dot}{target}{ring}{tally}{fill}</div><p class="note">Gommette posée, emplacement vide, cercle au feutre, série comptée en bâtons, aplat gribouillé du bouton.</p>')])


# =============================================================== 02 RISO (affiche de quartier)
BLUE, ORANGE2, CREAM = "#2c4a8a", "#ff6c2f", "#f2ebda"
GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'>"
         "<filter id='g'><feTurbulence type='fractalNoise' baseFrequency='1.1' numOctaves='2' seed='11'/>"
         "<feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -9 7.1'/></filter>"
         "<rect width='180' height='180' filter='url(%23g)'/></svg>")
PAPERN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>"
          "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.7' numOctaves='3' seed='2'/>"
          "<feColorMatrix values='0 0 0 0 .5 0 0 0 0 .44 0 0 0 0 .33 0 0 0 .14 0'/></filter>"
          "<rect width='200' height='200' filter='url(%23n)'/></svg>")
WALL = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
        "<filter id='w'><feTurbulence type='fractalNoise' baseFrequency='.045' numOctaves='4' seed='9'/>"
        "<feColorMatrix values='0 0 0 0 .2 0 0 0 0 .2 0 0 0 0 .2 0 0 0 .22 0'/></filter>"
        "<rect width='240' height='240' filter='url(%23w)'/></svg>")

CSS2 = f"""
.r2{{--blue:{BLUE};--or:{ORANGE2};--cream:{CREAM};width:100%;height:100%;position:relative;background:#a9b0b3 url("{WALL}");overflow:hidden}}
.r2 .poster{{position:absolute;left:22px;top:16px;width:696px;height:600px;background:var(--cream);box-shadow:0 1px 0 rgba(0,0,0,.1),0 10px 18px -10px rgba(0,0,0,.5);transform:rotate(-.35deg)}}
.r2 .poster:before{{content:"";position:absolute;inset:0;background:url("{PAPERN}");mix-blend-mode:multiply;pointer-events:none}}
.r2 .ink{{-webkit-mask:url("{GRAIN}");mask:url("{GRAIN}")}}
.r2 .tape{{position:absolute;width:84px;height:26px;background:rgba(236,226,196,.82);box-shadow:0 1px 1px rgba(0,0,0,.12);z-index:3;
  clip-path:polygon(0 8%,6% 0,12% 10%,18% 2%,100% 0,96% 22%,100% 40%,95% 60%,100% 80%,97% 100%,0 100%,4% 70%,0 45%,5% 25%)}}
.r2 .reg{{position:absolute;width:16px;height:16px}}
.r2 .in{{position:absolute;inset:22px 28px 0 28px}}
.r2 .kick{{display:flex;justify-content:space-between;align-items:baseline;color:var(--blue);font-weight:800;font-stretch:125%;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase}}
.r2 .title{{position:relative;margin-top:12px;height:94px}}
.r2 .title h1{{position:absolute;left:0;top:0;font-weight:900;font-stretch:62%;font-size:112px;line-height:.82;text-transform:uppercase;letter-spacing:-.005em;white-space:nowrap}}
.r2 .title .o{{color:transparent;background:radial-gradient(circle,var(--or) 46%,transparent 49%) 0 0/5px 5px;-webkit-background-clip:text;background-clip:text;transform:translate(7px,6px);mix-blend-mode:multiply}}
.r2 .title .b{{color:var(--blue);mix-blend-mode:multiply}}
.r2 .sub{{color:var(--blue);font-weight:700;font-stretch:125%;font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;margin-top:8px;display:flex;gap:14px;align-items:center}}
.r2 .sub i{{display:inline-block;width:7px;height:7px;background:var(--or);border-radius:50%}}
.r2 .stamp{{position:absolute;right:10px;top:100px;width:68px;height:68px;border-radius:50%;background:radial-gradient(circle,var(--or) 48%,transparent 51%) 0 0/4px 4px;display:grid;place-items:center;text-align:center;mix-blend-mode:multiply;transform:rotate(8deg)}}
.r2 .stamp b{{display:block;font-weight:900;font-stretch:62%;font-size:34px;line-height:.8;color:var(--blue)}}
.r2 .stamp span{{display:block;font-weight:800;font-stretch:100%;font-size:6.5px;letter-spacing:.12em;color:var(--blue);margin-top:2px}}
.r2 .said{{color:var(--blue);margin-top:30px;width:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:10px 18px;border-top:3px solid var(--blue);padding-top:10px}}
.r2 .said .n{{font-weight:900;font-stretch:62%;font-size:22px;line-height:1;color:var(--or);mix-blend-mode:multiply}}
.r2 .said .q{{font-size:14.5px;line-height:1.22;font-weight:560;font-stretch:88%;margin-top:2px}}
.r2 .said .w{{font-weight:750;font-stretch:120%;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;margin-top:5px;opacity:.85}}
.r2 .act{{display:flex;justify-content:space-between;align-items:center;margin-top:14px;color:var(--blue)}}
.r2 .act p{{font-weight:650;font-stretch:90%;font-size:14.5px}}
.r2 .act p b{{font-weight:850}}
.r2 .cta{{background:var(--blue);color:var(--cream);font-weight:900;font-stretch:110%;font-size:14px;letter-spacing:.12em;text-transform:uppercase;height:42px;padding:0 20px;white-space:nowrap;flex:none}}
.r2 .tabs{{position:absolute;left:0;right:0;bottom:0;height:150px;display:grid;grid-template-columns:repeat(3,1fr)}}
.r2 .perf{{position:absolute;left:0;right:0;bottom:150px;border-top:2px dashed rgba(44,74,138,.55)}}
.r2 .tab{{position:relative;cursor:pointer;color:var(--blue);padding:14px 18px 0;border-left:1.5px solid rgba(44,74,138,.55);transition:transform .2s}}
.r2 .tab:first-child{{border-left:0}}
.r2 .tab .ml{{display:flex;align-items:baseline;gap:8px;font-weight:800;font-stretch:125%;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase}}
.r2 .tab .ml b{{font-weight:900;font-stretch:62%;font-size:40px;letter-spacing:0;line-height:.8;color:var(--or);mix-blend-mode:multiply}}
.r2 .tab .mt{{display:block;font-weight:850;font-stretch:70%;font-size:23px;line-height:1;text-transform:uppercase;margin-top:6px}}
.r2 .tab .md{{display:block;font-size:12.5px;line-height:1.3;font-weight:520;font-stretch:90%;margin-top:5px}}
.r2 .tab:hover{{transform:translateY(-3px)}}
.r2 .tab:has(input:checked){{background:var(--cream);transform:translate(4px,-20px) rotate(-3.5deg);box-shadow:0 14px 16px -10px rgba(0,0,0,.55);z-index:4;
  clip-path:polygon(0 3%,5% 0,10% 4%,16% 1%,22% 5%,29% 0,35% 4%,42% 1%,49% 5%,56% 0,63% 4%,70% 1%,77% 5%,84% 0,91% 4%,100% 1%,100% 100%,0 100%)}}
.r2 .slot{{position:absolute;bottom:0;height:150px;background:#a9b0b3 url("{WALL}");clip-path:polygon(0 3%,5% 0,10% 4%,16% 1%,22% 5%,29% 0,35% 4%,42% 1%,49% 5%,56% 0,63% 4%,70% 1%,77% 5%,84% 0,91% 4%,100% 1%,100% 100%,0 100%);display:none}}
.r2:has(.tab:nth-child(1) input:checked) .slot{{display:block;left:0;width:33.33%}}
.r2:has(.tab:nth-child(2) input:checked) .slot{{display:block;left:33.33%;width:33.34%}}
.r2:has(.tab:nth-child(3) input:checked) .slot{{display:block;left:66.67%;width:33.33%}}
"""


def reg(x, y):
    return (f'<svg class="reg" width="16" height="16" style="{x};{y}" viewBox="0 0 16 16"><circle cx="8" cy="8" r="4.5" fill="none" stroke="{BLUE}" stroke-width="1"/>'
            f'<path d="M8 0V16M0 8H16" stroke="{BLUE}" stroke-width="1"/></svg>')


def game2():
    said = "".join(f'<div><span class="n">{i + 1:02d}</span><p class="q">“{q}”</p><p class="w">{n} · {r}</p></div>' for i, (n, r, q) in enumerate(OPINIONS))
    tabs = ""
    for l, t, d in MOTIONS:
        chk = " checked" if l == SEL else ""
        tabs += f'<label class="tab"><input type="radio" name="r2"{chk}><span class="ink" style="display:block"><span class="ml"><b>{l}</b>Motion</span><span class="mt">{t}</span><span class="md">{d}</span></span></label>'
    return f'''<div class="r2"><div class="poster">
{reg("left:8px", "top:8px")}{reg("right:8px", "top:8px")}
<div class="in"><div class="ink">
<div class="kick"><span>Neighborhood council · public meeting</span><span>No. {SESSION}</span></div>
<div class="title"><h1 class="o">The empty lot</h1><h1 class="b">The empty lot</h1></div>
<div class="sub"><span>On Alder Street</span><i></i><span>{DATE} · 7 pm</span></div>
<div class="stamp"><div><b>{STREAK}</b><span>DAYS IN<br>A ROW</span></div></div>
<div class="said">{said}</div>
<div class="act"><p>{SAT} in the room. <b>Tear off the motion most of the six will back.</b></p><button class="cta">Call the vote</button></div>
</div></div>
<div class="slot"></div><div class="perf"></div><div class="tabs">{tabs}</div>
</div><i class="tape" style="left:40px;top:4px;transform:rotate(-6deg)"></i><i class="tape" style="right:36px;top:6px;transform:rotate(5deg)"></i></div>'''


def kit2():
    tile = (f'<div class="tile" style="background:{CREAM}"><div style="position:absolute;inset:0;background:url(&quot;{PAPERN}&quot;);mix-blend-mode:multiply"></div>'
            f'<div style="position:absolute;left:18px;top:24px;width:120px;height:90px;background:{BLUE};-webkit-mask:url(&quot;{GRAIN}&quot;);mask:url(&quot;{GRAIN}&quot;);mix-blend-mode:multiply"></div>'
            f'<div style="position:absolute;left:70px;top:52px;width:120px;height:80px;background:radial-gradient(circle,{ORANGE2} 46%,transparent 49%) 0 0/5px 5px;mix-blend-mode:multiply"></div></div>')
    tab = (f'<div style="width:120px;height:74px;background:{CREAM};color:{BLUE};padding:8px 10px;transform:rotate(-4deg);box-shadow:0 8px 10px -6px rgba(0,0,0,.5);'
           f'clip-path:polygon(0 5%,8% 0,16% 6%,25% 1%,34% 6%,44% 0,54% 6%,64% 1%,74% 6%,84% 0,92% 5%,100% 1%,100% 100%,0 100%)">'
           f'<span style="font-weight:900;font-stretch:62%;font-size:28px;color:{ORANGE2}">B</span><span style="display:block;font-weight:850;font-stretch:70%;font-size:13px;text-transform:uppercase">Play court</span></div>')
    halftone = f'<span style="width:60px;height:60px;border-radius:50%;display:block;background:radial-gradient(circle,{ORANGE2} 46%,transparent 49%) 0 0/5px 5px"></span>'
    tape = '<span style="width:70px;height:22px;display:block;background:rgba(236,226,196,.9);box-shadow:0 1px 1px rgba(0,0,0,.15);clip-path:polygon(0 8%,6% 0,100% 0,96% 30%,100% 60%,96% 100%,0 100%,5% 60%,0 30%)"></span>'
    return kit("02", "Riso",
               "L'<b>affiche</b> de l'idée, comme celles qu'on scotche sur la vitrine de la laverie : deux encres en risographie (bleu et orange), "
               "avec leurs défauts réels (grain, trame, léger décalage de calage, surimpression qui fonce là où les encres se croisent). "
               "Les motions sont des <b>languettes à détacher</b> en bas de l'affiche : voter, c'est en arracher une.",
               [("Matière", tile + '<p class="note">Papier offset crème non couché. Encre bleue pleine, grain qui manque par endroits ; orange en trame de points ; surimpression en multiplication. L’affiche est scotchée sur un mur.</p>'),
                ("Couleur", sw(CREAM, "Offset crème", CREAM, "papier") + sw(BLUE, "Encre bleue", BLUE, "texte, titres") + sw(ORANGE2, "Encre orange", ORANGE2, "trame, chiffres, accent") + sw("#5b3d47", "Surimpression", "≈ #5b3d47", "les deux encres croisées") + '<p class="note">Seulement deux encres : la troisième teinte naît de leur superposition, elle n’est jamais choisie à part.</p>'),
                ("Typo", f'<p style="font-weight:900;font-stretch:62%;font-size:50px;line-height:.82;text-transform:uppercase;color:{BLUE}">Empty lot</p><p style="font-weight:800;font-stretch:125%;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:{BLUE};margin-top:8px">Public meeting · No. 47</p><p class="note">Archivo poussé aux deux extrêmes de sa largeur, comme une casse de caractères en bois : 62 % pour le titre, 125 % pour les bandeaux. Rien entre les deux.</p>'),
                ("Motifs", f'<div class="motifs">{tab}{halftone}{tape}{reg("position:relative", "left:0")}</div><p class="note">Languette arrachée, pastille en trame (la série), bout de scotch, repère de calage.</p>')])


# =============================================================== 03 TAMPON (formulaire)
FORM, CARBON, STAMP, LEDGER = "#e6ecdf", "#23263a", "#c8324f", "#4f8a66"
PAPERN3 = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>"
           "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='5'/>"
           "<feColorMatrix values='0 0 0 0 .3 0 0 0 0 .38 0 0 0 0 .3 0 0 0 .1 0'/></filter>"
           "<rect width='200' height='200' filter='url(%23n)'/></svg>")
STAMPMASK = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='80'>"
             "<filter id='s'><feTurbulence type='fractalNoise' baseFrequency='.55' numOctaves='3' seed='21'/>"
             "<feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -6 4.3'/></filter>"
             "<rect width='160' height='80' filter='url(%23s)'/></svg>")

CSS3 = f"""
.t3{{--form:{FORM};--carbon:{CARBON};--stamp:{STAMP};--ledger:{LEDGER};width:100%;height:100%;position:relative;background:#59605a;overflow:hidden}}
.t3 .form{{position:absolute;inset:14px 18px 0 18px;background:var(--form);box-shadow:0 8px 16px -8px rgba(0,0,0,.6)}}
.t3 .form:before{{content:"";position:absolute;inset:0;background:url("{PAPERN3}");mix-blend-mode:multiply;pointer-events:none}}
.t3 .holes i{{position:absolute;left:12px;width:13px;height:13px;border-radius:50%;background:#59605a;box-shadow:inset 1px 1px 2px rgba(0,0,0,.5)}}
.t3 .in{{position:absolute;inset:16px 22px 18px 42px;display:flex;flex-direction:column}}
.t3 .pr{{color:var(--ledger);font-weight:700;font-stretch:115%;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase}}
.t3 .ty{{font-family:"DM Mono",monospace;color:var(--carbon)}}
.t3 .head{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid var(--ledger);padding-bottom:6px}}
.t3 .head .nm{{font-weight:850;font-stretch:118%;font-size:15px;letter-spacing:.06em;text-transform:uppercase;color:var(--ledger)}}
.t3 .boxes{{display:grid;grid-template-columns:110px 150px 1fr 190px;border-bottom:1px solid var(--ledger)}}
.t3 .box{{border-right:1px solid var(--ledger);padding:5px 8px 6px}}
.t3 .box:last-child{{border-right:0}}
.t3 .box .ty{{font-size:15px;font-weight:500;margin-top:3px;display:block}}
.t3 .punch{{display:flex;gap:4px;margin-top:4px}}
.t3 .punch i{{width:15px;height:15px;border:1px solid var(--ledger);display:grid;place-items:center}}
.t3 .punch i.p:after{{content:"";width:9px;height:9px;border-radius:50%;background:#59605a;box-shadow:inset 1px 1px 1px rgba(0,0,0,.5)}}
.t3 .item{{padding:10px 0 10px;border-bottom:1px solid var(--ledger)}}
.t3 .item .ty{{display:block;font-size:27px;font-weight:500;letter-spacing:-.02em;margin-top:4px;line-height:1.05}}
.t3 table{{width:100%;border-collapse:collapse;margin-top:2px}}
.t3 th{{white-space:nowrap;text-align:left;padding:6px 6px 4px 0;border-bottom:1px solid var(--ledger)}}
.t3 td{{padding:5px 6px 5px 0;border-bottom:1px solid rgba(79,138,102,.45);vertical-align:top;font-size:12.5px;line-height:1.3}}
.t3 td.no{{width:30px;color:var(--ledger);font-weight:700;font-stretch:115%;font-size:10px}}
.t3 td.nm{{width:150px;font-family:"DM Mono";font-weight:500}}
.t3 td.nm span{{display:block;font-weight:400;font-size:10.5px;opacity:.7}}
.t3 td.st{{font-family:"DM Mono";font-size:12.5px}}
.t3 .mos{{margin-top:10px}}
.t3 .mo{{display:grid;grid-template-columns:26px 30px 1fr;align-items:center;border-bottom:1px solid rgba(79,138,102,.45);padding:7px 0;position:relative;cursor:pointer}}
.t3 .cb{{width:17px;height:17px;border:1.4px solid var(--ledger);position:relative}}
.t3 .mo:has(input:checked) .cb:after{{content:"X";position:absolute;left:2px;top:-3px;font:500 17px "DM Mono";color:var(--carbon)}}
.t3 .mo .l{{color:var(--ledger);font-weight:800;font-stretch:115%;font-size:12px}}
.t3 .mo .tx{{font-family:"DM Mono";color:var(--carbon);font-size:13px}}
.t3 .mo .tx b{{font-weight:500;font-size:14.5px;margin-right:8px}}
.t3 .mo .tx span{{opacity:.75}}
.t3 .mo:hover .cb{{background:rgba(79,138,102,.15)}}
.t3 .rub{{position:absolute;right:40px;top:-5px;color:var(--stamp);border:3px solid var(--stamp);border-radius:4px;padding:2px 12px 1px;font-weight:900;font-stretch:115%;font-size:22px;letter-spacing:.1em;text-transform:uppercase;
  transform:rotate(-7deg) scale(1.25);opacity:0;-webkit-mask:url("{STAMPMASK}");mask:url("{STAMPMASK}");mix-blend-mode:multiply;transition:transform .12s ease-in,opacity .08s;outline:1.5px solid var(--stamp);outline-offset:2px}}
.t3 .mo:has(input:checked) .rub{{opacity:.95;transform:rotate(-7deg) scale(1)}}
.t3 .foot{{display:flex;justify-content:space-between;align-items:center;margin-top:auto}}
.t3 .cta{{border:2.5px solid var(--carbon);color:var(--carbon);height:44px;padding:0 22px;font-weight:850;font-stretch:115%;font-size:13px;letter-spacing:.14em;text-transform:uppercase;box-shadow:3px 3px 0 var(--carbon);background:var(--form)}}
.t3 .cta:active{{transform:translate(2px,2px);box-shadow:1px 1px 0 var(--carbon)}}
"""


def game3():
    rows = "".join(f'<tr><td class="no">{i + 1:02d}</td><td class="nm">{n}<span>{r}</span></td><td class="st">{q}</td></tr>' for i, (n, r, q) in enumerate(OPINIONS))
    mos = ""
    for l, t, d in MOTIONS:
        chk = " checked" if l == SEL else ""
        mos += f'<label class="mo"><input type="radio" name="t3"{chk}><span class="cb"></span><span class="l">{l}.</span><span class="tx"><b>{t}</b><span>{d}</span></span><i class="rub">Moved</i></label>'
    punch = "".join(f'<i class="{"p" if i < STREAK else ""}"></i>' for i in range(7))
    return f'''<div class="t3"><div class="form"><div class="holes"><i style="top:90px"></i><i style="top:300px"></i><i style="top:510px"></i></div>
<div class="in">
<div class="head"><span class="nm">Neighborhood council</span><span class="pr">Form 6 · motion of the day</span></div>
<div class="boxes"><div class="box"><p class="pr">Session no.</p><span class="ty">{SESSION}</span></div><div class="box"><p class="pr">Date</p><span class="ty">{DATE}</span></div>
<div class="box"><p class="pr">In the chair</p><span class="ty">You + {SAT} more</span></div><div class="box"><p class="pr">Days in the chair</p><div class="punch">{punch}</div></div></div>
<div class="item"><p class="pr">Item on the agenda</p><span class="ty">The empty lot on Alder Street</span></div>
<table><tr><th class="pr" colspan="2">Statements received (6)</th><th class="pr">Statement</th></tr>{rows}</table>
<div class="mos"><p class="pr">Motions tabled · mark one, the one most of them will back</p>{mos}</div>
<div class="foot"><span class="pr">One form per neighbor per day</span><button class="cta">Stamp &amp; file</button></div>
</div></div></div>'''


def kit3():
    tile = (f'<div class="tile" style="background:{FORM}"><div style="position:absolute;inset:0;background:url(&quot;{PAPERN3}&quot;);mix-blend-mode:multiply"></div>'
            f'<div style="position:absolute;left:0;right:0;top:34px;border-top:2px solid {LEDGER}"></div>'
            + "".join(f'<div style="position:absolute;left:0;right:0;top:{60 + i * 22}px;border-top:1px solid rgba(79,138,102,.45)"></div>' for i in range(4))
            + f'<i style="position:absolute;left:10px;top:60px;width:13px;height:13px;border-radius:50%;background:#59605a"></i>'
            f'<span style="position:absolute;left:34px;top:64px;font:500 13px DM Mono,monospace;color:{CARBON}">Keep a lane clear…</span></div>')
    rub = (f'<span style="display:inline-block;color:{STAMP};border:3px solid {STAMP};outline:1.5px solid {STAMP};outline-offset:2px;border-radius:4px;padding:2px 12px 1px;font-weight:900;font-stretch:115%;font-size:22px;letter-spacing:.1em;text-transform:uppercase;'
           f'transform:rotate(-7deg);-webkit-mask:url(&quot;{STAMPMASK}&quot;);mask:url(&quot;{STAMPMASK}&quot;)">Moved</span>')
    punch = '<span style="display:flex;gap:4px">' + "".join(f'<i style="width:15px;height:15px;border:1px solid {LEDGER};display:grid;place-items:center">{"<b style=&quot;width:9px;height:9px;border-radius:50%;background:#59605a;display:block&quot;></b>" if i < 6 else ""}</i>' for i in range(7)) + "</span>"
    cb = f'<span style="width:17px;height:17px;border:1.4px solid {LEDGER};display:grid;place-items:center;font:500 17px DM Mono;color:{CARBON};line-height:1">X</span>'
    return kit("03", "Tampon",
               "S'écarte du kraft et de l'orange. La séance vue côté <b>secrétaire de mairie</b> : un formulaire vert pâle, des avis tapés à la machine "
               "dans un registre, et un <b>coup de tampon</b> « MOVED » quand on choisit. Le tampon donne un retour franc et satisfaisant, la série se lit comme une carte "
               "poinçonnée, et le registre aligne les six avis sans effort de lecture.",
               [("Matière", tile + '<p class="note">Papier de formulaire administratif vert pâle, imprimé d’un réglage vert foncé, perforé pour classeur. Le texte est tapé (ruban carbone), le tampon encré à la main.</p>'),
                ("Couleur", sw(FORM, "Formulaire", FORM, "papier") + sw(LEDGER, "Réglage", LEDGER, "lignes, légendes imprimées") + sw(CARBON, "Ruban carbone", CARBON, "tout ce qui est tapé") + sw(STAMP, "Encre à tampon", STAMP, "le vote, rien d'autre") + '<p class="note">Le vert est celui de l’imprimé. Le rouge n’existe que dans le tampon.</p>'),
                ("Typo", f'<p style="font:500 26px/1.05 DM Mono,monospace;letter-spacing:-.02em;color:{CARBON}">The empty lot on Alder Street</p><p style="font-weight:700;font-stretch:115%;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:{LEDGER};margin-top:8px">Item on the agenda · Form 6</p><p class="note">DM Mono pour tout ce qui est « tapé » ; Archivo large, en petites capitales espacées, pour l’imprimé du formulaire.</p>'),
                ("Motifs", f'<div class="motifs">{rub}{punch}{cb}</div><p class="note">Tampon MOVED (encre irrégulière), carte poinçonnée de la série, case cochée à la machine.</p>')])


page("01", "feutre", "Feutre", CSS1, game1(), kit1())
page("02", "riso", "Riso", CSS2, game2(), kit2())
page("03", "tampon", "Tampon", CSS3, game3(), kit3())
print("ok")
