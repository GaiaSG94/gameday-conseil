"""Conseil — V4: Foule + Stickers merged, in real-time 3D (Three.js, embedded).

Usage: python3 G-DESIGN/_src/gen4.py G-DESIGN/planches/v4
Three.js 0.170.0 (MIT) is inlined from _src/vendor so the planche opens offline.
"""
import json, pathlib, sys

SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))
import gen3 as g  # noqa: E402  (cast, fonts, host chrome)

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
THREE = (SRC / "vendor/three-0.170.0.module.min.js").read_text()

CREAM, INK, OR = "#f3eee2", "#151515", "#ff5a1f"
TINT = g.TINT

CSS = f"""
.q{{--cream:{CREAM};--ink:{INK};--or:{OR};width:100%;height:100%;position:relative;background:var(--cream);color:var(--ink);overflow:hidden}}
.q:before{{content:"";position:absolute;inset:0;background:url("{g.GRAIN3}");mix-blend-mode:multiply;pointer-events:none}}
.q canvas{{position:absolute;inset:0;width:740px;height:640px;display:block}}
.q .ui{{position:absolute;inset:0;pointer-events:none}}
.q .ui *{{pointer-events:auto}}
.q .meta{{position:absolute;left:28px;top:22px;right:28px;display:flex;justify-content:space-between;font:500 11px/1 "DM Mono",monospace;letter-spacing:.06em;text-transform:uppercase}}
.q .meta b{{font-weight:500;background:var(--ink);color:var(--cream);padding:4px 7px;border-radius:3px}}
.q h1{{position:absolute;left:0;right:0;top:40px;text-align:center;font-weight:900;font-size:50px;line-height:.92;letter-spacing:-.03em;text-transform:uppercase}}
.q h1 .sel{{position:relative;display:inline-block;padding:0 8px}}
.q h1 .sel:before{{content:"";position:absolute;inset:2px -2px -3px -2px;border:1.5px solid var(--or)}}
.q h1 .sel s{{position:absolute;width:8px;height:8px;background:#fff;border:1.5px solid var(--or)}}
.q .rule{{position:absolute;left:0;right:0;top:94px;text-align:center;font-size:14.5px;font-weight:500}}
.q .rule b{{font-weight:800}}
.q .bub{{position:absolute;left:0;top:0;width:176px;background:#fff;border-radius:14px;padding:8px 11px 8px;font-size:13px;line-height:1.24;font-weight:550;
  box-shadow:0 0 0 1.6px var(--ink),0 3px 0 1.6px var(--ink);will-change:transform}}
.q .bub:after{{content:"";position:absolute;top:16px;width:11px;height:11px;background:#fff;box-shadow:1.6px 1.6px 0 0 var(--ink)}}
.q .bub.l:after{{right:-6px;transform:rotate(-45deg)}}
.q .bub.r:after{{left:-6px;transform:rotate(135deg)}}
.q .bub em{{display:flex;align-items:center;gap:6px;font:500 9.5px/1 "DM Mono",monospace;font-style:normal;letter-spacing:.06em;text-transform:uppercase;opacity:.6;margin-top:5px}}
.q .bub em i{{width:9px;height:9px;border-radius:50%;box-shadow:0 0 0 1.5px #fff,0 0 0 2.5px rgba(0,0,0,.25)}}
.q .mos{{position:absolute;left:28px;right:28px;bottom:80px;display:flex;gap:16px}}
.q .mo{{flex:1;position:relative;cursor:pointer;background:#fff;border-radius:999px;padding:11px 16px 11px 54px;box-shadow:0 0 0 5px #fff,0 3px 8px rgba(0,0,0,.18);transition:transform .15s}}
.q .mo:nth-child(1){{transform:rotate(-1.5deg)}} .q .mo:nth-child(2){{transform:rotate(1deg)}} .q .mo:nth-child(3){{transform:rotate(-.6deg)}}
.q .mo:hover{{transform:rotate(0) translateY(-2px)}}
.q .mo i{{position:absolute;left:12px;top:50%;margin-top:-16px;width:32px;height:32px;border-radius:50%;background:var(--ink);color:var(--cream);font-style:normal;font-weight:900;font-size:16px;display:grid;place-items:center}}
.q .mo b{{display:block;font-weight:850;font-size:15px;letter-spacing:-.01em;line-height:1.1}}
.q .mo span{{display:block;font-size:11.5px;line-height:1.25;margin-top:2px}}
.q .mo .box{{position:absolute;inset:-12px -10px;border:1.5px solid var(--or);border-radius:4px;opacity:0;pointer-events:none}}
.q .mo .box s{{position:absolute;width:8px;height:8px;background:#fff;border:1.5px solid var(--or)}}
.q .mo .cur{{position:absolute;right:-16px;bottom:-22px;opacity:0;pointer-events:none}}
.q .mo:has(input:checked){{transform:rotate(0) scale(1.04);z-index:2}}
.q .mo:has(input:checked) i{{background:var(--or);color:#fff}}
.q .mo:has(input:checked) .box,.q .mo:has(input:checked) .cur{{opacity:1}}
.q .foot{{position:absolute;left:28px;right:28px;bottom:18px;display:flex;justify-content:space-between;align-items:center}}
.q .foot p{{font:500 11px/1.3 "DM Mono",monospace;letter-spacing:.05em;text-transform:uppercase}}
.q .cta{{height:46px;padding:0 26px;border-radius:23px;background:var(--ink);color:#fff;font-weight:850;font-size:15px;letter-spacing:.04em;text-transform:uppercase;box-shadow:0 4px 0 var(--or)}}
.q .tag{{position:absolute;font:500 10.5px/1 "DM Mono",monospace;letter-spacing:.06em;text-transform:uppercase;background:var(--cream);padding:3px 6px;border-radius:3px;box-shadow:0 0 0 1.4px var(--ink)}}
.q .nogl{{position:absolute;inset:200px 120px auto;text-align:center;font:500 12px "DM Mono",monospace;display:none}}
.castimgs img{{width:62px;height:78px;display:block}}
"""


