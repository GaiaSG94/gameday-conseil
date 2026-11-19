/* eslint-disable @typescript-eslint/no-explicit-any -- vendor three.module.js
   is untyped (shorthand ambient module): its objects are intentionally any */
import * as THREE from './vendor/three.module.js';

import type { Neighbor } from '../shared/game';

export type SceneOpts = {
  mode: 'game' | 'result';
  cast: Neighbor[];
  tints: Record<string, string>;
  current: number | null;
  yes: string[] | null;
};

export type SceneHandle = {
  setChoice: (motion: number | null) => void;
  setYes: (ids: string[] | null) => void;
  dispose: () => void;
};

type Part = (geo: unknown, color: unknown, outlined?: boolean) => any;

const INK = 0x151515;
const CLAY = 0xf6f2e9;
const ORANGE = 0xff5a1f;
const SPOTS: [number, number][] = [
  [-1.5, -1.2],
  [-1.68, 0.15],
  [-1.5, 1.5],
  [1.5, -1.2],
  [1.68, 0.15],
  [1.5, 1.5],
];

const spring = (t: number): number =>
  t <= 0 ? 0 : 1 - Math.exp(-7 * t) * Math.cos(11 * t);

const buildMaterials = () => {
  const ramp = new THREE.DataTexture(
    new Uint8Array([150, 150, 150, 255, 214, 214, 214, 255, 255, 255, 255, 255]),
    3,
    1
  );
  ramp.minFilter = THREE.NearestFilter;
  ramp.magFilter = THREE.NearestFilter;
  ramp.needsUpdate = true;
  const toon = (color: number | string | undefined): any =>
    new THREE.MeshToonMaterial({ color, gradientMap: ramp });
  const outline = new THREE.ShaderMaterial({
    uniforms: { t: { value: 0.065 } },
    vertexShader:
      'uniform float t; void main(){ vec3 p = position + normal * t; gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }',
    fragmentShader: 'void main(){ gl_FragColor = vec4(0.082,0.082,0.082,1.0); }',
    side: THREE.BackSide,
  });
  return { toon, outline };
};

const makePart = (mat: ReturnType<typeof buildMaterials>): Part => (
  geo,
  color,
  outlined = true
) => {
  const m = new THREE.Mesh(geo as never, mat.toon(color as number));
  m.castShadow = true;
  if (outlined) m.add(new THREE.Mesh(geo as never, mat.outline));
  return m;
};

const buildLot = (mat: ReturnType<typeof buildMaterials>): any => {
  const lot = new THREE.Group();
  lot.scale.setScalar(0.56);
  const slab = new THREE.Mesh(
    new THREE.BoxGeometry(4.2, 0.06, 2.8) as never,
    mat.toon(0xe8dcc2)
  );
  slab.position.y = 0.03;
  slab.receiveShadow = true;
  lot.add(slab);
  return lot;
};

