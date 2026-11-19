import type { Motion, Neighbor, Opinion } from './game';
import type { Result } from './vote';

export type ErrorResponse = {
  status: 'error';
  message: string;
};

export type InitResponse = {
  type: 'init';
  day: string;
  username: string;
  streak: number;
  votedToday: boolean;
  session: number;
  context: string;
  motions: Motion[];
  neighbors: Neighbor[];
  opinions: Opinion[];
  result: Result | null;
  backers: string[] | null;
  history: number[];
  best: number;
  community: number[];
  startedAt: number;
  nextAt: number;
};

export type SubmitResponse = {
  type: 'submit';
  result: Result;
  backers: string[];
  history: number[];
  best: number;
  community: number[];
};
