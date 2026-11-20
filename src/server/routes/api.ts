import { Hono } from 'hono';
import { context, reddit } from '@devvit/web/server';
import type { Context } from 'hono';
import type { ErrorResponse } from '../../shared/api';
import { dayKeyUTC } from '../../shared/game';
import { redisStore } from '../core/redis-store';
import { applyVote, readInit, readRecord } from '../core/session';

export const api = new Hono();

const error = (c: Context, message: string): Response =>
  c.json<ErrorResponse>({ status: 'error', message }, 400);

api.get('/init', async (c) => {
  if (!context.postId) return error(c, 'postId is required');
  try {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    return c.json(await readInit(redisStore(), username, dayKeyUTC()));
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return error(c, `init failed: ${message}`);
  }
});

api.post('/submit', async (c) => {
  if (!context.postId) return error(c, 'postId is required');
  const body = await c.req.json<{ motion?: unknown }>();
  const choice = typeof body.motion === 'number' ? body.motion : -1;
  if (!Number.isInteger(choice) || choice < 0 || choice > 2) {
    return error(c, 'motion must be 0, 1 or 2');
  }
  try {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    return c.json(
      await applyVote(redisStore(), username, dayKeyUTC(), choice)
    );
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return error(c, `submit failed: ${message}`);
  }
});

api.get('/record', async (c) => {
  if (!context.postId) return error(c, 'postId is required');
  try {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    return c.json(await readRecord(redisStore(), username, dayKeyUTC()));
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return error(c, `record failed: ${message}`);
  }
});