export const mountScene = (host: HTMLElement, opts: SceneOpts): SceneHandle => {
  const canvas = host.querySelector('canvas') as HTMLCanvasElement;
  const scene = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(24, 740 / 640, 0.1, 100);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  scene.add(new THREE.HemisphereLight(0xffffff, 0xd9cfbd, 1.6));
  const sun = new THREE.DirectionalLight(0xffffff, 2.2);
  sun.position.set(-4, 9, 5);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.radius = 6;
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5 });
  scene.add(sun);
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(40, 40) as never,
    new THREE.ShadowMaterial({ opacity: 0.16 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  const mat = buildMaterials();
  const part = makePart(mat);
  const lot = buildLot(mat);
  scene.add(lot);
  const { motions, weeds } = buildMotions(part, lot);
  const people = buildCast(opts, part, scene);
  buildPassersBy(part, scene);

  const target = new THREE.Vector3(0, 0.15, 0.25);
  let choice = opts.current;
  let changedAt = performance.now();
  let raf = 0;

  const resize = (): void => {
    const w = host.clientWidth || 740;
    const h = host.clientHeight || 640;
    renderer.setSize(w, h, false);
    cam.aspect = w / h;
    cam.updateProjectionMatrix();
  };
  resize();
  window.addEventListener('resize', resize);

  const anchor = (): void => {
    const w = host.clientWidth || 740;
    const h = host.clientHeight || 640;
    const k = w / 740;
    const v = new THREE.Vector3();
    host.querySelectorAll<HTMLElement>('[data-i]').forEach((bub) => {
      const i = Number(bub.dataset.i);
      const person = people[i];
      if (!person) return;
      person.head.getWorldPosition(v);
      v.project(cam);
      const x = ((v.x + 1) / 2) * w;
      const y = ((1 - v.y) / 2) * h;
      const bw = bub.offsetWidth;
      const side = i < 3 ? 'l' : 'r';
      const left = side === 'l' ? x - 44 * k - bw : x + 44 * k;
      const top = y - 34 * k;
      bub.style.transform = `translate(${Math.round(Math.max(8, Math.min(w - bw - 8, left)))}px, ${Math.round(top)}px)`;
    });
    const tag = host.querySelector<HTMLElement>('.tag');
    if (tag) {
      v.set(-2.1, 0.1, -1.4).project(cam);
      tag.style.left = `${Math.round(((v.x + 1) / 2) * w - 20)}px`;
      tag.style.top = `${Math.round(((1 - v.y) / 2) * h - 30)}px`;
    }
  };

  const frame = (): void => {
    const t = performance.now();
    const dt = (t - changedAt) / 1000;
    const a = Math.sin(t * 0.00025) * 0.06;
    cam.position.set(Math.sin(a) * 12.4, 9.0, Math.cos(a) * 12.4);
    cam.lookAt(target);
    motions.forEach((m, k) => {
      const on = k === choice;
      const s = on ? Math.max(0.001, spring(dt)) : Math.max(0.001, m.scale.x * 0.82);
      m.scale.setScalar(s);
    });
    weeds.visible = choice === null;
    people.forEach((p, i) => {
      const b = Math.sin(t * 0.002 + i * 1.3);
      p.n.position.y = 0.05 + Math.max(0, b) * 0.02;
      p.head.rotation.z = Math.sin(t * 0.0013 + i) * 0.06;
      if (p.arm.visible) p.arm.rotation.z = 0.32 + Math.sin(t * 0.006 + i) * 0.12;
      if (opts.mode === 'game' && choice !== null && dt < 0.9) {
        p.n.position.y += Math.max(0, Math.sin(dt * 9 - i * 0.35)) * 0.12 * (1 - dt / 0.9);
      }
    });
    renderer.render(scene, cam);
    anchor();
    raf = requestAnimationFrame(frame);
  };
  raf = requestAnimationFrame(frame);

  return {
    setChoice: (motion) => {
      choice = motion;
      changedAt = performance.now();
    },
    setYes: (ids) => {
      people.forEach((p) => {
        p.arm.visible = ids !== null && ids.includes(p.id);
        if (p.arm.visible) p.g.rotation.y = 0;
        else p.g.rotation.y = Math.PI * 0.92;
      });
    },
    dispose: () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', resize);
      renderer.dispose();
    },
  };
};

