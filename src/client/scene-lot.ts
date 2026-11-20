/* eslint-disable @typescript-eslint/no-explicit-any -- vendor three.module.js
   is untyped (shorthand ambient module): its objects are intentionally any */
import * as THREE from './vendor/three.module.js';

import type { Mats, Part } from './scene-materials';
import { inkMaterial, whiteMaterial } from './scene-materials';
import { LOT_COLOR, ORANGE } from './scene-materials';

export type Lot = { group: any; weeds: any };

const box = (part: Part, w: number, h: number, d: number, color: number, x: number, y: number, z: number): any => {
  const m = part(new THREE.BoxGeometry(w, h, d), color);
  m.position.set(x, y, z);
  m.receiveShadow = true;
  return m;
};

const postRing = (group: any): void => {
  const postMat = inkMaterial();
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

const buildWeeds = (lot: any): any => {
  const postMat = inkMaterial();
  const weeds = new THREE.Group();
  let seed = 7;
  const rnd = (): number => (seed = (seed * 16807) % 2147483647) / 2147483647;
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
  return weeds;
};

/* The empty lot: beige slab, ink stakes, wild weeds. */
export const buildLot = (mat: Mats): Lot => {
  const group = new THREE.Group();
  group.scale.setScalar(0.56);
  const slab = new THREE.Mesh(
    new THREE.BoxGeometry(4.2, 0.06, 2.8) as never,
    mat.toon(LOT_COLOR)
  );
  slab.position.y = 0.03;
  slab.receiveShadow = true;
  group.add(slab);
  postRing(group);
  const weeds = buildWeeds(group);
  return { group, weeds };
};

const rack = (part: Part, x: number, z: number, ry = 0): any => {
  const r = part(new THREE.TorusGeometry(0.16, 0.025, 8, 20, Math.PI), ORANGE, false);
  r.material = inkMaterial();
  r.position.set(x, 0.06, z);
  r.rotation.y = ry;
  return r;
};

const beds = (part: Part, cols: number, rows: number, x0: number, z0: number): any => {
  const g = new THREE.Group();
  const postMat = inkMaterial();
  for (let c = 0; c < cols; c++) {
    for (let r = 0; r < rows; r++) {
      const x = x0 + c * 1.05;
      const z = z0 + r * 0.82;
      g.add(box(part, 0.8, 0.22, 0.56, ORANGE, x, 0.17, z));
      for (const dx of [-0.22, 0, 0.22]) {
        const sprout = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.2, 6) as never, postMat);
        sprout.position.set(x + dx, 0.38, z);
        g.add(sprout);
      }
    }
  }
  return g;
};

const court = (part: Part, w: number, d: number, x0: number, hoops: boolean): any => {
  const g = new THREE.Group();
  const postMat = inkMaterial();
  const white = whiteMaterial();
  g.add(box(part, w, 0.05, d, ORANGE, x0, 0.085, 0));
  const line = (lw: number, ld: number, x: number, z: number): void => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(lw, 0.012, ld) as never, white);
    m.position.set(x, 0.118, z);
    g.add(m);
  };
  line(0.03, d - 0.16, x0, 0);
  line(w - 0.16, 0.03, x0, -d / 2 + 0.08);
  line(w - 0.16, 0.03, x0, d / 2 - 0.08);
  line(0.03, d - 0.16, x0 - w / 2 + 0.08, 0);
  line(0.03, d - 0.16, x0 + w / 2 + 0.08, 0);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.015, 6, 40) as never, white);
  ring.rotation.x = Math.PI / 2;
  ring.position.set(x0, 0.12, 0);
  g.add(ring);
  if (hoops) {
    for (const s of [-1, 1]) {
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.1, 8) as never, postMat);
      pole.position.set(x0 + s * (w / 2 + 0.1), 0.6, 0);
      g.add(pole);
      g.add(box(part, 0.04, 0.36, 0.56, 0xffffff, x0 + s * (w / 2 + 0.06), 1.08, 0));
    }
  }
  return g;
};

/* The three motions, built in orange on the lot: A beds, B court + racks, C shared. */
export const buildMotions = (part: Part, lot: any): any[] => {
  const a = beds(part, 3, 3, -1.05, -0.82);
  const b = court(part, 2.9, 2.1, -0.45, true);
  for (let i = 0; i < 4; i++) b.add(rack(part, 1.55, -0.9 + i * 0.6, Math.PI / 2));
  const c = beds(part, 1, 3, -1.55, -0.82);
  c.add(court(part, 1.9, 2.1, 0.25, false));
  for (let i = 0; i < 3; i++) c.add(rack(part, 1.65, -0.6 + i * 0.6, Math.PI / 2));
  const motions = [a, b, c];
  motions.forEach((m) => {
    m.scale.setScalar(0.001);
    lot.add(m);
  });
  return motions;
};