def handles():
    return "".join(f'<s style="{p}"></s>' for p in ("left:-5px;top:-5px", "right:-5px;top:-5px", "left:-5px;bottom:-5px", "right:-5px;bottom:-5px"))


def game():
    bubs = "".join(f'<p class="bub {"l" if i < 3 else "r"}" data-i="{i}">{q}<em><i style="background:{TINT[cid]}"></i>{n} · {role}</em></p>'
                   for i, (cid, n, role, q, acc) in enumerate(g.CAST))
    cur = f'<svg class="cur" width="22" height="26" viewBox="0 0 22 26"><path d="M2 2l16 10-7 1.5 4 8-3 1.5-4-8-6 5z" fill="{INK}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>'
    mos = "".join(f'<label class="mo"><input type="radio" name="q" value="{l}"{" checked" if l == g.SEL else ""}><i>{l}</i><b>{t}</b><span>{d}</span><span class="box">{handles()}</span>{cur}</label>'
                  for l, t, d in g.MOTIONS)
    return f'''<div class="q" id="q"><canvas id="cv" width="740" height="640"></canvas>
<div class="ui">
<div class="meta"><span>Session {g.SESSION} · {g.DATE}</span><span><b>{g.STREAK}-day streak</b></span></div>
<h1>Tonight: <span class="sel">the empty lot{handles()}</span></h1>
<p class="rule">Six neighbors, one lot. <b>Pick the motion most of them will back.</b></p>
<span class="tag" id="lottag">The lot, today</span>
{bubs}
<div class="mos">{mos}</div>
<div class="foot"><p>{g.SAT} neighbors have voted today</p><button class="cta">Call the vote</button></div>
<p class="nogl">3D indisponible dans ce navigateur (WebGL désactivé).</p>
</div></div>'''


