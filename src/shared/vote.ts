export type Result = {
  choice: number;
  won: boolean;
  score: number;
  streak: number;
  winner: number;
  supporters: string[];
};

export type VoteInput = {
  day: string;
  choice: number;
  solvedToday: boolean;
  stored: Result | null;
  priorStreak: number;
  lastDay: string | null;
  yesterday: string;
  winner: number;
  counts: readonly number[];
  supporters: string[];
};

export type VoteOutcome = {
  result: Result;
  lastDay: string;
  counted: boolean;
};

export const resolveVote = (input: VoteInput): VoteOutcome => {
  if (input.solvedToday && input.stored) {
    return {
      result: input.stored,
      lastDay: input.lastDay ?? input.day,
      counted: false,
    };
  }

  const won = input.choice === input.winner;
  const base = input.lastDay === input.yesterday ? input.priorStreak : 0;
  const streak = won ? base + 1 : 0;
  const result: Result = {
    choice: input.choice,
    won,
    score: input.counts[input.choice] ?? 0,
    streak,
    winner: input.winner,
    supporters: input.supporters,
  };
  return { result, lastDay: input.day, counted: true };
};
