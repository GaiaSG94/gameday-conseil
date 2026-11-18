"""Generates the 3 standalone V1 planches for Conseil (page Jeu)."""
import pathlib, sys

SP = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1])
SANS = (SP / "fonts/sans.b64").read_text()
MONO = (SP / "fonts/mono.b64").read_text()

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

# ---------------------------------------------------------------- chrome
BASE_CSS = """
@font-face{font-family:"CSans";src:url(data:font/woff2;base64,__SANS__) format("woff2");font-weight:100 800;font-stretch:75% 100%}
@font-face{font-family:"CMono";src:url(data:font/woff2;base64,__MONO__) format("woff2");font-weight:100 700}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:#d8d6d1;font-family:"CSans",system-ui,sans-serif;color:#1d1d1b;overflow:auto}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
input[type=radio]{position:absolute;opacity:0;pointer-events:none}
.stage{width:1440px;height:900px;transform-origin:0 0;position:relative;background:#e7e5e0;overflow:hidden}
.boardhead{position:absolute;left:44px;top:30px;right:44px;display:flex;justify-content:space-between;align-items:flex-start;gap:40px}
.boardhead .k{font:500 12px/1.4 "CMono",monospace;letter-spacing:.06em;text-transform:uppercase;color:#6b6862}
.boardhead h2{font-weight:800;font-stretch:80%;font-size:40px;line-height:1;margin-top:6px;letter-spacing:-.01em}
.boardhead p{max-width:720px;font-size:13px;line-height:1.5;color:#3d3b37}
.frames{position:absolute;left:44px;top:132px;display:flex;gap:40px;align-items:flex-start}
.fw{position:relative}
.fw .cap{position:absolute;left:0;top:-22px;font:500 11px/1 "CMono",monospace;letter-spacing:.05em;color:#6b6862;text-transform:uppercase;white-space:nowrap}
.dwrap{width:1018px;height:636px;border-radius:10px;overflow:hidden;box-shadow:0 1px 0 rgba(0,0,0,.08),0 18px 40px -18px rgba(0,0,0,.35)}
.mwrap{width:294px;height:636px;border-radius:30px;overflow:hidden;box-shadow:0 0 0 8px #1d1d1b,0 18px 40px -18px rgba(0,0,0,.45);margin-top:0}
.desk{width:1440px;height:900px;transform:scale(.7069);transform-origin:0 0;background:#f4f4f2;position:relative}
.mob{width:390px;height:844px;transform:scale(.7536);transform-origin:0 0;background:#fff;position:relative;overflow:hidden}
/* neutral host chrome: deliberately grey, no third-party marks */
.gbar{background:#d9d9d6;border-radius:6px;display:inline-block;height:10px}
.d-top{height:56px;background:#fff;border-bottom:1px solid #e2e2df;display:flex;align-items:center;padding:0 20px;gap:16px}
.d-top .mark{width:30px;height:30px;border-radius:8px;background:#cfcfcb}
.d-top .search{margin-left:180px;width:560px;height:38px;border-radius:19px;background:#efefec}
.d-top .dots{margin-left:auto;display:flex;gap:10px}.d-top .dots i{width:30px;height:30px;border-radius:50%;background:#e2e2df;display:block}
.d-rail{position:absolute;left:0;top:56px;bottom:0;width:240px;border-right:1px solid #e2e2df;padding:24px 20px;display:flex;flex-direction:column;gap:18px}
.d-side{position:absolute;left:1092px;top:80px;width:310px;height:300px;border-radius:12px;background:#fff;border:1px solid #e6e6e3;padding:18px;display:flex;flex-direction:column;gap:12px}
.d-post{position:absolute;left:300px;top:72px;width:760px;background:#fff;border:1px solid #e6e6e3;border-radius:14px;padding:14px 10px 6px}
.ph{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#64625d;padding:0 8px}
.ph .av{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-weight:800;font-stretch:75%;font-size:13px;color:#fff;background:#1f3a5f}
.ph b{color:#1d1d1b;font-weight:600}
.pt{font-size:19px;font-weight:650;line-height:1.25;padding:6px 8px 10px;color:#1d1d1b}
.pa{display:flex;gap:8px;padding:8px 6px 4px}
.pa span{height:32px;border-radius:16px;background:#f1f1ee;display:flex;align-items:center;gap:8px;padding:0 14px;font-size:12.5px;font-weight:600;color:#4a4844}
.pa svg{width:14px;height:14px}
.game-d{width:740px;height:600px;border-radius:10px;overflow:hidden;position:relative}
.m-status{height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;font-weight:650;font-size:15px}
.m-status i{display:inline-block;width:62px;height:11px;border-radius:4px;background:#1d1d1b}
.m-app{height:46px;display:flex;align-items:center;gap:12px;padding:0 14px;border-bottom:1px solid #ececea}
.m-app .mark{width:26px;height:26px;border-radius:7px;background:#cfcfcb}
.m-app .search{flex:1;height:32px;border-radius:16px;background:#efefec}
.m-post{padding:10px 0 0}
.m-post .pt{font-size:15.5px;padding:4px 12px 8px}
.m-post .ph{padding:0 12px;font-size:12px}
.game-m{width:390px;height:624px;position:relative;overflow:hidden}
.m-post .pa{padding:6px 10px}
.m-post .pa span{height:28px;font-size:11.5px;padding:0 11px}
.next{border-top:8px solid #f1f1ee;padding:12px;display:flex;flex-direction:column;gap:8px}
"""

