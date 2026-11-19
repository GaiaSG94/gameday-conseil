import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
  CONTEXTS,
  DAY_MS,
  dayKeyUTC,
  dailySeed,
  generateSession,
  LINES,
  publicSession,
  shuffle,
} from './game.ts';

const days = (count: number, start = '2026-12-01') =>
  Array.from({ length: count }, (_, i) =>
    dayKeyUTC(new Date(Date.parse(start + 'T00:00:00Z') + i * DAY_MS))
  );

test('seed deterministe et stable', () => {
  assert.equal(dailySeed('2026-12-01'), dailySeed('2026-12-01'));
  assert.notEqual(dailySeed('2026-12-01'), dailySeed('2026-12-02'));
});

test('la session du jour est deterministe', () => {
  assert.deepEqual(generateSession('2026-12-01'), generateSession('2026-12-01'));
});

test('jour cle UTC au format ISO', () => {
  assert.equal(dayKeyUTC(new Date('2026-12-09T23:59:59Z')), '2026-12-09');
  assert.equal(dayKeyUTC(new Date('2026-12-10T00:00:01Z')), '2026-12-10');
});

test('365 jours : gagnant unique, 3 motions, 6 avis, 6 soutiens', () => {
  const tally = [0, 0, 0];
  for (const day of days(365)) {
    const s = generateSession(day);
    assert.equal(s.motions.length, 3, day);
    assert.equal(s.opinions.length, 6, day);
    assert.equal(s.stances.length, 6, day);
    assert.ok(s.winner >= 0 && s.winner <= 2, day);
    assert.ok(
      s.counts.every((count) => count >= 0) && s.counts.reduce((a, b) => a + b, 0) === 6,
      day
    );
    assert.ok(
      s.counts.every((count, i) => i === s.winner || count < (s.counts[s.winner] ?? 0)),
      `gagnant non unique le ${day}: ${s.counts.join(',')}`
    );
    assert.ok(s.stances.every((stance) => stance >= 0 && stance <= 2), day);
    assert.equal(s.supporters.length, s.counts[s.winner], day);
    for (const opinion of s.opinions) {
      assert.ok(opinion.text.length > 10, `${day} ${opinion.id}`);
    }
    tally[s.winner] = (tally[s.winner] ?? 0) + 1;
  }
  assert.ok(tally.every((n) => n > 90), `gagnants mal repartis: ${tally.join(',')}`);
});

test('les avis collent au voisin et a sa motion', () => {
  const s = generateSession('2026-12-09');
  for (let i = 0; i < s.neighbors.length; i++) {
    const neighbor = s.neighbors[i];
    const stance = s.stances[i];
    const opinion = s.opinions.find((o) => o.id === neighbor?.id);
    if (!neighbor || stance === undefined || !opinion) continue;
    assert.equal(opinion.text, LINES[neighbor.id]?.[stance]);
  }
  assert.ok(CONTEXTS.includes(s.context));
});

test('le contenu varie d un jour a l autre', () => {
  const all = days(30).map((day) => {
    const s = generateSession(day);
    return JSON.stringify([s.stances, s.context]);
  });
  assert.ok(new Set(all).size >= 25);
});

test('publicSession ne divulgue ni gagnant ni soutiens', () => {
  const pub = publicSession(generateSession('2026-12-01')) as Record<string, unknown>;
  assert.ok(!('winner' in pub));
  assert.ok(!('stances' in pub));
  assert.ok(!('counts' in pub));
  assert.ok(!('supporters' in pub));
  assert.equal(JSON.stringify(pub).includes('"winner"'), false);
});

test('melange seede deterministe et sans perte', () => {
  const a = shuffle([1, 2, 3, 4, 5, 6], dailySeed('2026-12-01'));
  const b = shuffle([1, 2, 3, 4, 5, 6], dailySeed('2026-12-01'));
  assert.deepEqual(a, b);
  assert.deepEqual([...a].sort(), [1, 2, 3, 4, 5, 6]);
});
