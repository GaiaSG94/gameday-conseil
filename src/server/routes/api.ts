import { Hono } from 'hono';
import { context, redis, reddit } from '@devvit/web/server';
import type { Context } from 'hono';
import type { ErrorResponse, InitResponse, SubmitResponse } from '../../shared/api';
import { DAY_MS, dayKeyUTC, generateSession, publicSession } from '../../shared/game';
import { resolveVote } from '../../shared/vote';
import type { Result } from '../../shared/vote';
import type { Session } from '../../shared/game';

export const api = new Hono();

const HISTORY_DAYS = 7;

const yesterdayKey = (): string => dayKeyUTC(new Date(Date.now() - DAY_MS));

const error = (c: Context, message: string): Response =>
  c.json<ErrorResponse>({ status: 'error', message }, 400);

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

const bestOf = (best: number, streak: number): number => Math.max(best, streak);

const handleInit = async (c: Context): Promise<Response> => {
  if (!context.postId) return error(c, 'postId is required');
  try {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    const day = dayKeyUTC();
    const session = generateSession(day);
    const [streakRaw, solvedRaw, resultRaw, histRaw, bestRaw, a, b, d] =
      await Promise.all([
        redis.get(`streak:${username}`),
        redis.get(`solved:${username}:${day}`),
        redis.get(`result:${username}:${day}`),
        redis.get(`hist:${username}`),
        redis.get(`best:${username}`),
        redis.get(`tally:${day}:0`),
        redis.get(`tally:${day}:1`),
        redis.get(`tally:${day}:2`),
      ]);
    const votedToday = solvedRaw === '1';
    const stored = votedToday ? readResult(resultRaw) : null;
    const choice = stored ? stored.choice : 0;

    return c.json<InitResponse>({
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
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return error(c, `init failed: ${message}`);
  }
};

const handleSubmit = async (c: Context): Promise<Response> => {
  if (!context.postId) return error(c, 'postId is required');
  const body = await c.req.json<{ motion?: unknown }>();
  const choice = typeof body.motion === 'number' ? body.motion : -1;
  if (!Number.isInteger(choice) || choice < 0 || choice > 2) {
    return error(c, 'motion must be 0, 1 or 2');
  }

  try {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    const day = dayKeyUTC();
    const session = generateSession(day);
    const [streakRaw, lastDayRaw, solvedRaw, resultRaw, histRaw, bestRaw, a, b, d] =
      await Promise.all([
        redis.get(`streak:${username}`),
        redis.get(`lastday:${username}`),
        redis.get(`solved:${username}:${day}`),
        redis.get(`result:${username}:${day}`),
        redis.get(`hist:${username}`),
        redis.get(`best:${username}`),
        redis.get(`tally:${day}:0`),
        redis.get(`tally:${day}:1`),
        redis.get(`tally:${day}:2`),
      ]);
    const outcome = resolveVote({
      day,
      choice,
      solvedToday: solvedRaw === '1',
      stored: readResult(resultRaw),
      priorStreak: readCount(streakRaw),
      lastDay: lastDayRaw ?? null,
      yesterday: yesterdayKey(),
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
      best = bestOf(best, outcome.result.streak);
      await Promise.all([
        redis.set(`streak:${username}`, String(outcome.result.streak)),
        redis.set(`lastday:${username}`, outcome.lastDay),
        redis.set(`solved:${username}:${day}`, '1'),
        redis.set(`result:${username}:${day}`, JSON.stringify(outcome.result)),
        redis.set(`hist:${username}`, history.join('')),
        redis.set(`best:${username}`, String(best)),
        redis.set(`tally:${day}:${choice}`, String(community[choice])),
      ]);
    }

    return c.json<SubmitResponse>({
      type: 'submit',
      result: outcome.result,
      backers: backersOf(session, choice),
      history,
      best,
      community,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return error(c, `submit failed: ${message}`);
  }
};

api.get('/init', handleInit);
api.post('/submit', handleSubmit);
