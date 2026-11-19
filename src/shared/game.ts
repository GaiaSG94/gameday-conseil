export type MotionId = 'A' | 'B' | 'C';

export type Neighbor = {
  id: string;
  name: string;
  role: string;
  tint: string;
  acc: 'toque' | 'kid' | 'cane' | 'helmet' | 'can' | 'cap';
};

export type Motion = {
  id: MotionId;
  title: string;
  detail: string;
};

export type Opinion = {
  id: string;
  name: string;
  role: string;
  tint: string;
  text: string;
};

export type Session = {
  day: string;
  session: number;
  context: string;
  motions: Motion[];
  neighbors: Neighbor[];
  opinions: Opinion[];
  stances: number[];
  winner: number;
  counts: number[];
  supporters: string[];
};

export type PublicSession = Pick<
  Session,
  'day' | 'session' | 'context' | 'motions' | 'neighbors' | 'opinions'
>;

export const DAY_MS = 24 * 60 * 60 * 1000;
export const EPOCH = Date.parse('2026-01-01T00:00:00Z');

export const NEIGHBORS: Neighbor[] = [
  { id: 'ines', name: 'Ines', role: 'bakery, no. 4', tint: '#f6c9b5', acc: 'toque' },
  { id: 'theo', name: 'Theo', role: 'dad of three', tint: '#bfd6e8', acc: 'kid' },
  { id: 'ruth', name: 'Ruth', role: 'here since 1984', tint: '#d9cdea', acc: 'cane' },
  { id: 'sam', name: 'Sam', role: 'bike courier', tint: '#bfe0cc', acc: 'helmet' },
  { id: 'odile', name: 'Odile', role: 'garden waitlist', tint: '#f3dc9a', acc: 'can' },
  { id: 'kofi', name: 'Kofi', role: 'owns no. 12', tint: '#d5d6d8', acc: 'cap' },
];

export const MOTIONS: Motion[] = [
  { id: 'A', title: 'Community garden', detail: 'Plots for the waitlist, gate locked at 9 pm.' },
  { id: 'B', title: 'Play court & racks', detail: 'Paved court, bike racks, lit till 11 pm.' },
  { id: 'C', title: 'Shared lot', detail: 'Beds, a play corner, racks. Small owner levy.' },
];

export const CONTEXTS = [
  'The city will match whatever the neighborhood raises.',
  'The lease runs out in ninety days. Decide tonight.',
  'The lot has been empty since the flood two winters ago.',
  'Two hundred signatures are already on the table.',
  'The council will accept one proposal, no amendments.',
  'Another summer of weeds is not an option, they say.',
];

export const LINES: Record<string, [string, string, string]> = {
  ines: [
    "A garden? Keep my six-a.m. delivery lane clear and I'm for it.",
    'A court under my window till eleven? Not the court.',
    'Beds and a lane I can use — that gets my vote.',
  ],
  theo: [
    'Plots are lovely, but my kids want somewhere to kick a ball.',
    'A lit court and racks. They need it more than a flowerbed.',
    'A bit of both, and I can walk there in two minutes.',
  ],
  ruth: [
    'Plants, yes — with a gate at nine it stays quiet. I’m in.',
    'Lit till eleven? Not on my street, thank you.',
    'Quiet after dark is all I ask; a small levy I can accept.',
  ],
  sam: [
    'Nowhere to lock a bike. Count me out of the garden.',
    'Racks and a lit court — I’ll use both every day.',
    'Racks by the entrance, please. Then I’m for the shared lot.',
  ],
  odile: [
    'Two years on the list. Give me a plot — gardens all the way.',
    'A court is fine, but where do I grow things? Not the court.',
    'Beds and a play corner? I’d take that today.',
  ],
  kofi: [
    'A garden is fine as long as owners pay nothing.',
    'Paving that lot costs us owners. Not the court.',
    'A small levy for shared beds I can live with — the shared lot.',
  ],
};

export const dayKeyUTC = (now: Date = new Date()): string =>
  now.toISOString().slice(0, 10);

export const dailySeed = (day: string): number => {
  let hash = 2166136261;
  const input = 'conseil:' + day;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
};

export const mulberry32 = (seed: number): (() => number) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

export const shuffle = <T>(
  items: readonly T[],
  rand: (() => number) | number
): T[] => {
  const next = typeof rand === 'number' ? mulberry32(rand) : rand;
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(next() * (i + 1));
    const a = out[i];
    const b = out[j];
    if (a !== undefined && b !== undefined) {
      out[i] = b;
      out[j] = a;
    }
  }
  return out;
};

export const generateSession = (day: string): Session => {
  const rand = mulberry32(dailySeed(day));
  const session =
    Math.floor((Date.parse(day + 'T00:00:00Z') - EPOCH) / DAY_MS) + 1;
  const context = CONTEXTS[Math.floor(rand() * CONTEXTS.length)] ?? CONTEXTS[0]!;
  const winner = Math.floor(rand() * 3);
  const move = 1 + Math.floor(rand() * 2);
  const counts = [2, 2, 2];
  const donor = (winner + 1) % 3;
  counts[donor] = (counts[donor] ?? 0) - move;
  counts[winner] = (counts[winner] ?? 0) + move;

  const stances = shuffle(
    counts.flatMap((count, motion) => Array<number>(count).fill(motion)),
    rand
  );
  const opinions = NEIGHBORS.map((neighbor, i) => {
    const stance = stances[i] ?? 0;
    return {
      id: neighbor.id,
      name: neighbor.name,
      role: neighbor.role,
      tint: neighbor.tint,
      text: LINES[neighbor.id]?.[stance] ?? '',
    };
  });
  const supporters = NEIGHBORS.filter((_, i) => stances[i] === winner).map(
    (neighbor) => neighbor.id
  );

  return {
    day,
    session,
    context,
    motions: MOTIONS.map((motion) => ({ ...motion })),
    neighbors: NEIGHBORS.map((neighbor) => ({ ...neighbor })),
    opinions: shuffle(opinions, rand),
    stances,
    winner,
    counts,
    supporters,
  };
};

export const publicSession = (session: Session): PublicSession => ({
  day: session.day,
  session: session.session,
  context: session.context,
  motions: session.motions,
  neighbors: session.neighbors,
  opinions: session.opinions,
});
