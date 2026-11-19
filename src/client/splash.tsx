import './index.css';

import { context, requestExpandedMode } from '@devvit/web/client';
import { useCallback, useEffect, useState } from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import type { InitResponse } from '../shared/api';

const dateLabel = (day: string): string =>
  new Date(day + 'T00:00:00Z').toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  });

const Splash = () => {
  const [init, setInit] = useState<InitResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const res = await fetch('/api/init');
      const data = await res.json();
      if (data.status === 'error') throw new Error(data.message);
      setInit(data as InitResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'load failed');
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  if (error) {
    return (
      <div className="splash">
        <p className="mono">{error}</p>
      </div>
    );
  }
  if (!init) {
    return (
      <div className="splash">
        <p className="mono">Convening the council…</p>
      </div>
    );
  }

  const voted = init.community[0]! + init.community[1]! + init.community[2]!;
  const hello = context.username ? ` Hi, ${context.username}.` : '';

  return (
    <div className="splash">
      <p className="mono">
        Council · session {init.session} · {dateLabel(init.day)}
      </p>
      <h1>
        Tonight:
        <br />
        <span className="sel">the empty lot</span>
      </h1>
      <p>
        Six neighbors, three motions, one vote. {init.context}
        {hello}
      </p>
      {init.streak > 0 && <span className="stamp">{init.streak}-day streak</span>}
      <p className="mono">
        {voted} {voted === 1 ? 'neighbor has' : 'neighbors have'} voted · takes
        about a minute
      </p>
      <button
        className="cta"
        onClick={(e) => requestExpandedMode(e.nativeEvent, 'game')}
      >
        {init.votedToday ? 'See the result' : 'Take the chair'}
      </button>
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Splash />
  </StrictMode>
);
