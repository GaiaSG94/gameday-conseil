import './base.css';
import './endcard.css';
import './series.css';

import { requestExpandedMode } from '@devvit/web/client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import type { RecordResponse } from '../shared/api';
import { weekdayLabel } from './format';
import { mountScene } from './scene';
import type { SceneHandle } from './scene';
import { Handles } from './stickers';

const ACC_OF: Record<string, 'toque' | 'kid' | 'cane' | 'helmet' | 'can' | 'cap'> = {
  ines: 'toque',
  theo: 'kid',
  ruth: 'cane',
  sam: 'helmet',
  odile: 'can',
  kofi: 'cap',
};

const SPOTS: [number, number][] = [
  [-2.75, -0.15],
  [-1.65, -0.15],
  [-0.55, -0.15],
  [0.55, -0.15],
  [1.65, -0.15],
  [2.75, -0.15],
];

const Pips = ({ score, today }: { score: number | null; today: boolean }) => (
  <span className="pips">
    {Array.from({ length: 6 }, (_, k) => (
      <i
        key={k}
        style={{
          background:
            score !== null && k < score
              ? today
                ? 'var(--orange)'
                : 'var(--ink)'
              : 'transparent',
        }}
      />
    ))}
  </span>
);

export const Series = () => {
  const [record, setRecord] = useState<RecordResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const hostRef = useRef<HTMLDivElement | null>(null);
  const sceneRef = useRef<SceneHandle | null>(null);
  const recordRef = useRef<RecordResponse | null>(null);

  const load = useCallback(async () => {
    try {
      const res = await fetch('/api/record');
      const data = await res.json();
      if (data.status === 'error') throw new Error(data.message);
      setRecord(data as RecordResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'load failed');
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    if (!record || !hostRef.current || sceneRef.current || recordRef.current === record) {
      return;
    }
    recordRef.current = record;
    const neighbors = record.regulars.map((regular) => ({
      id: regular.id,
      name: regular.name,
      role: regular.role,
      tint: regular.tint,
      acc: ACC_OF[regular.id] ?? 'cap',
    }));
    const tints: Record<string, string> = {};
    for (const neighbor of neighbors) tints[neighbor.id] = neighbor.tint;
    try {
      sceneRef.current = mountScene(hostRef.current, {
        mode: 'series',
        cast: neighbors,
        tints,
        current: null,
        yes: null,
        noLot: true,
        spots: SPOTS,
        cam: [15.5, 5.2],
        target: [0, -0.95, 0],
      });
    } catch {
      /* WebGL unavailable: the .nogl message stays visible */
    }
    return () => {
      sceneRef.current?.dispose();
      sceneRef.current = null;
    };
  }, [record]);

  if (error) {
    return (
      <div className="app">
        <p className="loading">{error}</p>
      </div>
    );
  }
  if (!record) {
    return (
      <div className="app">
        <p className="loading">Fetching the minutes…</p>
      </div>
    );
  }

  return (
    <div className="app series">
      <div className="board">
        <div className="scene-host" ref={hostRef}>
          <canvas />
          <p className="nogl">3D is unavailable in this browser (WebGL disabled).</p>
        </div>
        <div className="ui">
          <div className="meta">
            <span>Your council record</span>
            <button
              className="meta-btn"
              onClick={(e) => requestExpandedMode(e.nativeEvent, 'game')}
              title="Back to the game"
            >
              <b>Session {record.session}</b>
            </button>
          </div>
          <h1 className="title">
            The{' '}
            <span className="sel">
              regulars
              <Handles />
            </span>
          </h1>
          <p className="rule">
            How often each neighbor backed your motion, last 7 sessions.
          </p>
          {record.regulars.map((regular, i) => (
            <span key={regular.id} data-i={i} data-side="t" className="yn y" style={{ textAlign: 'center' }}>
              <b>{regular.backed}/7</b>
            </span>
          ))}
          <div className="stk streak-stk">
            <p className="k">Streak</p>
            <p className="big" style={{ fontSize: 80, marginTop: 6 }}>
              {record.streak}
            </p>
            <p style={{ fontWeight: 800, fontSize: 14 }}>days in the chair</p>
            <p className="sub">
              Record: <b>{record.best}</b> · Average{' '}
              <b>{record.average === null ? '—' : `${record.average}/6`}</b>
            </p>
            <p className="sub">
              Neighborhood average{' '}
              <b>
                {record.neighborhood.average === null
                  ? '—'
                  : `${record.neighborhood.average}/6`}
              </b>
            </p>
          </div>
          <div className="stk days-stk">
            <p className="k" style={{ marginBottom: 4 }}>
              Last 7 sessions
            </p>
            {record.sessions.map((row) => {
              const today = row.day === record.day;
              return (
                <div key={row.day} className="srow" style={{ fontWeight: today ? 800 : 550 }}>
                  <span className="k" style={{ opacity: today ? 1 : 0.6 }}>
                    #{row.session} · {weekdayLabel(row.day)}
                  </span>
                  <span className="topic">{row.context}</span>
                  <Pips score={row.score} today={today} />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Series />
  </StrictMode>
);