ICON_UP = '<svg viewBox="0 0 14 14"><path d="M7 2 2.5 7.5H5.5V12h3V7.5h3z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'
ICON_DOWN = '<svg viewBox="0 0 14 14" style="transform:rotate(180deg)"><path d="M7 2 2.5 7.5H5.5V12h3V7.5h3z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'
ICON_BUBBLE = '<svg viewBox="0 0 14 14"><path d="M2 3.5h10v6H6l-3 2.5v-2.5H2z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'

POST_TITLE = f"Council session #{SESSION}: the empty lot on Alder Street"


def actions():
    return (f'<div class="pa"><span>{ICON_UP} 214 {ICON_DOWN}</span>'
            f'<span>{ICON_BUBBLE} 38</span><span>Share</span></div>')


def desktop(game):
    rail = "".join(f'<span class="gbar" style="width:{w}px"></span>' for w in (120, 96, 140, 0, 80, 130, 110, 90))
    side = "".join(f'<span class="gbar" style="width:{w}px"></span>' for w in (150, 260, 240, 200, 0, 120, 230))
    return f'''<div class="desk">
<div class="d-top"><span class="mark"></span><span class="gbar" style="width:70px"></span><span class="search"></span><span class="dots"><i></i><i></i><i></i></span></div>
<div class="d-rail">{rail}</div>
<div class="d-post"><div class="ph"><span class="av">C</span><b>r/conseil_daily</b><span>· 3 h</span></div>
<div class="pt">{POST_TITLE}</div>
<div class="game-d">{game}</div>{actions()}</div>
<div class="d-side">{side}</div></div>'''


def mobile(game):
    nxt = "".join(f'<span class="gbar" style="width:{w}px"></span>' for w in (120, 300, 260))
    return f'''<div class="mob">
<div class="m-status"><span>9:41</span><i></i></div>
<div class="m-app"><span class="mark"></span><span class="search"></span></div>
<div class="m-post"><div class="ph"><span class="av">C</span><b>r/conseil_daily</b><span>· 3 h</span></div>
<div class="pt">{POST_TITLE}</div>
<div class="game-m">{game}</div>{actions()}</div>
<div class="next">{nxt}</div></div>'''


def page(num, slug, title, pitch, css, game_fn):
    html = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conseil · Jeu · {num} {title}</title>
