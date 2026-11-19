import assert from 'node:assert/strict';
import { test } from 'node:test';

import { generateSession } from './game.ts';
import { resolveVote } from './vote.ts';
import type { Result, VoteInput } from './vote.ts';

const base = (day: string): VoteInput => {
  const session = generateSession(day);
  return {
    day,
    choice: session.winner,
    solvedToday: false,
    stored: null,
    priorStreak: 0,
    lastDay: null,
    yesterday: '',
    winner: session.winner,
    counts: session.counts,
    supporters: session.supporters,
  };
};

test('une victoire le jour 1 demarre la serie a 1', () => {
  const input = { ...base('2026-12-01'), yesterday: '2026-11-30' };
  const out = resolveVote(input);
  assert.equal(out.result.won, true);
  assert.equal(out.result.streak, 1);
  assert.equal(out.result.score, input.counts[input.winner]);
  assert.equal(out.counted, true);
});

test('deux jours consecutifs font 2', () => {
  const day1 = resolveVote({ ...base('2026-12-01'), yesterday: '2026-11-30' });
  const day2 = resolveVote({
    ...base('2026-12-02'),
    priorStreak: day1.result.streak,
    lastDay: day1.lastDay,
    yesterday: '2026-12-01',
  });
  assert.equal(day2.result.streak, 2);
});

test('un trou d un jour remet la serie a 1', () => {
  const out = resolveVote({
    ...base('2026-12-04'),
    priorStreak: 6,
    lastDay: '2026-12-02',
    yesterday: '2026-12-03',
  });
  assert.equal(out.result.streak, 1);
});

test('rejouer le meme jour ne change ni serie ni score', () => {
  const stored: Result = {
    choice: 1,
    won: true,
    score: 4,
    streak: 7,
    winner: 1,
    supporters: ['ines', 'sam'],
  };
  const out = resolveVote({
    ...base('2026-12-02'),
    choice: 0,
    solvedToday: true,
    stored,
    priorStreak: 9,
    lastDay: '2026-12-01',
    yesterday: '2026-12-01',
  });
  assert.deepEqual(out.result, stored);
  assert.equal(out.result.streak, 7);
  assert.equal(out.counted, false);
});

test('une defaite remet la serie a 0', () => {
  const input = base('2026-12-03');
  const choice = (input.winner + 1) % 3;
  const out = resolveVote({ ...input, choice });
  assert.equal(out.result.won, false);
  assert.equal(out.result.streak, 0);
  assert.equal(out.result.score, input.counts[choice]);
  assert.equal(out.counted, true);
});

test('le score est le nombre de voisins qui soutiennent le choix', () => {
  const session = generateSession('2026-12-05');
  const out = resolveVote({
    ...base('2026-12-05'),
    choice: (session.winner + 1) % 3,
  });
  assert.equal(out.result.score, session.counts[(session.winner + 1) % 3]);
});