def kit():
    imgs = "".join(f'<figure><img alt="{n}" data-cast="{i}"><figcaption>{n}</figcaption></figure>' for i, (_, n, *_r) in enumerate(g.CAST))
    pills = (f'<div style="position:relative;display:inline-block;background:#fff;border-radius:999px;padding:9px 16px;font-weight:850;box-shadow:0 0 0 5px #fff,0 3px 8px rgba(0,0,0,.18);margin:8px 0 0 8px">Play court'
             f'<span style="position:absolute;inset:-12px -10px;border:1.5px solid {OR};border-radius:4px">{handles()}</span></div>')
    tints = "".join(f'<i style="display:inline-block;width:22px;height:22px;border-radius:50%;background:{TINT[c]};box-shadow:0 0 0 3px #fff,0 1px 3px rgba(0,0,0,.25);margin:0 8px 6px 0"></i>' for c, *_ in g.CAST)
    return g.kit("01", "Quartier 3D",
                 "Fusion de <b>Foule</b> et de <b>Stickers</b>, en vraie 3D temps réel. Les six voisins sont des <b>figurines en pâte claire cernées d'encre</b> "
                 "(rendu cartoon, contour noir) autour du terrain vague. Chacun se tient sur sa <b>pastille-sticker</b> de couleur et parle dans sa bulle. "
                 "Choisir une motion la <b>construit en orange sur le terrain</b>, avec un petit rebond. La caméra respire doucement, les voisins se tournent vers le terrain.",
                 [("Le casting en 3D", f'<div class="castrow castimgs">{imgs}</div><p class="note">Capsule, tête ronde, deux yeux, un seul accessoire. Pâte claire en trois tons, contour encre constant, ombre douce au sol.</p>'),
                  ("Couleur", g.sw(CREAM, "Crème", CREAM, "fond granuleux") + g.sw(INK, "Encre", INK, "contours, texte") + g.sw(OR, "Orange", OR, "motion, sélection") + f'<p class="note">Pastilles des voisins (tons pâles, sous les pieds et dans les bulles) :<br>{tints}</p>'),
                  ("Typo", '<p style="font-weight:900;font-size:36px;line-height:.92;letter-spacing:-.03em;text-transform:uppercase">Tonight: the<br>empty lot</p><p class="note">Archivo 900, approche serrée ; Archivo 550 dans les bulles ; DM Mono pour la méta.</p>'),
                  ("Motifs", pills + '<p class="note">Sticker-pilule à bord blanc, cadre de sélection à poignées, bulle cernée à ombre pleine, pastille sous chaque figurine.</p>')]).replace("V3 · direction 01/03", "V4 · fusion Foule + Stickers, 3D")


