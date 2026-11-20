/* The council's server-side logic, independent of the persistence layer
   (Store) so it runs unchanged in Devvit and in local tools. */
import { DAY_MS, NEIGHBORS, dayKeyUTC, generateSession, publicSession } from '../../shared/game';
import type { Session } from '../../shared/game';
import { RECORD_DAYS, buildRecord } from '../../shared/record';
import type { RecordDay } from '../../shared/record';
import type { RegularBase } from '../../shared/record';
import type { RecordResponse } from '../../shared/api';
import { resolveVote } from '../../shared/vote';
import type { Result } from '../../shared/vote';
import type { InitResponse, SubmitResponse } from '../../shared/api';
import type { Store } from './store';

export const HISTORY_DAYS = 7;

const readCount = (raw: string | null | undefined): number => {
  const value = parseInt(raw ?? '0', 10);
  return Number.isFinite(value) && value > 0 ? value : 0;
};

const readHistory = (raw: string | null | undefined): number[] =>
  (raw ?? '')
    .split('')
    .filter((char) => char === '0' || char === '1')
    .map((char) => Number(char))
    .slice(-HISTORY_DAYS);

const readResult = (raw: string | null | undefined): Result | null => {
  if (!raw) return null;
  try {
    const value = JSON.parse(raw) as Result;
    return typeof value?.choice === 'number' && typeof value.streak === 'number'
      ? value
      : null;
  } catch {
    return null;
  }
};

const backersOf = (session: Session, motion: number): string[] =>
  session.neighbors
    .filter((_, i) => session.stances[i] === motion)
    .map((neighbor) => neighbor.id);

const appendHistory = (raw: string | null | undefined, won: boolean): number[] => {
  const chars = (raw ?? '').replace(/[^01]/g, '') + (won ? '1' : '0');
  return readHistory(chars.slice(-HISTORY_DAYS));
};

export const readInit = async (
  store: Store,
  username: string,
  day: string
): Promise<InitResponse> => {
  const session = generateSession(day);
  const [streakRaw, solvedRaw, resultRaw, histRaw, bestRaw, a, b, d] =
    await Promise.all([
      store.get(`streak:${username}`),
      store.get(`solved:${username}:${day}`),
      store.get(`result:${username}:${day}`),
      store.get(`hist:${username}`),
      store.get(`best:${username}`),
      store.get(`tally:${day}:0`),
      store.get(`tally:${day}:1`),
      store.get(`tally:${day}:2`),
    ]);
  const votedToday = solvedRaw === '1';
  const stored = votedToday ? readResult(resultRaw) : null;
  const choice = stored ? stored.choice : 0;
  return {
    type: 'init',
    username,
    streak: readCount(streakRaw),
    votedToday,
    ...publicSession(session),
    result: stored,
    backers: stored ? backersOf(session, choice) : null,
    history: readHistory(histRaw),
    best: readCount(bestRaw),
    community: [readCount(a), readCount(b), readCount(d)],
    startedAt: Date.now(),
    nextAt: Date.parse(day + 'T00:00:00Z') + DAY_MS,
  };
};

