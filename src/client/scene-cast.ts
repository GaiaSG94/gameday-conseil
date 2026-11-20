/* eslint-disable @typescript-eslint/no-explicit-any -- vendor three.module.js
   is untyped (shorthand ambient module): its objects are intentionally any */
import * as THREE from './vendor/three.module.js';

import type { Part } from './scene-materials';
import { CLAY, inkMaterial } from './scene-materials';

export type Neighbor3d = { g: any; n: any; head: any; arm: any };

/* Sticker pastille under each neighbor: white rim, tinted top. */
export const buildDisc = (tint: string): any => {
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
  const inkMat = inkMaterial();
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
    const cap = part(new THREE.SphereGeometry(0.28, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), CLAY);
    cap.position.y = 0.04;
    head.add(cap);
    const brim = part(new THREE.BoxGeometry(0.3, 0.03, 0.22), CLAY);
    brim.position.set(0, 0.06, 0.3);
    head.add(brim);
  }
  if (acc === 'helmet') {
    const shell = part(new THREE.SphereGeometry(0.3, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), CLAY);
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

/* Capsule body, round head, two eyes, one accessory that says who they are. */
export const buildNeighbor = (part: Part, acc: string): any => {
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
      inkMaterial()
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

/* The rest of the street: smaller, faded, out of the debate. */
export const buildPassersBy = (part: Part, scene: any): void => {
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