JS = r"""
const src = document.getElementById('three-src').textContent;
const THREE = await import(URL.createObjectURL(new Blob([src], {type: 'text/javascript'})));
const CAST = __CAST__, TINT = __TINT__;
const OPTS = Object.assign({cam: [12.4, 9.0], target: [0, .15, .25], mode: 'game', current: null, yes: null}, window.CONSEIL_OPTS || {});
const INK = 0x151515, CLAY = 0xf6f2e9, ORANGE = 0xff5a1f;
const cv = document.getElementById('cv');
let renderer;
try { renderer = new THREE.WebGLRenderer({canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true}); }
catch (e) { document.querySelector('.nogl').style.display = 'block'; throw e; }
renderer.setPixelRatio(Math.min(2, devicePixelRatio || 1));
renderer.setSize(740, 640, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(24, 740 / 640, .1, 100);

// three-step toon ramp: lit / mid / shade, like inked clay
const ramp = new THREE.DataTexture(new Uint8Array([150, 150, 150, 255, 214, 214, 214, 255, 255, 255, 255, 255]), 3, 1);
ramp.minFilter = ramp.magFilter = THREE.NearestFilter; ramp.needsUpdate = true;
const toon = c => new THREE.MeshToonMaterial({color: c, gradientMap: ramp});
const outlineMat = new THREE.ShaderMaterial({
  uniforms: {t: {value: .065}},
  vertexShader: 'uniform float t; void main(){ vec3 p = position + normal * t; gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }',
  fragmentShader: 'void main(){ gl_FragColor = vec4(0.082,0.082,0.082,1.0); }',
  side: THREE.BackSide});
function part(geo, color, {outline = true, cast = true, mat} = {}) {
  const m = new THREE.Mesh(geo, mat || toon(color));
  m.castShadow = cast;
  if (outline) { const o = new THREE.Mesh(geo, outlineMat); m.add(o); }
  return m;
}

scene.add(new THREE.HemisphereLight(0xffffff, 0xd9cfbd, 1.6));
const sun = new THREE.DirectionalLight(0xffffff, 2.2);
sun.position.set(-4, 9, 5); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); sun.shadow.radius = 6;
Object.assign(sun.shadow.camera, {left: -5, right: 5, top: 5, bottom: -5});
scene.add(sun);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({opacity: .16}));
ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

// ---------- a neighbor
function neighbor(acc, scale = 1, eyes = true) {
  const g = new THREE.Group();
  const body = part(new THREE.CapsuleGeometry(.3, .46, 6, 20), CLAY); body.position.y = .53; g.add(body);
  const head = new THREE.Group(); head.position.y = 1.2; g.add(head);
  head.add(part(new THREE.SphereGeometry(.27, 28, 20), CLAY));
  if (eyes) for (const x of [-.09, .09]) { const e = new THREE.Mesh(new THREE.SphereGeometry(.032, 10, 8), new THREE.MeshBasicMaterial({color: INK})); e.position.set(x, .02, .255); head.add(e); }
  if (acc === 'toque') {
    const band = part(new THREE.CylinderGeometry(.2, .2, .1, 24), CLAY); band.position.y = .25; head.add(band);
    for (const [x, y, z, r] of [[0, .43, 0, .17], [-.12, .37, .03, .12], [.12, .37, .02, .12], [0, .36, -.1, .12]]) { const p = part(new THREE.SphereGeometry(r, 18, 14), CLAY); p.position.set(x, y, z); head.add(p); }
  }
  if (acc === 'cap') {
    const c = part(new THREE.SphereGeometry(.28, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), CLAY); c.position.y = .04; head.add(c);
    const brim = part(new THREE.BoxGeometry(.3, .03, .22), CLAY); brim.position.set(0, .06, .3); head.add(brim);
  }
  if (acc === 'helmet') {
    const h = part(new THREE.SphereGeometry(.3, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), CLAY); h.position.y = .03; head.add(h);
    for (const x of [-.08, .08]) { const v = new THREE.Mesh(new THREE.BoxGeometry(.035, .05, .5), new THREE.MeshBasicMaterial({color: INK})); v.position.set(x, .3, 0); head.add(v); }
    const bag = part(new THREE.BoxGeometry(.2, .24, .12), CLAY); bag.position.set(.3, .45, .05); g.add(bag);
    const strap = new THREE.Mesh(new THREE.TorusGeometry(.33, .018, 6, 30), new THREE.MeshBasicMaterial({color: INK}));
    strap.position.set(0, .72, 0); strap.rotation.set(0, Math.PI / 2, .7); g.add(strap);
  }
  if (acc === 'cane') {
    const bun = part(new THREE.SphereGeometry(.11, 16, 12), CLAY); bun.position.set(0, .27, -.08); head.add(bun);
    const cane = part(new THREE.CylinderGeometry(.025, .025, .8, 8), CLAY); cane.position.set(.4, .4, .12); cane.rotation.z = -.08; g.add(cane);
    const hook = part(new THREE.TorusGeometry(.07, .025, 8, 16, Math.PI), CLAY); hook.position.set(.33, .8, .12); g.add(hook);
  }
  if (acc === 'can') {
    const c = part(new THREE.CylinderGeometry(.11, .12, .2, 18), CLAY); c.position.set(.42, .3, .1); g.add(c);
    const sp = part(new THREE.CylinderGeometry(.02, .025, .26, 8), CLAY); sp.position.set(.58, .38, .1); sp.rotation.z = -.9; g.add(sp);
  }
  if (acc === 'kid') { const k = neighbor('', .58); k.position.set(.48, 0, .12); g.add(k); g.userData.kid = k; }
  g.scale.setScalar(scale);
  const arm = part(new THREE.CapsuleGeometry(.075, .44, 4, 10), CLAY); arm.position.set(-.36, 1.18, .02); arm.rotation.z = .32; arm.visible = false; g.add(arm);
  g.userData.arm = arm;
  g.userData.head = head;
  return g;
}
function disc(tint) {
  const g = new THREE.Group();
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(.62, .62, .045, 40), toon(0xffffff)); rim.position.y = .022; rim.receiveShadow = true; g.add(rim);
  const top = new THREE.Mesh(new THREE.CylinderGeometry(.54, .54, .05, 40), toon(new THREE.Color(tint))); top.position.y = .026; top.receiveShadow = true; g.add(top);
  return g;
}

// ---------- the lot
const LOT = new THREE.Group(); LOT.scale.setScalar(.56); scene.add(LOT);
const slab = new THREE.Mesh(new THREE.BoxGeometry(4.2, .06, 2.8), toon(0xe8dcc2)); slab.position.y = .03; slab.receiveShadow = true; LOT.add(slab);
const postGeo = new THREE.CylinderGeometry(.025, .025, .22, 6), postMat = new THREE.MeshBasicMaterial({color: INK});
for (let i = 0; i <= 24; i++) {
  const t = i / 24, per = 2 * (4.2 + 2.8), d = t * per;
  let x, z;
  if (d < 4.2) { x = -2.1 + d; z = -1.4; } else if (d < 7) { x = 2.1; z = -1.4 + (d - 4.2); } else if (d < 11.2) { x = 2.1 - (d - 7); z = 1.4; } else { x = -2.1; z = 1.4 - (d - 11.2); }
  const p = new THREE.Mesh(postGeo, postMat); p.position.set(x, .11, z); LOT.add(p);
}
const weeds = new THREE.Group(); LOT.add(weeds);
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (let i = 0; i < 26; i++) {
  const w = new THREE.Group();
  for (let k = 0; k < 3; k++) { const b = new THREE.Mesh(new THREE.ConeGeometry(.025, .22 + rnd() * .12, 5), postMat); b.position.set((k - 1) * .05, .12, 0); b.rotation.z = (k - 1) * .35; w.add(b); }
  w.position.set(-1.9 + rnd() * 3.8, .06, -1.2 + rnd() * 2.4); weeds.add(w);
}

// ---------- the three motions, built in orange
const box = (w, h, d, c, x, y, z) => { const m = part(new THREE.BoxGeometry(w, h, d), c); m.position.set(x, y, z); m.receiveShadow = true; return m; };
function rack(x, z, ry = 0) { const r = part(new THREE.TorusGeometry(.16, .025, 8, 20, Math.PI), INK, {outline: false}); r.material = new THREE.MeshBasicMaterial({color: INK}); r.position.set(x, .06, z); r.rotation.y = ry; return r; }
function beds(cols, rows, x0, z0) {
  const g = new THREE.Group();
  for (let c = 0; c < cols; c++) for (let r = 0; r < rows; r++) {
    const x = x0 + c * 1.05, z = z0 + r * .82;
    g.add(box(.8, .22, .56, ORANGE, x, .17, z));
    for (const dx of [-.22, 0, .22]) { const s = new THREE.Mesh(new THREE.ConeGeometry(.05, .2, 6), postMat); s.position.set(x + dx, .38, z); g.add(s); }
  }
  return g;
}
function court(w, d, x0, hoops) {
  const g = new THREE.Group();
  g.add(box(w, .05, d, ORANGE, x0, .085, 0));
  const white = new THREE.MeshBasicMaterial({color: 0xffffff}), L = (lw, ld, x, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(lw, .012, ld), white); m.position.set(x, .118, z); g.add(m); };
  L(.03, d - .16, x0, 0); L(w - .16, .03, x0, -d / 2 + .08); L(w - .16, .03, x0, d / 2 - .08); L(.03, d - .16, x0 - w / 2 + .08, 0); L(.03, d - .16, x0 + w / 2 - .08, 0);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(.32, .015, 6, 40), white); ring.rotation.x = Math.PI / 2; ring.position.set(x0, .12, 0); g.add(ring);
  if (hoops) for (const s of [-1, 1]) {
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, 1.1, 8), postMat); pole.position.set(x0 + s * (w / 2 + .1), .6, 0); g.add(pole);
    const board = box(.04, .36, .56, 0xffffff, x0 + s * (w / 2 + .06), 1.08, 0); g.add(board);
  }
  return g;
}
const MOT = {
  A: beds(3, 3, -1.05, -.82),
  B: (() => { const g = court(2.9, 2.1, -.45, true); for (let i = 0; i < 4; i++) g.add(rack(1.55, -.9 + i * .6, Math.PI / 2)); return g; })(),
  C: (() => { const g = beds(1, 3, -1.55, -.82); g.add(court(1.9, 2.1, .25, false)); for (let i = 0; i < 3; i++) g.add(rack(1.65, -.6 + i * .6, Math.PI / 2)); return g; })(),
};
for (const k in MOT) { MOT[k].scale.setScalar(.001); LOT.add(MOT[k]); }

// ---------- the six, on their stickers, around the lot
const SPOTS = OPTS.spots || [[-1.5, -1.2], [-1.68, .15], [-1.5, 1.5], [1.5, -1.2], [1.68, .15], [1.5, 1.5]];
const people = CAST.map((c, i) => {
  const g = new THREE.Group();
  g.add(disc(TINT[c.id]));
  const n = neighbor(c.acc); n.position.y = .05; g.add(n);
  g.scale.setScalar(.55); g.position.set(SPOTS[i][0], 0, SPOTS[i][1]);
  g.lookAt(g.position.x * .35, 0, 7);
  if (OPTS.yes) { if (OPTS.yes.includes(c.id)) n.userData.arm.visible = true; else n.rotation.y = Math.PI * .92; }
  scene.add(g); return {g, n, c};
});
// passers-by, the rest of the street (smaller, faded)
if (OPTS.noLot) LOT.visible = false;
for (const [x, z] of (OPTS.noLot ? [] : [[-.8, -2.1], [1.1, -2.3], [-2.9, -2.6], [3.0, -2.5]])) {
  const p = neighbor('', .4); p.position.set(x, 0, z); p.rotation.y = (x > 0 ? -1 : 1) * .5;
  p.traverse(o => { if (o.material && o.material.isMeshToonMaterial) { o.material = o.material.clone(); o.material.transparent = true; o.material.opacity = .3; } });
  scene.add(p);
}

// ---------- camera + overlay anchoring
const target = new THREE.Vector3(...OPTS.target);
function placeCam(t) {
  const a = Math.sin(t * .00025) * .06;
  cam.position.set(Math.sin(a) * OPTS.cam[0], OPTS.cam[1], Math.cos(a) * OPTS.cam[0]);
  cam.lookAt(target);
}
const ancs = [...document.querySelectorAll('.q [data-i]')], tag = document.getElementById('lottag');
const v = new THREE.Vector3();
function anchor() {
  ancs.forEach(b => {
    const i = +b.dataset.i, p = people[i]; p.n.userData.head.getWorldPosition(v); v.project(cam);
    const x = (v.x + 1) / 2 * 740, y = (1 - v.y) / 2 * 640, w = b.offsetWidth, side = b.dataset.side || (i < 3 ? 'l' : 'r');
    let left, top;
    if (side === 't') { left = x - w / 2; top = y - b.offsetHeight - 26; }
    else { left = side === 'l' ? x - 44 - w : x + 44; top = y - 34; }
    b.style.transform = `translate(${Math.round(Math.max(8, Math.min(740 - w - 8, left)))}px, ${Math.round(top)}px)`;
  });
  if (!tag) return;
  v.set(-2.1, .1, -1.4).project(cam);
  tag.style.left = Math.round((v.x + 1) / 2 * 740 - 20) + 'px'; tag.style.top = Math.round((1 - v.y) / 2 * 640 - 30) + 'px';
}

// ---------- choosing a motion builds it on the lot
let current = null, changedAt = 0;
function choose(k) { current = k; changedAt = performance.now(); }
document.querySelectorAll('.q input[name=q]').forEach(r => r.addEventListener('change', () => choose(r.value)));
const pre = document.querySelector('.q input[name=q]:checked'); if (pre) choose(pre.value); else if (OPTS.current) choose(OPTS.current);
const spring = t => t <= 0 ? 0 : 1 - Math.exp(-7 * t) * Math.cos(11 * t);

function frame(t) {
  placeCam(t);
  const dt = (performance.now() - changedAt) / 1000;
  for (const k in MOT) {
    const on = k === current, s = on ? Math.max(.001, spring(dt)) : Math.max(.001, MOT[k].scale.x * .82);
    MOT[k].scale.setScalar(s);
  }
  weeds.visible = !current;
  people.forEach((p, i) => {
    const b = Math.sin(t * .002 + i * 1.3);
    p.n.position.y = .05 + Math.max(0, b) * .02;
    p.n.userData.head.rotation.z = Math.sin(t * .0013 + i) * .06;
    if (p.n.userData.arm.visible) p.n.userData.arm.rotation.z = .32 + Math.sin(t * .006 + i) * .12;
    if (OPTS.mode === 'game' && current && dt < .9) p.n.position.y += Math.max(0, Math.sin(dt * 9 - i * .35)) * .12 * (1 - dt / .9);
  });
  renderer.render(scene, cam);
  anchor();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

// ---------- cast portraits for the kit (rendered once, same materials)
const pr = new THREE.WebGLRenderer({antialias: true, alpha: true, preserveDrawingBuffer: true});
pr.setPixelRatio(2); pr.setSize(62, 78);
const ps = new THREE.Scene(); ps.add(new THREE.HemisphereLight(0xffffff, 0xd9cfbd, 1.6)); const pl = new THREE.DirectionalLight(0xffffff, 2.2); pl.position.set(-4, 9, 5); ps.add(pl);
const pc = new THREE.PerspectiveCamera(24, 62 / 78, .1, 50); pc.position.set(0, 1.5, 5.4); pc.lookAt(0, .78, 0);
CAST.forEach((c, i) => {
  const g = new THREE.Group(); g.add(disc(TINT[c.id])); const n = neighbor(c.acc); n.position.y = .05; g.add(n); g.rotation.y = -.35;
  ps.add(g); pr.render(ps, pc); ps.remove(g);
  const img = document.querySelector(`img[data-cast="${i}"]`); if (img) img.src = pr.domElement.toDataURL();
});
document.documentElement.dataset.ready = '1';
"""


def page():
    base = g.BASE.replace("__ARCHIVO__", g.F["archivo"]).replace("__DM4__", g.F["dmmono-400"]).replace("__DM5__", g.F["dmmono-500"])
    cast = json.dumps([{"id": c[0], "acc": c[4]} for c in g.CAST])
    js = JS.replace("__CAST__", cast).replace("__TINT__", json.dumps(TINT))
    (OUT / "01-quartier-3d.html").write_text(f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conseil · Jeu V4 · Quartier 3D</title>
<style>{base}{CSS}</style></head>
<body><div class="sheet" id="sheet">{g.chrome(game())}{kit()}</div>
<script type="text/plain" id="three-src">{THREE}</script>
<script type="module">{js}</script>
<script>(function(){{var s=document.getElementById("sheet");function f(){{var k=Math.min(1,innerWidth/1440);s.style.transform="scale("+k+")";document.body.style.height=s.offsetHeight*k+"px"}}addEventListener("resize",f);f()}})();</script>
</body></html>''')


if __name__ == "__main__":
    page()
    print("ok")
