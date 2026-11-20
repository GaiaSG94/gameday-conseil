/* Local preview bench for the council: serves the built client and the real
   server logic over an in-memory store, so every screen can be captured with
   the real generator and the real API shapes (no Devvit account needed).

   Run: node --experimental-strip-types --import ./tools/preview/resolve-ts.mjs \
          tools/preview/server.ts [port]
*/
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

import { dailySeed, dayKeyUTC, generateSession, mulberry32 } from '../../src/shared/game.ts';
import { memoryStore } from '../../src/server/core/store.ts';
import { applyVote, readInit, readRecord } from '../../src/server/core/session.ts';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const CLIENT = join(ROOT, 'dist', 'client');
const PORT = Number(process.argv[2] ?? 5177);
const USER = 'Gaia';

const TYPES: Record<string, string> = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.woff2': 'font/woff2',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
};

const BOOTSTRAP = `<script>globalThis.devvit={context:{postId:'t3_preview',username:'Gaia',subredditName:'gameday-preview'},entrypoints:{default:'/splash.html',splash:'/splash.html',game:'/game.html',series:'/series.html'},token:'preview'};</script>`;

type Store = ReturnType<typeof memoryStore>;

/* The neighborhood voted: every day, a plausible split of the three motions. */
const seedCommunity = async (store: Store, day: string): Promise<void> => {
  const session = generateSession(day);
  const rand = mulberry32(dailySeed(day) ^ 0x5f5f);
  const total = 180 + Math.floor(rand() * 140);
  const tally = [0, 0, 0];
  for (let i = 0; i < total; i++) {
    const pick = Math.floor(rand() * 3);
    tally[pick] = (tally[pick] ?? 0) + 1;
  }
  let scoreSum = 0;
  tally.forEach((count, i) => {
    scoreSum += count * (session.counts[i] ?? 0);
  });
  await Promise.all([
    store.set(`tally:${day}:0`, String(tally[0])),
    store.set(`tally:${day}:1`, String(tally[1])),
    store.set(`tally:${day}:2`, String(tally[2])),
    store.set(`votes:${day}`, String(total)),
    store.set(`scoresum:${day}`, String(scoreSum)),
  ]);
};

/* A believable week: the player played six sessions, the neighborhood voted
   every day. Same generator and same keys as production. */
const seed = async (store: Store): Promise<void> => {
  const today = dayKeyUTC();
  for (let back = 6; back >= 1; back--) {
    const day = dayKeyUTC(new Date(Date.now() - back * 86400000));
    const rand = mulberry32(dailySeed(day));
    const session = generateSession(day);
    const choice = rand() < 0.6 ? session.winner : Math.floor(rand() * 3);
    await applyVote(store, USER, day, choice);
    await seedCommunity(store, day);
  }
  await seedCommunity(store, today);
};

const json = (
  res: { writeHead: (code: number, head: Record<string, string>) => void; end: (body: string) => void },
  code: number,
  body: unknown
): void => {
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(body));
};

const serveStatic = async (
  res: { writeHead: (code: number, head: Record<string, string>) => void; end: (body: string) => void },
  path: string
): Promise<void> => {
  const clean = normalize(path).replace(/^([/\\])+/, '');
  const file = join(CLIENT, clean === '' ? 'splash.html' : clean);
  try {
    const body = await readFile(file);
    const type = TYPES[extname(file)] ?? 'application/octet-stream';
    const out = type.startsWith('text/html')
      ? Buffer.from(body.toString('utf8').replace('</head>', `${BOOTSTRAP}</head>`))
      : body;
    res.writeHead(200, { 'Content-Type': type });
    res.end(out);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('not found');
  }
};

const main = async (): Promise<void> => {
  let store = memoryStore();
  await seed(store);
  createServer(async (req, res) => {
    const url = new URL(req.url ?? '/', 'http://localhost');
    if (url.pathname === '/api/reset' && req.method === 'POST') {
      store = memoryStore();
      await seed(store);
      json(res, 200, { status: 'ok' });
      return;
    }
    if (url.pathname === '/api/init') {
      json(res, 200, await readInit(store, USER, dayKeyUTC()));
      return;
    }
    if (url.pathname === '/api/submit' && req.method === 'POST') {
      const chunks: Buffer[] = [];
      for await (const chunk of req) chunks.push(chunk as Buffer);
      const body = JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
      const motion = typeof body.motion === 'number' ? body.motion : -1;
      if (!Number.isInteger(motion) || motion < 0 || motion > 2) {
        json(res, 400, { status: 'error', message: 'motion must be 0, 1 or 2' });
        return;
      }
      json(res, 200, await applyVote(store, USER, dayKeyUTC(), motion));
      return;
    }
    if (url.pathname === '/api/record') {
      json(res, 200, await readRecord(store, USER, dayKeyUTC()));
      return;
    }
    await serveStatic(res, url.pathname);
  }).listen(PORT, () => {
    console.log(`preview conseil sur http://127.0.0.1:${PORT}/`);
  });
};

await main();