<style>{BASE_CSS.replace("__SANS__", SANS).replace("__MONO__", MONO)}
{css}</style></head>
<body><div class="stage" id="stage">
<div class="boardhead"><div><div class="k">Conseil · page Jeu · V1 · direction {num}/03</div><h2>{title}</h2></div><p>{pitch}</p></div>
<div class="frames">
<div class="fw"><div class="cap">Desktop 1440 × 900 · état : motion B choisie, vote prêt</div><div class="dwrap">{desktop(game_fn("d", "B"))}</div></div>
<div class="fw"><div class="cap">Mobile 390 × 844 · état : aucune motion</div><div class="mwrap">{mobile(game_fn("m", None))}</div></div>
</div></div>
<script>
// fit the 1440x900 board to the window; motions are clickable (CSS :checked)
(function(){{var s=document.getElementById("stage");function f(){{var k=Math.min(innerWidth/1440,innerHeight/900);s.style.transform="scale("+k+")";document.body.style.height=900*k+"px"}}addEventListener("resize",f);f()}})();
</script></body></html>'''
    (OUT / f"{num}-{slug}.html").write_text(html)


def motions_inputs(dev, sel, cls="mo"):
    out = []
    for letter, t, d in MOTIONS:
        chk = " checked" if sel == letter else ""
        out.append(f'<label class="{cls}"><input type="radio" name="m{dev}" value="{letter}"{chk}>'
                   f'<span class="ml">{letter}</span><span class="mt">{t}</span><span class="md">{d}</span></label>')
    return "".join(out)


def tally(n, cls="tally"):
    # tally marks: groups of five, the council-clerk way
    marks, x = [], 0
    for i in range(n):
        if i and i % 5 == 4:
            marks.append(f'<path d="M{x - 17} 13 L{x + 1} 2"/>')
            continue
        marks.append(f'<path d="M{x + .8} 1.5 V13.5"/>'); x += 5
        if i % 5 == 4: x += 4
    w = x + 6
    return f'<svg class="{cls}" viewBox="-1 0 {w} 15" width="{w}" height="15">{"".join(marks)}</svg>'


def tally6():
    # 5 strokes + crossbar, then 1 stroke
    p = "".join(f'<path d="M{1 + i * 4.6} 2 V14"/>' for i in range(4))
    p += '<path d="M-1 12 L18 3"/><path d="M25 2 V14"/>'
    return f'<svg class="tally" viewBox="-2 0 30 16" width="30" height="16">{p}</svg>'


# ---------------------------------------------------------------- 01 Paperboard
CSS1 = """
.p1{--kraft:#d9c7a7;--navy:#1f3a5f;--orange:#e07a3f;--paper:#f7f1e3;width:100%;height:100%;background:var(--kraft);color:var(--navy);position:relative;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .12  0 0 0 .22 0'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>")}
.p1 .bar{display:flex;justify-content:space-between;align-items:center;font:500 11.5px/1 "CMono",monospace;letter-spacing:.06em;text-transform:uppercase}
.p1 .streak{display:flex;align-items:center;gap:8px}
.p1 .tally{stroke:var(--navy);stroke-width:1.7;fill:none;stroke-linecap:round}
.p1 h1{font-weight:800;font-stretch:75%;text-transform:uppercase;line-height:.9;letter-spacing:-.005em}
.p1 .rule{font-size:14px;line-height:1.35;font-weight:500}
.p1 .rule b{font-weight:750}
.p1 .notes{display:grid;grid-template-columns:repeat(3,1fr)}
.p1 .note{background:var(--paper);position:relative;box-shadow:0 1px 0 rgba(60,40,10,.18),0 6px 10px -6px rgba(60,40,10,.45);display:flex;flex-direction:column;justify-content:space-between}
.p1 .note:nth-child(1){transform:rotate(-1.4deg)}.p1 .note:nth-child(2){transform:rotate(.8deg)}.p1 .note:nth-child(3){transform:rotate(-.5deg)}
.p1 .note:nth-child(4){transform:rotate(1.1deg)}.p1 .note:nth-child(5){transform:rotate(-.9deg)}.p1 .note:nth-child(6){transform:rotate(.4deg)}
.p1 .pin{position:absolute;left:50%;top:-6px;width:13px;height:13px;margin-left:-6.5px;border-radius:50%;background:var(--orange);box-shadow:inset -2px -2px 0 rgba(0,0,0,.18),0 2px 2px rgba(40,20,0,.35)}
.p1 .q{font-weight:500;line-height:1.28}
.p1 .who{font:500 10.5px/1.2 "CMono",monospace;letter-spacing:.03em;text-transform:uppercase;opacity:.8}
.p1 .who b{font-family:"CSans";font-weight:800;font-stretch:80%;font-size:1.25em;letter-spacing:0;opacity:1;margin-right:4px}
.p1 .motions{display:grid}
.p1 .mo{position:relative;border:2px solid var(--navy);background:rgba(247,241,227,.55);display:grid;grid-template-columns:auto 1fr;column-gap:10px;align-content:center;cursor:pointer;transition:background .15s,transform .15s}
.p1 .mo:hover{background:var(--paper)}
.p1 .ml{grid-row:span 2;font-weight:800;font-stretch:75%;width:30px;height:30px;border:2px solid var(--navy);border-radius:50%;display:grid;place-items:center;font-size:17px;align-self:center}
.p1 .mt{font-weight:800;font-stretch:80%;text-transform:uppercase;font-size:17px;line-height:1.05}
.p1 .md{font-size:12.5px;line-height:1.3;font-weight:450}
.p1 .mo:has(input:checked){background:var(--orange);border-color:var(--navy);transform:rotate(-.6deg);box-shadow:3px 3px 0 var(--navy)}
.p1 .mo:has(input:checked) .ml{background:var(--navy);color:var(--orange)}
.p1 .foot{display:flex;align-items:center;justify-content:space-between}
.p1 .sat{font:500 11px/1.3 "CMono",monospace;letter-spacing:.04em;text-transform:uppercase}
.p1 .cta{background:var(--navy);color:var(--paper);font-weight:800;font-stretch:80%;text-transform:uppercase;letter-spacing:.02em;font-size:17px;height:46px;padding:0 26px;border-radius:3px}
.p1:not(:has(input:checked)) .cta{background:transparent;color:var(--navy);border:2px dashed rgba(31,58,95,.55)}
.p1 .cta .on{display:none}.p1:has(input:checked) .cta .on{display:inline}.p1:has(input:checked) .cta .off{display:none}
/* desktop */
.p1.d{padding:20px 26px 22px;display:flex;flex-direction:column;gap:12px}
.p1.d h1{font-size:50px;margin-top:2px}
.p1.d .notes{gap:18px 20px;margin-top:6px}
.p1.d .note{height:98px;padding:16px 14px 10px}
.p1.d .q{font-size:15px}
.p1.d .motions{grid-template-columns:repeat(3,1fr);gap:14px;margin-top:6px}
.p1.d .mo{height:92px;padding:10px 12px}
/* mobile */
.p1.m{padding:12px 14px 14px;display:flex;flex-direction:column;gap:8px}
.p1.m .bar{font-size:10px}
.p1.m h1{font-size:38px}
.p1.m .rule{font-size:12.5px}
.p1.m .notes{grid-template-columns:1fr 1fr;gap:12px 10px;margin-top:4px}
.p1.m .note{height:72px;padding:11px 9px 6px}
.p1.m .q{font-size:12.2px}
.p1.m .who{font-size:9.5px}
.p1.m .motions{gap:7px;margin-top:4px}
.p1.m .mo{padding:6px 10px;min-height:44px}
.p1.m .ml{width:26px;height:26px;font-size:15px}
.p1.m .mt{font-size:15px}.p1.m .md{font-size:11.2px}
.p1.m .cta{height:44px;width:100%;font-size:16px}
.p1.m .foot{flex-direction:column;gap:6px;align-items:stretch}.p1.m .sat{text-align:center;font-size:9.5px;order:2}
"""


def game1(dev, sel):
    notes = "".join(f'<div class="note"><i class="pin"></i><p class="q">“{q}”</p><p class="who"><b>{n}</b>{r}</p></div>'
                    for n, r, q in OPINIONS)
    title = "The empty lot<br>on Alder St." if dev == "m" else "The empty lot on Alder Street"
    rule = ("Six neighbors spoke. <b>Table the motion most of them will back.</b>" if dev == "d"
            else "<b>Table the motion most neighbors will back.</b>")
    return f'''<div class="g p1 {dev}">
