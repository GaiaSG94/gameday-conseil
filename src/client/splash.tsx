import './base.css';
import './splash.css';

import { requestExpandedMode } from '@devvit/web/client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import type { InitResponse } from '../shared/api';
import { dateLabel } from './format';
import { mountScene } from './scene';
import type { SceneHandle } from './scene';
import { Handles } from './stickers';

export const Splash = () => {
  const [init, setInit] = useState<InitResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const hostRef = useRef<HTMLDivElement | null>(null);
  const sceneRef = useRef<SceneHandle | null>(null);
  const initRef = useRef<InitResponse | null>(null);

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

  useEffect(() => {
    if (!init || !hostRef.current || sceneRef.current || initRef.current === init) return;
    initRef.current = init;
    const tints: Record<string, string> = {};
    for (const neighbor of init.neighbors) tints[neighbor.id] = neighbor.tint;
    try {
      sceneRef.current = mountScene(hostRef.current, {
        mode: 'post',
        cast: init.neighbors,
        tints,
        current: init.result ? init.result.choice : null,
        yes: null,
        cam: [12.0, 8.4],
        target: [0, 0.1, -0.25],
      });
    } catch {
      /* WebGL unavailable: the .nogl message stays visible */
    }
    return () => {
      sceneRef.current?.dispose();
      sceneRef.current = null;
    };
  }, [init]);

  if (error) {
    return (
      <div className="app">
        <p className="loading">{error}</p>
      </div>
    );
  }
  if (!init) {
    return (
      <div className="app">
        <p className="loading">Convening the council…</p>
      </div>
    );
  }

  const voted = init.community[0]! + init.community[1]! + init.community[2]!;

  return (
    <div className="app">
      <div className="board">
        <div className="scene-host" ref={hostRef}>
          <canvas />
          <p className="nogl">3D is unavailable in this browser (WebGL disabled).</p>
        </div>
        <div className="ui">
          <div className="meta">
            <span>
              Session {init.session} · {dateLabel(init.day)}
            </span>
            {init.streak > 0 && (
              <span>
                <b>{init.streak}-day streak</b>
              </span>
            )}
          </div>
          <h1 className="title">
            Tonight:{' '}
            <span className="sel">
              the empty lot
              <Handles />
            </span>
          </h1>
          <p className="rule">
            Six neighbors are waiting for the chair.{' '}
            <b>One lot, three motions, one vote.</b>
          </p>
          <span className="tag">The lot, today</span>
          {init.neighbors.map((neighbor, i) => (
            <span key={neighbor.id} data-i={i} data-side="t" className="dots">
              …
            </span>
          ))}
          <div className="stk post-stk">
            <div className="grow">
              <p className="k">Today&rsquo;s session</p>
              <p className="post-head">Read six neighbors. Table one motion.</p>
              <p className="post-sub">{init.context}</p>
              <p className="post-sub">
                {voted.toLocaleString('en-US')} neighbors have voted · takes about a minute
              </p>
            </div>
            <button
              className="cta"
              onClick={(e) => requestExpandedMode(e.nativeEvent, 'game')}
            >
              {init.votedToday ? 'See the result' : 'Take the chair'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Splash />
  </StrictMode>
);
