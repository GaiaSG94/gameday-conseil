import './base.css';
import './game.css';

import { requestExpandedMode } from '@devvit/web/client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import type { InitResponse, SubmitResponse } from '../shared/api';
import { EndCard } from './endcard';
import { dateLabel } from './format';
import { mountScene } from './scene';
import type { SceneHandle } from './scene';
import { Cursor, Handles } from './stickers';

const RESULT_VIEW = { cam: [12.6, 9.2] as [number, number], target: [1.75, 0.15, -0.2] as [number, number, number] };

export const Game = () => {
  const [init, setInit] = useState<InitResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [choice, setChoice] = useState<number | null>(null);
  const [sub, setSub] = useState<SubmitResponse | null>(null);
  const [sending, setSending] = useState(false);
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
      const handle = mountScene(hostRef.current, {
        mode: 'game',
        cast: init.neighbors,
        tints,
        current: init.result ? init.result.choice : null,
        yes: init.backers,
      });
      sceneRef.current = handle;
      if (init.result) handle.setView(RESULT_VIEW);
    } catch {
      /* WebGL unavailable: the .nogl message stays visible */
    }
    return () => {
      sceneRef.current?.dispose();
      sceneRef.current = null;
    };
  }, [init]);

  const send = async () => {
    if (choice === null || sending) return;
    setSending(true);
    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ motion: choice }),
      });
      const data = await res.json();
      if (data.status === 'error') throw new Error(data.message);
      const response = data as SubmitResponse;
      setSub(response);
      sceneRef.current?.setChoice(response.result.choice);
      sceneRef.current?.setYes(response.backers);
      sceneRef.current?.setView(RESULT_VIEW);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'submit failed');
    } finally {
      setSending(false);
    }
  };

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

  const result = sub?.result ?? init.result;
  const voted = Boolean(result);
  const backers = sub ? sub.backers : (init.backers ?? []);
  const community = sub ? sub.community : init.community;
  const neighbors = init.neighbors;
  const opinions = init.opinions;

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
            <button
              className="meta-btn"
              onClick={(e) => requestExpandedMode(e.nativeEvent, 'series')}
              title="Your record"
            >
              <b>{(result ?? { streak: init.streak }).streak}-day streak</b>
            </button>
          </div>
          {voted ? (
            <EndCard init={init} result={result!} backers={backers} community={community} />
          ) : (
            <>
              <h1 className="title">
                Tonight:{' '}
                <span className="sel">
                  the empty lot
                  <Handles />
                </span>
              </h1>
              <p className="rule">
                Six neighbors, one lot.{' '}
                <b>Pick the motion most of them will back.</b>
              </p>
              <span className="tag">The lot, today</span>
              {opinions.map((opinion) => {
                const i = neighbors.findIndex((neighbor) => neighbor.id === opinion.id);
                return (
                  <p
                    key={opinion.id}
                    data-i={i}
                    data-side={i < 3 ? 'l' : 'r'}
                    className={`bub ${i < 3 ? 'l' : 'r'}`}
                  >
                    {opinion.text}
                    <em>
                      <i style={{ background: opinion.tint }} />
                      {opinion.name} · {opinion.role}
                    </em>
                  </p>
                );
              })}
              <div className="motions">
                {init.motions.map((motion, i) => (
                  <button
                    key={motion.id}
                    className={`motion${choice === i ? ' chosen' : ''}`}
                    onClick={() => {
                      setChoice(i);
                      sceneRef.current?.setChoice(i);
                    }}
                  >
                    <i>{motion.id}</i>
                    <b>{motion.title}</b>
                    <span>{motion.detail}</span>
                    <span className="frame">
                      <s />
                      <s />
                      <s />
                      <s />
                    </span>
                    <Cursor />
                  </button>
                ))}
              </div>
              <div className="foot">
                <p>
                  {community[0]! + community[1]! + community[2]!} neighbors have voted today
                </p>
                <button
                  className="cta"
                  disabled={choice === null || sending}
                  onClick={() => void send()}
                >
                  {sending ? 'Counting…' : 'Call the vote'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Game />
  </StrictMode>
);
