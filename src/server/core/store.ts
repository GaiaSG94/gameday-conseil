/* Key/value persistence behind the council. The server binds the Devvit
   Redis adapter; local tools bind the in-memory one. */
export type Store = {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
  incr(key: string, by?: number): Promise<number>;
};

export const memoryStore = (): Store & { snapshot(): [string, string][] } => {
  const values = new Map<string, string>();
  return {
    get: async (key) => values.get(key) ?? null,
    set: async (key, value) => {
      values.set(key, value);
    },
    incr: async (key, by = 1) => {
      const next = (parseInt(values.get(key) ?? '0', 10) || 0) + by;
      values.set(key, String(next));
      return next;
    },
    snapshot: () => [...values],
  };
};