<div class="bar"><span>Session {SESSION} · {DATE}</span><span class="streak">{tally6()} {STREAK}-day streak</span></div>
<h1>{title}</h1><p class="rule">{rule}</p>
<div class="notes">{notes}</div>
<div class="motions">{motions_inputs(dev, sel)}</div>
<div class="foot"><span class="sat">{SAT} neighbors have sat today · 1 vote a day</span>
<button class="cta"><span class="on">Call the vote</span><span class="off">Pick a motion</span></button></div></div>'''


# ---------------------------------------------------------------- 02 Affiche
CSS2 = """
.p2{--navy:#1f3a5f;--orange:#e07a3f;--cream:#f2ebdd;width:100%;height:100%;background:var(--cream);color:var(--navy);display:flex;flex-direction:column}
.p2 .top{background:var(--navy);color:var(--cream);position:relative}
.p2 .bar{display:flex;justify-content:space-between;align-items:center;font:500 11px/1 "CMono",monospace;letter-spacing:.08em;text-transform:uppercase;opacity:.92}
.p2 .bar .st{display:flex;align-items:baseline;gap:6px}
.p2 .bar .st b{font-family:"CSans";font-weight:800;font-stretch:75%;font-size:22px;letter-spacing:0;color:var(--orange)}
.p2 h1{font-weight:800;font-stretch:75%;text-transform:uppercase;line-height:.84;letter-spacing:-.01em}
.p2 .sub{font-weight:500;font-stretch:90%;text-transform:uppercase;letter-spacing:.14em}
.p2 .rule{font-weight:600;color:var(--navy)}
.p2 .ops{display:grid;grid-template-columns:1fr 1fr}
.p2 .op{display:grid;grid-template-columns:auto 1fr;column-gap:12px;border-top:2px solid var(--navy);align-content:start}
.p2 .n{font-weight:800;font-stretch:75%;line-height:.8;grid-row:span 2}
.p2 .q{font-weight:500;line-height:1.25}
.p2 .who{font:500 10.5px/1.3 "CMono",monospace;letter-spacing:.05em;text-transform:uppercase;opacity:.75}
.p2 .who b{font-weight:700;opacity:1}
.p2 .motions{display:grid}
.p2 .mo{border:3px solid var(--navy);display:grid;grid-template-columns:auto 1fr;column-gap:12px;align-content:center;cursor:pointer;transition:background .12s}
.p2 .mo:hover{background:#fff}
.p2 .ml{grid-row:span 2;font-weight:800;font-stretch:75%;line-height:.8;align-self:center}
.p2 .mt{font-weight:800;font-stretch:78%;text-transform:uppercase;line-height:1}
.p2 .md{line-height:1.25;font-weight:450}
.p2 .mo:has(input:checked){background:var(--orange)}
.p2 .cta{background:var(--navy);color:var(--cream);font-weight:800;font-stretch:78%;text-transform:uppercase;letter-spacing:.03em;display:flex;align-items:center;justify-content:space-between;width:100%}
.p2 .cta .arr{display:inline-block;width:28px;height:2px;background:currentColor;position:relative}
.p2 .cta .arr:after{content:"";position:absolute;right:0;top:-5px;width:10px;height:10px;border-top:2px solid currentColor;border-right:2px solid currentColor;transform:rotate(45deg);transform-origin:center;right:1px}
.p2:not(:has(input:checked)) .cta{background:transparent;color:var(--navy);box-shadow:inset 0 0 0 3px var(--navy);opacity:.5}
.p2 .cta .on{display:none}.p2:has(input:checked) .cta .on{display:inline}.p2:has(input:checked) .cta .off{display:none}
.p2 .sat{font:500 10.5px/1 "CMono",monospace;letter-spacing:.06em;text-transform:uppercase;opacity:.7}
/* desktop */
.p2.d .top{padding:18px 26px 20px}
.p2.d h1{font-size:104px;margin-top:14px}
.p2.d .sub{font-size:17px;margin-top:8px;color:var(--orange)}
.p2.d .body{padding:14px 26px 20px;display:flex;flex-direction:column;gap:12px;flex:1}
.p2.d .rule{font-size:15px}
.p2.d .ops{gap:0 26px}
.p2.d .op{padding:8px 0 9px}
.p2.d .n{font-size:30px}
.p2.d .q{font-size:15px}
.p2.d .motions{grid-template-columns:repeat(3,1fr);gap:12px}
.p2.d .mo{padding:10px 12px;height:80px}
.p2.d .ml{font-size:40px}.p2.d .mt{font-size:18px}.p2.d .md{font-size:12.5px;margin-top:3px}
.p2.d .foot{display:flex;align-items:center;gap:20px;margin-top:auto}
.p2.d .cta{height:48px;padding:0 20px;font-size:20px;flex:0 0 300px}
/* mobile */
.p2.m .top{padding:12px 14px 14px}
.p2.m .bar{font-size:9.5px}.p2.m .bar .st b{font-size:18px}
.p2.m h1{font-size:62px;margin-top:8px}
.p2.m .sub{font-size:13px;margin-top:5px;color:var(--orange)}
.p2.m .body{padding:10px 14px 12px;display:flex;flex-direction:column;gap:8px;flex:1}
.p2.m .rule{font-size:12.5px}
.p2.m .ops{gap:0 12px}
.p2.m .op{padding:6px 0 6px;column-gap:7px}
.p2.m .n{font-size:20px}
.p2.m .q{font-size:12px}
.p2.m .who{font-size:9px}
.p2.m .motions{gap:6px}
.p2.m .mo{padding:5px 10px;border-width:2.5px;min-height:42px}
.p2.m .ml{font-size:28px}.p2.m .mt{font-size:15px}.p2.m .md{font-size:11px}
.p2.m .foot{display:flex;flex-direction:column;gap:6px;margin-top:auto}
.p2.m .cta{height:44px;padding:0 16px;font-size:17px}
.p2.m .sat{text-align:center;font-size:9px}
"""


def game2(dev, sel):
    ops = "".join(f'<div class="op"><span class="n">{i + 1:02d}</span><p class="q">{q}</p><p class="who"><b>{n}</b> · {r}</p></div>'
                  for i, (n, r, q) in enumerate(OPINIONS))
    rule = ("Six neighbors spoke. Pick the motion most of them will back." if dev == "d"
            else "Pick the motion most neighbors will back.")
    return f'''<div class="g p2 {dev}">
