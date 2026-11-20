/* eslint-disable @typescript-eslint/no-explicit-any -- vendor three.module.js
   is untyped (shorthand ambient module): its objects are intentionally any */
import * as THREE from './vendor/three.module.js';

import type { Neighbor } from '../shared/game';
import { buildDisc, buildNeighbor, buildPassersBy } from './scene-cast';
import type { Neighbor3d } from './scene-cast';
import { buildLot, buildMotions } from './scene-lot';
import { buildMaterials, makePart } from './scene-materials';

export type SceneMode = 'post' | 'game' | 'result' | 'series';

export type SceneOpts = {
  mode: SceneMode;
  cast: Neighbor[];
  tints: Record<string, string>;
  current: number | null;
  yes: string[] | null;
  cam?: [number, number];
  target?: [number, number, number];
  spots?: [number, number][];
  noLot?: boolean;
};

export type SceneHandle = {
  setChoice: (motion: number | null) => void;
  setYes: (ids: string[] | null) => void;
  setView: (view: { cam?: [number, number]; target?: [number, number, number] }) => void;
  dispose: () => void;
};

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

const buildCast = (opts: SceneOpts, part: ReturnType<typeof makePart>, scene: any): Neighbor3d[] => {
  const spots = opts.spots ?? SPOTS;
  return opts.cast.map((neighbor, i) => {
    const spot = spots[i] ?? spots[0]!;
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
    return { id: neighbor.id, g, n, head: n.userData.head, arm: n.userData.arm } as Neighbor3d & { id: string };
  });
};

/* One shared scene for every page (planche gen4): the camera breathes, the
   cast breathes, and choosing a motion builds it on the lot with a spring. */
export const mountScene = (host: HTMLElement, opts: SceneOpts): SceneHandle => {
  const canvas = host.querySelector('canvas') as HTMLCanvasElement;
  /* The stickers live in the overlay sibling of the canvas: anchor against the
     whole board, not only the canvas host. */
  const board = (host.closest('.board') as HTMLElement | null) ?? host;
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
  scene.add(lot.group);
  if (opts.noLot) lot.group.visible = false;
  const motions = buildMotions(part, lot.group);
  const people = buildCast(opts, part, scene);
  if (!opts.noLot) buildPassersBy(part, scene);

  const camRadius = opts.cam?.[0] ?? 12.4;
  const camHeight = opts.cam?.[1] ?? 9.0;
  const target = new THREE.Vector3(...(opts.target ?? [0, 0.15, 0.25]));
  let radius = camRadius;
  let height = camHeight;
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

  const place = (bub: HTMLElement, x: number, y: number, w: number, h: number, k: number): void => {
    const host_ = host.clientWidth || 740;
    const side = bub.dataset.side ?? 'l';
    let left: number;
    let top: number;
    if (side === 't') {
      left = x - w / 2;
      top = y - h - 26 * k;
    } else if (side === 'l') {
      left = x - 44 * k - w;
      top = y - 34 * k;
    } else {
      left = x + 44 * k;
      top = y - 34 * k;
    }
    bub.style.transform = `translate(${Math.round(Math.max(8, Math.min(host_ - w - 8, left)))}px, ${Math.round(top)}px)`;
  };

  const anchor = (): void => {
    const w = host.clientWidth || 740;
    const h = host.clientHeight || 640;
    const k = w / 740;
    const v = new THREE.Vector3();
    board.querySelectorAll<HTMLElement>('[data-i]').forEach((bub) => {
      const i = Number(bub.dataset.i);
      const person = people[i];
      if (!person) return;
      person.head.getWorldPosition(v);
      v.project(cam);
      place(
        bub,
        ((v.x + 1) / 2) * w,
        ((1 - v.y) / 2) * h,
        bub.offsetWidth,
        bub.offsetHeight,
        k
      );
    });
    const tag = board.querySelector<HTMLElement>('.tag');
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
    cam.position.set(Math.sin(a) * radius, height, Math.cos(a) * radius);
    cam.lookAt(target);
    motions.forEach((m, k) => {
      const on = k === choice;
      const s = on ? Math.max(0.001, spring(dt)) : Math.max(0.001, m.scale.x * 0.82);
      m.scale.setScalar(s);
    });
    lot.weeds.visible = choice === null;
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
        p.arm.visible = ids !== null && ids.includes((p as Neighbor3d & { id: string }).id);
        if (p.arm.visible) p.g.rotation.y = 0;
        else p.g.rotation.y = Math.PI * 0.92;
      });
    },
    setView: (view) => {
      if (view.cam) {
        radius = view.cam[0];
        height = view.cam[1];
      }
      if (view.target) target.set(...view.target);
    },
    dispose: () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', resize);
      renderer.dispose();
    },
  };
};

export const letterOf = (motion: number): string =>
  ['A', 'B', 'C'][motion] ?? 'A';
