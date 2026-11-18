"""Conseil — remaining pages in the validated V4 style (Post, Carte de fin, Séries).

Usage: python3 G-DESIGN/_src/gen5.py G-DESIGN/planches/v4
Demo data below rests on assumptions listed in PAGES.md (3 motions, score x/6,
one vote a day, recurring cast).
"""
import json, pathlib, sys

SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))
import gen3 as g   # noqa: E402
import gen4 as q   # noqa: E402

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
INK, OR, CREAM = q.INK, q.OR, q.CREAM
TINT = g.TINT
NAME = {c[0]: c[1] for c in g.CAST}

# --- demo outcome of session 47 (player picked B)
YES = ["theo", "sam", "kofi"]
WHY = {"ines": "Racks on my lane? No.", "theo": "Finally, a place to play.", "ruth": "Lit till 11? Not again.",
       "sam": "Racks! Yes.", "odile": "Still no plots.", "kofi": "No levy. Fine."}
SPLIT = [("A", "Community garden", 26), ("B", "Play court & racks", 33), ("C", "Shared lot", 41)]
HISTORY = [(41, "Thu 12", "Bins on Elm Row", 4), (42, "Fri 13", "The bus shelter", 5), (43, "Sat 14", "Market day noise", 3),
           (44, "Sun 15", "Speed bumps", 5), (45, "Mon 16", "Who waters the planters", 4), (46, "Tue 17", "Holiday lights budget", 2),
           (47, "Wed 18", "The empty lot", 3)]
AGREED = {"ines": 4, "theo": 6, "ruth": 2, "sam": 5, "odile": 3, "kofi": 5}

EXTRA = f"""
.q .big{{font-weight:900;letter-spacing:-.04em;line-height:.85}}
.q .stk{{background:#fff;border-radius:18px;box-shadow:0 0 0 5px #fff,0 4px 10px rgba(0,0,0,.18);position:absolute}}
.q .k{{font:500 10px/1.2 "DM Mono",monospace;letter-spacing:.07em;text-transform:uppercase;opacity:.65}}
.q .yn{{position:absolute;left:0;top:0;background:#fff;border-radius:12px;padding:5px 9px 6px;font-size:12px;font-weight:650;line-height:1.2;white-space:nowrap;
  box-shadow:0 0 0 1.6px var(--ink),0 3px 0 1.6px var(--ink)}}
.q .yn b{{display:inline-block;font-weight:900;font-size:11px;letter-spacing:.06em;text-transform:uppercase;padding:2px 6px;border-radius:6px;margin-right:6px}}
.q .yn.y b{{background:var(--or);color:#fff}} .q .yn.n b{{background:var(--ink);color:#fff}}
.q .yn:after{{content:"";position:absolute;left:50%;bottom:-6px;margin-left:-5px;width:10px;height:10px;background:#fff;box-shadow:1.6px 1.6px 0 0 var(--ink);transform:rotate(45deg)}}
.q .dots{{position:absolute;left:0;top:0;background:#fff;border-radius:12px;padding:6px 10px;font-weight:900;letter-spacing:.12em;box-shadow:0 0 0 1.6px var(--ink),0 3px 0 1.6px var(--ink)}}
.q .bar{{height:12px;border-radius:6px;background:#e9e2d2;overflow:hidden}}
.q .bar i{{display:block;height:100%;border-radius:6px;background:var(--ink)}}
.q .bar.me i{{background:var(--or)}}
"""


def opts_script(o):
    return f"<script>window.CONSEIL_OPTS={json.dumps(o)};</script>"