const buildMotions = (part: Part, lot: any): { motions: any[]; weeds: any } => {
  const postMat = new THREE.MeshBasicMaterial({ color: INK });
  const box = (w: number, h: number, d: number, color: number, x: number, y: number, z: number): any => {
    const m = part(new THREE.BoxGeometry(w, h, d), color);
    m.position.set(x, y, z);
    m.receiveShadow = true;
    return m;
  };
  const postRing = (group: any): void => {
    for (let i = 0; i <= 24; i++) {
      const per = 2 * (4.2 + 2.8);
      const d = (i / 24) * per;
      let x: number;
      let z: number;
      if (d < 4.2) {
        x = -2.1 + d;
        z = -1.4;
      } else if (d < 7) {
        x = 2.1;
        z = -1.4 + (d - 4.2);
      } else if (d < 11.2) {
        x = 2.1 - (d - 7);
        z = 1.4;
      } else {
        x = -2.1;
        z = 1.4 - (d - 11.2);
      }
      const p = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.22, 6) as never, postMat);
      p.position.set(x, 0.11, z);
      group.add(p);
    }
  };
  postRing(lot);

  let seed = 7;
  const rnd = (): number => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const weeds = new THREE.Group();
  for (let i = 0; i < 26; i++) {
    const w = new THREE.Group();
    for (let k = 0; k < 3; k++) {
      const blade = new THREE.Mesh(
        new THREE.ConeGeometry(0.025, 0.22 + rnd() * 0.12, 5) as never,
        postMat
      );
      blade.position.set((k - 1) * 0.05, 0.12, 0);
      blade.rotation.z = (k - 1) * 0.35;
      w.add(blade);
    }
    w.position.set(-1.9 + rnd() * 3.8, 0.06, -1.2 + rnd() * 2.4);
    weeds.add(w);
  }
  lot.add(weeds);

  const rack = (x: number, z: number, ry = 0): any => {
    const r = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.025, 8, 20, Math.PI) as never, postMat);
    r.position.set(x, 0.06, z);
    r.rotation.y = ry;
    return r;
  };
  const beds = (cols: number, rows: number, x0: number, z0: number): any => {
    const g = new THREE.Group();
    for (let c = 0; c < cols; c++) {
      for (let r = 0; r < rows; r++) {
        const x = x0 + c * 1.05;
        const z = z0 + r * 0.82;
        g.add(box(0.8, 0.22, 0.56, ORANGE, x, 0.17, z));
        for (const dx of [-0.22, 0, 0.22]) {
          const sprout = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.2, 6) as never, postMat);
          sprout.position.set(x + dx, 0.38, z);
          g.add(sprout);
        }
      }
    }
    return g;
  };
  const court = (w: number, d: number, x0: number, hoops: boolean): any => {
    const g = new THREE.Group();
    g.add(box(w, 0.05, d, ORANGE, x0, 0.085, 0));
    const white = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const line = (lw: number, ld: number, x: number, z: number): void => {
      const m = new THREE.Mesh(new THREE.BoxGeometry(lw, 0.012, ld) as never, white);
      m.position.set(x, 0.118, z);
      g.add(m);
    };
    line(0.03, d - 0.16, x0, 0);
    line(w - 0.16, 0.03, x0, -d / 2 + 0.08);
    line(w - 0.16, 0.03, x0, d / 2 - 0.08);
    line(0.03, d - 0.16, x0 - w / 2 + 0.08, 0);
    line(0.03, d - 0.16, x0 + w / 2 - 0.08, 0);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.015, 6, 40) as never, white);
    ring.rotation.x = Math.PI / 2;
    ring.position.set(x0, 0.12, 0);
    g.add(ring);
    if (hoops) {
      for (const s of [-1, 1]) {
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.1, 8) as never, postMat);
        pole.position.set(x0 + s * (w / 2 + 0.1), 0.6, 0);
        g.add(pole);
        g.add(box(0.04, 0.36, 0.56, 0xffffff, x0 + s * (w / 2 + 0.06), 1.08, 0));
      }
    }
    return g;
  };
  const a = beds(3, 3, -1.05, -0.82);
  const b = court(2.9, 2.1, -0.45, true);
  for (let i = 0; i < 4; i++) b.add(rack(1.55, -0.9 + i * 0.6, Math.PI / 2));
  const c = beds(1, 3, -1.55, -0.82);
  c.add(court(1.9, 2.1, 0.25, false));
  for (let i = 0; i < 3; i++) c.add(rack(1.65, -0.6 + i * 0.6, Math.PI / 2));
  const motions = [a, b, c];
  motions.forEach((m) => {
    m.scale.setScalar(0.001);
    lot.add(m);
  });
  return { motions, weeds };
};

const buildDisc = (tint: string): any => {
  const g = new THREE.Group();
  const rim = new THREE.Mesh(
    new THREE.CylinderGeometry(0.62, 0.62, 0.045, 40) as never,
    new THREE.MeshToonMaterial({ color: 0xffffff })
  );
  rim.position.y = 0.022;
  rim.receiveShadow = true;
  g.add(rim);
  const top = new THREE.Mesh(
    new THREE.CylinderGeometry(0.54, 0.54, 0.05, 40) as never,
    new THREE.MeshToonMaterial({ color: new THREE.Color(tint) })
  );
  top.position.y = 0.026;
  top.receiveShadow = true;
  g.add(top);
  return g;
};