<div class="top"><div class="bar"><span>Session {SESSION} · {DATE}</span><span class="st">Streak <b>{STREAK}</b></span></div>
<h1>The empty lot</h1><div class="sub">on Alder Street</div></div>
<div class="body"><p class="rule">{rule}</p><div class="ops">{ops}</div>
<div class="motions">{motions_inputs(dev, sel)}</div>
<div class="foot"><button class="cta"><span class="on">Call the vote</span><span class="off">Pick a motion</span><i class="arr"></i></button>
<span class="sat">{SAT} neighbors have sat today · 1 vote a day</span></div></div></div>'''


# ---------------------------------------------------------------- 03 Minutes
CSS3 = """
.p3{--ink:#161615;--paper:#fbfaf6;--rule:#dedbd2;--green:#1f6b4f;--mute:#77746c;width:100%;height:100%;background:var(--paper);color:var(--ink);display:flex}
.p3 .meta{font:500 11px/1.2 "CMono",monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--mute)}
.p3 .meta b{color:var(--ink);font-weight:700}
.p3 h1{font-weight:650;letter-spacing:-.025em;line-height:.9;text-transform:lowercase}
.p3 .rule{font-weight:350;line-height:1.35}
.p3 .rule b{font-weight:600}
.p3 .table{display:block}
.p3 .table .t{fill:none;stroke:var(--ink);stroke-width:1.2}
.p3 .table .seat circle{fill:var(--paper);stroke:var(--ink);stroke-width:1.2}
.p3 .table .seat text{font:700 11px "CMono",monospace;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
.p3 .table .you circle{fill:var(--ink)}.p3 .table .you text{fill:var(--paper);font-size:8.5px}
.p3 .table .lbl{font:500 8.5px "CMono",monospace;letter-spacing:.06em;fill:var(--mute);text-anchor:middle}
.p3 .mins{list-style:none}
.p3 .mins li{display:grid;grid-template-columns:auto 1fr;column-gap:10px;border-top:1px solid var(--rule);align-items:start}
.p3 .ini{font:700 10.5px/1 "CMono",monospace;width:22px;height:22px;border:1.2px solid var(--ink);border-radius:50%;display:grid;place-items:center}
.p3 .q{font-weight:350;line-height:1.3}
.p3 .q b{font-weight:650;margin-right:6px}
.p3 .q .r{font:500 10px "CMono",monospace;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);margin-right:8px}
.p3 .mhead{font:700 11px/1 "CMono",monospace;letter-spacing:.12em;text-transform:uppercase}
.p3 .mo{display:grid;grid-template-columns:auto 1fr;column-gap:12px;border-top:1px solid var(--rule);cursor:pointer;align-items:center}
.p3 .mo:last-child{border-bottom:1px solid var(--rule)}
.p3 .ml{grid-row:span 2;width:18px;height:18px;border-radius:50%;border:1.4px solid var(--ink);font-size:0;position:relative;transition:background .12s}
.p3 .mt{font-weight:600;line-height:1.15}
.p3 .mt:before{content:attr(data-l);font:500 10.5px "CMono",monospace;color:var(--mute);margin-right:8px;letter-spacing:.04em}
.p3 .md{font-weight:350;color:#4b4943;line-height:1.3}
.p3 .mo:hover .ml{box-shadow:inset 0 0 0 3px var(--paper),inset 0 0 0 9px var(--rule)}
.p3 .mo:has(input:checked) .ml{background:var(--green);border-color:var(--green);box-shadow:inset 0 0 0 3.5px var(--paper),inset 0 0 0 9px var(--green)}
.p3 .mo:has(input:checked) .mt{color:var(--green)}
.p3 .cta{height:44px;border-radius:22px;border:1.4px solid var(--ink);padding:0 22px;font-weight:600;display:inline-flex;align-items:center;gap:10px;font-size:15px}
.p3:has(input:checked) .cta{background:var(--green);border-color:var(--green);color:var(--paper)}
.p3:not(:has(input:checked)) .cta{color:var(--mute);border-color:var(--rule)}
.p3 .cta .on{display:none}.p3:has(input:checked) .cta .on{display:inline}.p3:has(input:checked) .cta .off{display:none}
/* desktop */
.p3.d{padding:22px 26px 22px;gap:28px}
.p3.d .left{width:220px;display:flex;flex-direction:column;justify-content:space-between}
.p3.d .right{flex:1;display:flex;flex-direction:column;gap:10px;min-width:0}
.p3.d h1{font-size:54px;margin-top:14px}
.p3.d .rule{font-size:15px;margin-top:12px}
.p3.d .mins li{padding:7px 0}
.p3.d .q{font-size:14.5px}
.p3.d .mo{padding:8px 0}
.p3.d .mt{font-size:15.5px}.p3.d .md{font-size:13px}
.p3.d .foot{display:flex;align-items:center;justify-content:space-between;margin-top:auto}
/* mobile */
.p3.m{flex-direction:column;padding:12px 14px 12px;gap:7px}
.p3.m .meta{font-size:9.5px}
.p3.m .hrow{display:flex;justify-content:space-between;align-items:flex-end;gap:8px}
.p3.m h1{font-size:34px}
.p3.m .rule{font-size:12.5px}
.p3.m .mins li{padding:4px 0;column-gap:8px}
.p3.m .ini{width:19px;height:19px;font-size:9px}
.p3.m .q{font-size:12px}
.p3.m .q .r{display:none}
.p3.m .mhead{font-size:9.5px;margin-top:3px}
.p3.m .mo{padding:5px 0;column-gap:10px}
.p3.m .ml{width:16px;height:16px}
.p3.m .mt{font-size:13.5px}.p3.m .md{font-size:11px}
.p3.m .foot{display:flex;align-items:center;justify-content:space-between;margin-top:auto}
.p3.m .cta{height:42px;font-size:14px;padding:0 18px}
"""


def table_svg(w, h):
    # oval table, six seats around, the player in the chair at the bottom
    cx, cy, rx, ry = w / 2, h / 2 - 6, w / 2 - 30, h / 2 - 34
    import math
    seats = []
    angs = [-150, -90, -30, 30, 150, 210]  # leave 90 deg (bottom) for the chair
    angs = [-140, -90, -40, 20, 160, 200]
    for (n, _, _), a in zip(OPINIONS, [-150, -90, -30, 25, 155, 205]):
        x = cx + (rx + 16) * math.cos(math.radians(a)); y = cy + (ry + 16) * math.sin(math.radians(a))
        seats.append(f'<g class="seat"><circle cx="{x:.1f}" cy="{y:.1f}" r="12"/><text x="{x:.1f}" y="{y:.1f}">{n[0]}</text></g>')
    yx, yy = cx, cy + ry + 16
    seats.append(f'<g class="seat you"><circle cx="{yx}" cy="{yy}" r="13"/><text x="{yx}" y="{yy}">YOU</text></g>')
    return (f'<svg class="table" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><ellipse class="t" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>'
            f'<text class="lbl" x="{cx}" y="{cy + 3}">ALDER ST. LOT</text>{"".join(seats)}</svg>')


def game3(dev, sel):
    mins = "".join(f'<li><span class="ini">{n[0]}</span><p class="q"><b>{n}</b><span class="r">{r}</span>{q}</p></li>'
                   for n, r, q in OPINIONS)
    mos = "".join(f'<label class="mo"><input type="radio" name="m{dev}" value="{l}"{" checked" if sel == l else ""}>'
                  f'<span class="ml"></span><span class="mt" data-l="motion {l.lower()}.">{t.lower()}</span><span class="md">{d}</span></label>'
                  for l, t, d in MOTIONS)
    cta = '<button class="cta"><span class="on">call the vote</span><span class="off">pick a motion</span> →</button>'
    if dev == "d":
        return f'''<div class="g p3 d"><div class="left"><div><p class="meta"><b>session {SESSION}</b><br>{DATE} · 19:00<br>alder st. hall</p>