def write(fname, title, ui, opts, kit_html):
    base = g.BASE.replace("__ARCHIVO__", g.F["archivo"]).replace("__DM4__", g.F["dmmono-400"]).replace("__DM5__", g.F["dmmono-500"])
    cast = json.dumps([{"id": c[0], "acc": c[4]} for c in g.CAST])
    js = q.JS.replace("__CAST__", cast).replace("__TINT__", json.dumps(TINT))
    game = f'<div class="q" id="q"><canvas id="cv" width="740" height="640"></canvas><div class="ui">{ui}<p class="nogl">3D indisponible dans ce navigateur (WebGL désactivé).</p></div></div>'
    (OUT / fname).write_text(f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conseil · {title}</title>
<style>{base}{q.CSS}{EXTRA}</style></head>
<body><div class="sheet" id="sheet">{g.chrome(game)}{kit_html}</div>
{opts_script(opts)}
<script type="text/plain" id="three-src">{q.THREE}</script>
<script type="module">{js}</script>
<script>(function(){{var s=document.getElementById("sheet");function f(){{var k=Math.min(1,innerWidth/1440);s.style.transform="scale("+k+")";document.body.style.height=s.offsetHeight*k+"px"}}addEventListener("resize",f);f()}})();</script>
</body></html>''')


def pagekit(num, title, why, cells):
    return g.kit(num, title, why, cells).replace(f"V3 · direction {num}/03", f"V4 · page {num}/04")


# =============================================================== 02 POST (in the feed, not played yet)
def post():
    dots = "".join(f'<span class="dots" data-i="{i}" data-side="t">…</span>' for i in range(6))
    ui = f'''<div class="meta"><span>Session {g.SESSION} · {g.DATE}</span><span><b>{g.STREAK}-day streak</b></span></div>
<h1>Tonight: <span class="sel">the empty lot{q.handles()}</span></h1>
<p class="rule">Six neighbors are waiting for the chair. <b>One lot, three motions, one vote.</b></p>
<span class="tag" id="lottag">The lot, today</span>{dots}
<div class="stk" style="left:50%;bottom:30px;transform:translateX(-50%) rotate(-1deg);padding:16px 18px 16px 22px;display:flex;align-items:center;gap:22px;width:560px">
 <div style="flex:1"><p class="k">Today's session</p><p style="font-weight:850;font-size:17px;letter-spacing:-.01em;margin-top:3px">Read six neighbors. Table one motion.</p>
 <p style="font-size:12.5px;margin-top:3px">{g.SAT} neighbors have voted · takes about a minute</p></div>
 <button class="cta" style="flex:none">Take the chair</button></div>'''
    opts = {"mode": "post", "cam": [12.0, 8.4], "target": [0, .1, -.25]}
    kit = pagekit("02", "Post",
                  "Ce qu'on voit en scrollant le feed, avant de jouer. La scène est vivante, le terrain encore en friche, et chaque voisin a <b>quelque chose à dire</b> (« … ») sans le dévoiler. "
                  "Une seule action : <b>Take the chair</b>. La série du joueur est rappelée en haut pour donner une raison de ne pas la casser.",
                  [("États", '<p class="note"><b>Pas encore joué</b> (cette planche) : bulles « … », bouton actif.<br><b>Déjà joué aujourd’hui</b> : le terrain montre la motion du joueur, le bouton devient « See the result », et la série est à jour.</p>'),
                   ("Ce qui accroche", '<p class="note">Le titre du jour en très grand, les six silhouettes reconnaissables d’un jour à l’autre (casting récurrent, question 5 de PAGES.md), et la preuve sociale (« 1,284 neighbors have voted ») collée au bouton.</p>'),
                   ("Mouvement", '<p class="note">Caméra qui respire, voisins qui respirent. Au clic sur « Take the chair », les bulles « … » s’ouvrent sur les vraies citations (transition vers la page Jeu).</p>'),
                   ("Interdits", '<p class="note">Aucun spoiler sur le score ou la meilleure motion. Pas de thème Reddit (pas de karma, pas de mascotte).</p>')])
    write("02-post.html", "Post V4", ui, opts, kit)


# =============================================================== 03 END CARD
def endcard():
    yn = "".join(f'<span class="yn {"y" if cid in YES else "n"}" data-i="{i}" data-side="t"><b>{"Yes" if cid in YES else "No"}</b>{WHY[cid]}</span>'
                 for i, (cid, *_r) in enumerate(g.CAST))
    split = "".join(f'''<div style="display:grid;grid-template-columns:18px 1fr 34px;gap:8px;align-items:center;margin-top:7px">
<b style="font-weight:900;font-size:13px">{l}</b><div class="bar{' me' if l == g.SEL else ''}"><i style="width:{pct}%"></i></div><span style="font:500 11px DM Mono">{pct}%</span></div>''' for l, t, pct in SPLIT)
    pips = "".join(f'<i style="display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:4px;background:{TINT[c] if c in YES else "#fff"};box-shadow:0 0 0 1.5px {INK}"></i>' for c, *_ in g.CAST)
    ui = f'''<div class="meta"><span>Session {g.SESSION} · result</span><span><b>7-day streak</b></span></div>
{yn}
<div class="stk" style="right:26px;top:58px;width:268px;padding:18px 20px 18px;transform:rotate(1deg)">
 <p class="k">You tabled · B · Play court &amp; racks</p>
 <p class="big" style="font-size:92px;margin-top:8px">3<span style="font-size:48px">/6</span></p>
 <p style="font-weight:800;font-size:15px;margin-top:2px">neighbors backed you</p>
 <p style="margin-top:8px">{pips}</p>
 <p style="font-size:12.5px;line-height:1.35;margin-top:10px">Best motion today: <b>C · Shared lot</b>, backed by <b>5/6</b>.</p>
 <div style="margin-top:12px;border-top:1.5px dashed rgba(0,0,0,.2);padding-top:10px"><p class="k">What {g.SAT} neighbors tabled</p>{split}</div>
</div>
<div class="stk" style="left:28px;right:26px;bottom:24px;padding:14px 16px 14px 20px;display:flex;align-items:center;gap:16px;transform:rotate(-.6deg)">
 <div style="flex:1"><p style="font-weight:850;font-size:16px">Ruth said no. Make your case.</p><p style="font-size:12.5px;margin-top:2px">Your reply goes to the comments, signed with your 3/6.</p></div>
 <span class="k" style="opacity:.8">Next session in 14 h 22 min</span>
 <button class="cta" style="flex:none">Comment</button></div>'''
    opts = {"mode": "result", "current": "B", "yes": YES, "cam": [12.6, 9.2], "target": [1.75, .15, -.2]}
    kit = pagekit("03", "Carte de fin",
                  "Le résultat se lit <b>dans la scène</b> : ceux qui soutiennent la motion lèvent le bras, les autres tournent le dos, et chacun dit en une ligne pourquoi. "
                  "Le score est un gros sticker (<b>3/6</b>), suivi de la meilleure motion du jour et de ce qu'a choisi le quartier. On termine par une <b>accroche à commentaire</b> qui nomme un voisin qui a dit non.",
                  [("Lecture en 5 s", '<p class="note">1. Bras levés contre dos tournés. 2. Le gros 3/6. 3. La meilleure motion. 4. La répartition du quartier, la barre du joueur en orange.</p>'),
                   ("Accroche commentaire", '<p class="note">Le bouton cite un voisin qui a dit non (« Ruth said no ») : on a une raison d’écrire, et le commentaire porte le score.</p>'),
                   ("Retour quotidien", '<p class="note">La série passe à 7 et le compte à rebours de la prochaine séance s’affiche. Une seule partie par jour.</p>'),
                   ("Hypothèses", '<p class="note">Score = nombre de voisins sur 6 qui votent pour, et le maximum du jour peut être inférieur à 6 (questions 2 et 3 de PAGES.md). « Signed with your 3/6 » suppose qu’on peut poster le commentaire depuis le jeu.</p>')])
    write("03-carte-de-fin.html", "Carte de fin V4", ui, opts, kit)


# =============================================================== 04 STREAKS & COMMUNITY
def series():
    tags = "".join(f'<span class="yn y" data-i="{i}" data-side="t" style="text-align:center"><b style="margin:0">{AGREED[cid]}/7</b></span>' for i, (cid, *_r) in enumerate(g.CAST))
    days = ""
    for n, d, topic, sc in HISTORY:
        today = n == g.SESSION
        days += (f'<div style="display:grid;grid-template-columns:96px 1fr 92px;align-items:center;gap:10px;padding:6px 0;border-top:1px solid rgba(0,0,0,.08)">'
                 f'<span class="k" style="opacity:{1 if today else .6}">#{n} · {d}</span><span style="font-size:13px;font-weight:{800 if today else 550}">{topic}</span>'
                 f'<span style="display:flex;gap:3px;justify-content:flex-end">' + "".join(f'<i style="width:9px;height:9px;border-radius:50%;background:{(OR if today else INK) if k < sc else "transparent"};box-shadow:0 0 0 1.3px {INK}"></i>' for k in range(6)) + "</span></div>")
    ui = f'''<div class="meta"><span>Your council record</span><span><b>Session {g.SESSION}</b></span></div>
<h1 style="text-align:left;left:28px;top:40px">The <span class="sel">regulars{q.handles()}</span></h1>
<p class="rule" style="text-align:left;left:30px;top:94px">How often each neighbor backed your motion, last 7 sessions.</p>
{tags}
<div class="stk" style="left:28px;bottom:24px;width:236px;padding:16px 18px;transform:rotate(-1deg)">
 <p class="k">Streak</p><p class="big" style="font-size:80px;margin-top:6px">7</p><p style="font-weight:800;font-size:14px">days in the chair</p>
 <p style="font-size:12.5px;margin-top:6px">Record: <b>12</b> · Average <b>3.7/6</b></p>
 <p style="font-size:12.5px;margin-top:2px">Neighborhood average <b>3.4/6</b></p></div>
<div class="stk" style="right:26px;bottom:24px;width:418px;padding:14px 18px 10px;transform:rotate(.6deg)">
 <p class="k" style="margin-bottom:4px">Last 7 sessions</p>{days}</div>'''
    spots = [[-2.75, -.15], [-1.65, -.15], [-.55, -.15], [.55, -.15], [1.65, -.15], [2.75, -.15]]
    opts = {"mode": "series", "noLot": True, "spots": spots, "cam": [15.5, 5.2], "target": [0, -.95, 0]}
    kit = pagekit("04", "Séries & classement",
                  "La couche communautaire. En haut, les <b>habitués</b> : les six voisins en rang, chacun avec le nombre de fois qu'il a soutenu le joueur sur les 7 dernières séances (le casting récurrent devient un fil personnel). "
                  "En bas, la <b>série</b> en très grand et les <b>7 dernières séances</b>, chacune avec son score en pastilles.",
                  [("Ce qu’on compare", '<p class="note">Le joueur face à lui-même (série, record, moyenne) et face au quartier (moyenne du quartier). Il n’y a pas de classement nominatif entre joueurs tant que la question 4 de PAGES.md n’est pas tranchée.</p>'),
                   ("Pastilles de score", '<p class="note">Six pastilles par séance, pleines jusqu’au score ; aujourd’hui en orange, les jours passés en encre.</p>'),
                   ("Les habitués", '<p class="note">Une étiquette « x/7 » au-dessus de chaque figurine. Cela n’a de sens que si le casting est récurrent (question 5). Avec un casting tournant, on remplacerait ce bloc par la répartition des choix du jour.</p>'),
                   ("Données de démo", '<p class="note">Sujets #41–#46 inventés pour la planche (poubelles, abribus, marché, ralentisseurs, jardinières, illuminations).</p>')])
    write("04-series.html", "Séries V4", ui, opts, kit)


post()
endcard()
series()
print("ok")