const buildAccessory = (part: Part, g: any, head: any, acc: string): void => {
  const inkMat = new THREE.MeshBasicMaterial({ color: INK });
  if (acc === 'toque') {
    const band = part(new THREE.CylinderGeometry(0.2, 0.2, 0.1, 24), CLAY);
    band.position.y = 0.25;
    head.add(band);
    const puffs: [number, number, number, number][] = [
      [0, 0.43, 0, 0.17],
      [-0.12, 0.37, 0.03, 0.12],
      [0.12, 0.37, 0.02, 0.12],
      [0, 0.36, -0.1, 0.12],
    ];
    for (const [x, y, z, r] of puffs) {
      const puff = part(new THREE.SphereGeometry(r, 18, 14), CLAY);
      puff.position.set(x, y, z);
      head.add(puff);
    }
  }
  if (acc === 'cap') {
    const cap = part(
      new THREE.SphereGeometry(0.28, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2),
      CLAY
    );
    cap.position.y = 0.04;
    head.add(cap);
    const brim = part(new THREE.BoxGeometry(0.3, 0.03, 0.22), CLAY);
    brim.position.set(0, 0.06, 0.3);
    head.add(brim);
  }
  if (acc === 'helmet') {
    const shell = part(
      new THREE.SphereGeometry(0.3, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2),
      CLAY
    );
    shell.position.y = 0.03;
    head.add(shell);
    for (const x of [-0.08, 0.08]) {
      const vent = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.05, 0.5) as never, inkMat);
      vent.position.set(x, 0.3, 0);
      head.add(vent);
    }
    const bag = part(new THREE.BoxGeometry(0.2, 0.24, 0.12), CLAY);
    bag.position.set(0.3, 0.45, 0.05);
    g.add(bag);
    const strap = new THREE.Mesh(new THREE.TorusGeometry(0.33, 0.018, 6, 30) as never, inkMat);
    strap.position.set(0, 0.72, 0);
    strap.rotation.set(0, Math.PI / 2, 0.7);
    g.add(strap);
  }
  if (acc === 'cane') {
    const bun = part(new THREE.SphereGeometry(0.11, 16, 12), CLAY);
    bun.position.set(0, 0.27, -0.08);
    head.add(bun);
    const cane = part(new THREE.CylinderGeometry(0.025, 0.025, 0.8, 8), CLAY);
    cane.position.set(0.4, 0.4, 0.12);
    cane.rotation.z = -0.08;
    g.add(cane);
    const hook = part(new THREE.TorusGeometry(0.07, 0.025, 8, 16, Math.PI), CLAY);
    hook.position.set(0.33, 0.8, 0.12);
    g.add(hook);
  }
  if (acc === 'can') {
    const can = part(new THREE.CylinderGeometry(0.11, 0.12, 0.2, 18), CLAY);
    can.position.set(0.42, 0.3, 0.1);
    g.add(can);
    const spout = part(new THREE.CylinderGeometry(0.02, 0.025, 0.26, 8), CLAY);
    spout.position.set(0.58, 0.38, 0.1);
    spout.rotation.z = -0.9;
    g.add(spout);
  }
  if (acc === 'kid') {
    const k = buildNeighbor(part, '');
    k.scale.setScalar(0.58);
    k.position.set(0.48, 0, 0.12);
    g.add(k);
    g.userData.kid = k;
  }
};

const buildNeighbor = (part: Part, acc: string): any => {
  const g = new THREE.Group();
  const body = part(new THREE.CapsuleGeometry(0.3, 0.46, 6, 20), CLAY);
  body.position.y = 0.53;
  g.add(body);
  const head = new THREE.Group();
  head.position.y = 1.2;
  g.add(head);
  head.add(part(new THREE.SphereGeometry(0.27, 28, 20), CLAY));
  for (const x of [-0.09, 0.09]) {
    const eye = new THREE.Mesh(
      new THREE.SphereGeometry(0.032, 10, 8) as never,
      new THREE.MeshBasicMaterial({ color: INK })
    );
    eye.position.set(x, 0.02, 0.255);
    head.add(eye);
  }
  buildAccessory(part, g, head, acc);
  const arm = part(new THREE.CapsuleGeometry(0.075, 0.44, 4, 10), CLAY);
  arm.position.set(-0.36, 1.18, 0.02);
  arm.rotation.z = 0.32;
  arm.visible = false;
  g.add(arm);
  g.userData.arm = arm;
  g.userData.head = head;
  return g;
};

type Person = { id: string; g: any; n: any; head: any; arm: any };

const buildCast = (opts: SceneOpts, part: Part, scene: any): Person[] =>
  opts.cast.map((neighbor, i) => {
    const spot = SPOTS[i] ?? SPOTS[0]!;
    const g = new THREE.Group();
    g.add(buildDisc(opts.tints[neighbor.id] ?? '#dddddd'));
    const n = buildNeighbor(part, neighbor.acc);
    n.position.y = 0.05;
    g.add(n);
    g.scale.setScalar(0.55);
    g.position.set(spot[0], 0, spot[1]);
    g.lookAt(g.position.x * 0.35, 0, 7);
    if (opts.yes) {
      const arm = n.userData.arm;
      arm.visible = opts.yes.includes(neighbor.id);
      if (!arm.visible) n.rotation.y = Math.PI * 0.92;
    }
    scene.add(g);
    return { id: neighbor.id, g, n, head: n.userData.head, arm: n.userData.arm };
  });

const buildPassersBy = (part: Part, scene: any): void => {
  const spots: [number, number][] = [
    [-0.8, -2.1],
    [1.1, -2.3],
    [-2.9, -2.6],
    [3.0, -2.5],
  ];
  for (const [x, z] of spots) {
    const p = buildNeighbor(part, '');
    p.scale.setScalar(0.4);
    p.position.set(x, 0, z);
    p.rotation.y = (x > 0 ? -1 : 1) * 0.5;
    p.traverse((o: { material?: { isMeshToonMaterial?: boolean; clone?: () => any } }) => {
      const material = o.material;
      if (material && material.isMeshToonMaterial && material.clone) {
        const faded = material.clone();
        faded.transparent = true;
        faded.opacity = 0.3;
        o.material = faded;
      }
    });
    scene.add(p);
  }
};

export const letterOf = (motion: number): string =>
  ['A', 'B', 'C'][motion] ?? 'A';
