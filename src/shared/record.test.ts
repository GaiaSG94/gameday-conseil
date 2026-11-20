import assert from 'node:assert/strict';
import { test } from 'node:test';

import type { RecordDay } from './record.ts';
import { buildRecord } from './record.ts';

const cast = [
  { id: 'ines', name: 'Ines', role: 'bakery', tint: '#f6c9b5' },
  { id: 'theo', name: 'Theo', role: 'dad', tint: '#bfd6e8' },
];

const day = (overrides: Partial<RecordDay>): RecordDay => ({
  day: '2026-11-13',
  session: 320,
  context: 'The lease runs out in ninety days.',
  winner: 0,
  counts: [3, 2, 1],
  stancesById: { ines: 0, theo: 1 },
  choice: null,
  ...overrides,
});


test('a played day yields the true score and win of that day', () => {
  const record = buildRecord({
    neighbors: cast,
    days: [day({ choice: 1 })],
    community: [{ score: 0, votes: 0 }],
  });
  const row = record.sessions[0]!;
  assert.equal(row.choice, 1);
  assert.equal(row.score, 2);
  assert.equal(row.won, false);
  assert.equal(record.played, 1);
});

test('regulars count the days they backed the player', () => {
  const record = buildRecord({
    neighbors: cast,
    days: [
      day({ choice: 0 }),
      day({ choice: 0 }),
      day({ day: '2026-11-15', session: 322, choice: null }),
    ],
    community: [{ score: 0, votes: 0 }, { score: 0, votes: 0 }, { score: 0, votes: 0 }],
  });
  const ines = record.regulars.find((r) => r.id === 'ines')!;
  const theo = record.regulars.find((r) => r.id === 'theo')!;
  assert.equal(ines.backed, 2);
  assert.equal(theo.backed, 0);
  assert.equal(record.played, 2);
});

test('average is the mean score of played sessions', () => {
  const record = buildRecord({
    neighbors: cast,
    days: [day({ choice: 0 }), day({ day: '2026-11-14', session: 321, counts: [4, 2, 0], stancesById: { ines: 0, theo: 0 }, choice: 0 })],
    community: [{ score: 0, votes: 0 }, { score: 0, votes: 0 }],
  });
  assert.equal(record.average, 3.5);
});

test('neighborhood average is the score sum over the vote count', () => {
  const record = buildRecord({
    neighbors: cast,
    days: [day({})],
    community: [
      { score: 3, votes: 1 },
      { score: 4, votes: 2 },
      { score: 0, votes: 1 },
    ],
  });
  assert.equal(record.neighborhood.votes, 4);
  assert.equal(record.neighborhood.average, 1.8);
});

test('no votes at all: averages stay null, not zero', () => {
  const record = buildRecord({
    neighbors: cast,
    days: [day({})],
    community: [{ score: 0, votes: 0 }],
  });
  assert.equal(record.average, null);
  assert.equal(record.neighborhood.average, null);
  assert.equal(record.neighborhood.votes, 0);
});