export const applyVote = async (
  store: Store,
  username: string,
  day: string,
  choice: number
): Promise<SubmitResponse> => {
  const session = generateSession(day);
  const yesterday = dayKeyUTC(new Date(Date.parse(day + 'T00:00:00Z') - DAY_MS));
  const [streakRaw, lastDayRaw, solvedRaw, resultRaw, histRaw, bestRaw, a, b, d] =
    await Promise.all([
      store.get(`streak:${username}`),
      store.get(`lastday:${username}`),
      store.get(`solved:${username}:${day}`),
      store.get(`result:${username}:${day}`),
      store.get(`hist:${username}`),
      store.get(`best:${username}`),
      store.get(`tally:${day}:0`),
      store.get(`tally:${day}:1`),
      store.get(`tally:${day}:2`),
    ]);
  const outcome = resolveVote({
    day,
    choice,
    solvedToday: solvedRaw === '1',
    stored: readResult(resultRaw),
    priorStreak: readCount(streakRaw),
    lastDay: lastDayRaw ?? null,
    yesterday,
    winner: session.winner,
    counts: session.counts,
    supporters: session.supporters,
  });
  const community = [readCount(a), readCount(b), readCount(d)];
  let history = readHistory(histRaw);
  let best = readCount(bestRaw);

  if (outcome.counted) {
    community[choice] = (community[choice] ?? 0) + 1;
    history = appendHistory(histRaw, outcome.result.won);
    best = Math.max(best, outcome.result.streak);
    await writeVote(store, username, day, choice, outcome.result, history, best, community);
  }

  return {
    type: 'submit',
    result: outcome.result,
    backers: backersOf(session, choice),
    history,
    best,
    community,
  };
};

/* One vote: streaks, idempotence keys, tally and the community score sum. */
const writeVote = async (
  store: Store,
  username: string,
  day: string,
  choice: number,
  result: Result,
  history: number[],
  best: number,
  community: number[]
): Promise<void> => {
  const score = result.score;
  await Promise.all([
    store.set(`streak:${username}`, String(result.streak)),
    store.set(`lastday:${username}`, day),
    store.set(`solved:${username}:${day}`, '1'),
    store.set(`result:${username}:${day}`, JSON.stringify(result)),
    store.set(`hist:${username}`, history.join('')),
    store.set(`best:${username}`, String(best)),
    store.set(`tally:${day}:${choice}`, String(community[choice])),
    store.set(`choice:${username}:${day}`, String(choice)),
    store.incr(`votes:${day}`),
    store.incr(`scoresum:${day}`, score),
  ]);
};

/* The "Séries & quartier" page: seven sessions, regulars, averages. */
export const readRecord = async (
  store: Store,
  username: string,
  day: string
): Promise<RecordResponse> => {
  const days = lastDays(day);
  const [streakRaw, bestRaw, ...rest] = await Promise.all([
    store.get(`streak:${username}`),
    store.get(`best:${username}`),
    ...days.flatMap((d) => [
      store.get(`choice:${username}:${d}`),
      store.get(`scoresum:${d}`),
      store.get(`votes:${d}`),
    ]),
  ]);
  const choices = days.map((_, i) => parseChoice(rest[i * 3]));
  const community = days.map((_, i) => ({
    score: readCount(rest[i * 3 + 1]),
    votes: readCount(rest[i * 3 + 2]),
  }));
  return {
    type: 'record',
    day,
    session: generateSession(day).session,
    streak: readCount(streakRaw),
    best: readCount(bestRaw),
    ...buildRecord({ neighbors: recordNeighbors(), days: recordDays(days, choices), community }),
  };
};

const lastDays = (day: string): string[] =>
  Array.from({ length: RECORD_DAYS }, (_, i) =>
    dayKeyUTC(new Date(Date.parse(day + 'T00:00:00Z') - (RECORD_DAYS - 1 - i) * DAY_MS))
  );

const parseChoice = (raw: string | null | undefined): number | null => {
  const value = raw == null ? NaN : parseInt(raw, 10);
  return Number.isInteger(value) && value >= 0 && value <= 2 ? value : null;
};

const recordNeighbors = (): RegularBase[] =>
  NEIGHBORS.map(({ id, name, role, tint }) => ({ id, name, role, tint }));

const recordDays = (days: string[], choices: (number | null)[]): RecordDay[] =>
  days.map((d, i) => {
    const session = generateSession(d);
    const stancesById: Record<string, number> = {};
    session.neighbors.forEach((neighbor, n) => {
      stancesById[neighbor.id] = session.stances[n] ?? 0;
    });
    return {
      day: d,
      session: session.session,
      context: session.context,
      winner: session.winner,
      counts: session.counts,
      stancesById,
      choice: choices[i] ?? null,
    };
  });