<h1>the empty lot on alder street.</h1><p class="rule">Six neighbors spoke. <b>Table the motion most of them will back.</b></p></div>
<div>{table_svg(220, 170)}<p class="meta" style="margin-top:10px"><b>{STREAK}-day</b> streak · {SAT} sat today</p></div></div>
<div class="right"><p class="mhead">minutes</p><ul class="mins">{mins}</ul><p class="mhead" style="margin-top:6px">on the table</p><div>{mos}</div>
<div class="foot"><span class="meta">1 vote a day · same agenda for everyone</span>{cta}</div></div></div>'''
    return f'''<div class="g p3 m"><div class="hrow"><p class="meta"><b>session {SESSION}</b> · {DATE}</p><p class="meta"><b>{STREAK}-day</b> streak</p></div>
<h1>the empty lot on alder street.</h1><p class="rule"><b>Table the motion most neighbors will back.</b></p>
<ul class="mins">{mins}</ul><p class="mhead">on the table</p><div>{mos}</div>
<div class="foot"><span class="meta">{SAT} sat today</span>{cta}</div></div>'''


page("01", "paperboard", "Paperboard",
     "La direction du brief, poussée. Le tableau de liège d'une salle de quartier : six avis punaisés sur du kraft, titres condensés marine, l’orange réservé à la motion choisie. Chaleureux et un peu de travers, comme une vraie réunion.",
     CSS1, game1)
page("02", "affiche", "Affiche",
     "Inspirée de Teko : le titre du jour occupe toute la largeur, comme une affiche de réunion collée au mur. Aplats francs marine / crème / orange, sans texture ni rotation, avis numérotés 01–06 séparés par des filets. Se lit de loin, en une seconde.",
     CSS2, game2)
page("03", "proces-verbal", "Procès-verbal",
     "S'écarte du brief : fond clair, mono pour la méta, titre en minuscules serré (principes de Concept Studio). Les six voisins sont assis autour d'une table et le joueur est à la place du président. Les avis sont écrits comme un compte rendu. Un seul accent, vert d'encre civique, à la place du kraft et de l’orange.",
     CSS3, game3)
print("ok")
