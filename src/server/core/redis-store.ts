/* Devvit Redis bound to the Store contract. */
import { redis } from '@devvit/web/server';
import type { Store } from './store';

export const redisStore = (): Store => ({
  get: async (key) => (await redis.get(key)) ?? null,
  set: async (key, value) => {
    await redis.set(key, value);
  },
  incr: (key, by = 1) => redis.incrBy(key, by),
});
