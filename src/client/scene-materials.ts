/* eslint-disable @typescript-eslint/no-explicit-any -- vendor three.module.js
   is untyped (shorthand ambient module): its objects are intentionally any */
import * as THREE from './vendor/three.module.js';

export const INK = 0x151515;
export const CLAY = 0xf6f2e9;
export const ORANGE = 0xff5a1f;
export const LOT_COLOR = 0xe8dcc2;

export type Mats = {
  toon: (color: number | string | undefined) => any;
  outline: any;
};
export type Part = (geo: unknown, color: unknown, outlined?: boolean) => any;

/* Three-step toon ramp: lit / mid / shade, like inked clay. */
export const buildMaterials = (): Mats => {
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

export const makePart = (mat: Mats): Part => (geo, color, outlined = true) => {
  const m = new THREE.Mesh(geo as never, mat.toon(color as number));
  m.castShadow = true;
  if (outlined) m.add(new THREE.Mesh(geo as never, mat.outline));
  return m;
};

export const inkMaterial = (): any => new THREE.MeshBasicMaterial({ color: INK });
export const whiteMaterial = (): any => new THREE.MeshBasicMaterial({ color: 0xffffff });
