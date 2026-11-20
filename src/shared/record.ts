/* Record layer of the council (page "Séries & quartier"): pure and free of
   runtime imports, so node --test can load it directly. Callers hand over
   the day data (from the deterministic generator) and static cast facts. */

export const RECORD_DAYS = 7;

export type RegularBase = {
  id: string;
  name: string;
  role: string;
  tint: string;
};

export type Regular = RegularBase & {
  backed: number;
};

export type RecordDay = {
  day: string;
  session: number;
  context: string;
  winner: number;
  counts: readonly number[];
  stancesById: Record<string, number>;
  choice: number | null;
};

export type SessionRow = {
  day: string;
  session: number;
  context: string;
  choice: number | null;
  score: number | null;
  won: boolean | null;
};

export type CouncilRecord = {
  sessions: SessionRow[];
  regulars: Regular[];
  played: number;
  average: number | null;
  neighborhood: { average: number | null; votes: number };
};

export type RecordInput = {
  neighbors: RegularBase[];
  days: RecordDay[];
  community: { score: number; votes: number }[];
};

const round1 = (value: number): number => Math.round(value * 10) / 10;

const playedDays = (days: RecordDay[]): RecordDay[] =>
  days.filter((day) => day.choice !== null && day.choice !== undefined);

const regularsFrom = (input: RecordInput): Regular[] =>
  input.neighbors.map((neighbor) => ({
    ...neighbor,
    backed: playedDays(input.days).filter(
      (day) => day.stancesById[neighbor.id] === day.choice
    ).length,
  }));

const sessionsFrom = (days: RecordDay[]): SessionRow[] =>
  days.map((day) => ({
    day: day.day,
    session: day.session,
    context: day.context,
    choice: day.choice ?? null,
    score:
      day.choice === null || day.choice === undefined
        ? null
        : (day.counts[day.choice] ?? 0),
    won:
      day.choice === null || day.choice === undefined
        ? null
        : day.choice === day.winner,
  }));

export const buildRecord = (input: RecordInput): CouncilRecord => {
  const sessions = sessionsFrom(input.days);
  const played = sessions.filter((row) => row.choice !== null);
  const total = played.reduce((sum, row) => sum + (row.score ?? 0), 0);
  const votes = input.community.reduce((sum, day) => sum + day.votes, 0);
  const score = input.community.reduce((sum, day) => sum + day.score, 0);
  return {
    sessions,
    regulars: regularsFrom(input),
    played: played.length,
    average: played.length ? round1(total / played.length) : null,
    neighborhood: {
      average: votes > 0 ? round1(score / votes) : null,
      votes,
    },
  };
};
