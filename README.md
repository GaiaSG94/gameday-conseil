# Council — gameday-conseil

A daily Reddit mini-game built on Devvit Web. Chair the neighborhood council:
six neighbors argue about the empty lot, you read their opinions and table the
motion that most of them will back.

**Council — Session N · Tonight: the empty lot.**

## How to play

1. Open the post in the feed. The splash shows today's session, the community
   turnout and your streak.
2. Tap **Take the chair** to expand the game. Six neighbors stand around the
   empty lot, each in a speech bubble explaining what they want (gardens, a
   play court, bike racks, a levy, quiet after dark…).
3. Pick one of three motions — **A** community garden, **B** play court &
   racks, **C** shared lot. Choosing a motion builds it in orange on the lot.
4. **Call the vote.** Your motion is scored by how many of the six neighbors
   support it (x/6). The winner is decided by the daily seed and is unique:
   the best possible score is 4/6 or 3/6, never 6/6.
5. The end card shows who backed you (arms raised in the scene), the best
   motion of the day, the community split, your streak, your best streak and a
   one-tap comment hook ("Ruth said no. Make your case.").

## Daily loop

- One session per day, identical for every player: the seed is
  `conseil:<UTC day>` hashed (FNV-1a) and fed to mulberry32, fully
  deterministic and timezone-independent.
- One vote per day. Voting again the same day returns your stored result and
  never touches your streak.
- A win extends your streak only if you voted yesterday; a miss or a skipped
  day resets it to 0.
- Community tallies count each player once per day.

## Reddit-y layer

- Streaks and a personal best, stored server-side in Redis.
- The last seven sessions as a win/loss strip.
- The community split of today's vote, with your choice highlighted.
- A comment hook that names a dissenting neighbor.

## Tech

- **Client**: React 19 + Vite, hand-written CSS (cream/ink/orange "Quartier 3D"
  style), embedded Three.js 0.170.0 (MIT) rendering a claymation 3D scene with
  toon shading and ink outlines. No network requests from the client.
- **Server**: Hono on Devvit Web (`@devvit/web/server`), Redis for streaks,
  per-day results, history, best and community tallies. The server never sends
  the winner or the support map before the player has voted.
- **Shared**: deterministic daily generator (`src/shared/game.ts`) and the
  vote/streak rules (`src/shared/vote.ts`), imported by both sides.
- Fonts: Archivo (variable, OFL) and DM Mono (OFL), embedded locally.

## Development

```sh
npm install
npm run dev          # playtest on a dev subreddit
npm test             # unit tests (node --test)
npm run test:types   # tsc --build
npm run lint         # eslint
npm run build        # vite build
```

Upload with `npm run deploy` (requires a Devvit account and an approved
playtest subreddit). The app is submitted as a private app: do not publish it
while the hackathon is running.

## License

MIT. Third-party assets keep their own licenses (Three.js MIT, Archivo and
DM Mono SIL OFL).
