import './index.css';

import { context, navigateTo } from '@devvit/web/client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import type { InitResponse, SubmitResponse } from '../shared/api';
import type { Result } from '../shared/vote';
import { letterOf, mountScene } from './scene';
import type { SceneHandle } from './scene';

const dateLabel = (day: string): string =>
  new Date(day + 'T00:00:00Z').toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  });

const countdown = (nextAt: number, now: number): string => {
  if (!now) return '';
  const ms = Math.max(0, nextAt - now);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  return `Next session in ${h} h ${String(m).padStart(2, '0')} min`;
};

const indexOf = (ids: string[], id: string): number => ids.indexOf(id);

const CommunityBar = ({
  community,
  choice,
}: {
  community: number[];
  choice: number | null;
}) => {
  const total = community.reduce((a, b) => a + b, 0);
  if (total === 0) return <p className="note">No votes yet today. Yours would be first.</p>;
  return (
    <div>
      <div className="bar">
        {community.map((count, i) =>
          count > 0 ? (
            <span
              key={i}
              className={i === choice ? 'mine' : 'other'}
              style={{ width: `${Math.round((count / total) * 100)}%` }}
            />
          ) : null
        )}
      </div>
      <p className="note">
        {community
          .map((count, i) => `${letterOf(i)} ${Math.round((count / total) * 100)}%`)
          .join(' · ')}{' '}
        — {total} {total === 1 ? 'vote' : 'votes'}
      </p>
    </div>
  );
};

const EndCard = ({
  init,
  result,
  backers,
  community,
  history,
  best,
}: {
  init: InitResponse;
  result: Result;
  backers: string[];
  community: number[];
  history: number[];
  best: number;
}) => {
  const [now, setNow] = useState(0);
  useEffect(() => {
    setNow(Date.now());
    const timer = setInterval(() => setNow(Date.now()), 30000);
    return () => clearInterval(timer);
  }, []);

  const dissenter = init.neighbors.find((n) => !backers.includes(n.id));
  const winnerMotion = init.motions[result.winner];

  return (
    <div className="panel">
      <p className="hero">
        {result.score}
        <small>/6</small>
      </p>
      <p className="lede">
        {result.won ? 'The council agreed with you.' : 'The council went another way.'}{' '}
        You tabled {letterOf(result.choice)} ·{' '}
        {init.motions[result.choice]?.title ?? ''}.
      </p>
      <p className="section-title">who backed you</p>
      <div className="split">
        {init.neighbors.map((neighbor) => (
          <span key={neighbor.id} className={`pill${backers.includes(neighbor.id) ? '' : ' no'}`}>
            <i style={{ background: neighbor.tint }} />
            {neighbor.name}
          </span>
        ))}
      </div>
      {!result.won && winnerMotion && (
        <p className="note">
          Best motion today: {letterOf(result.winner)} · {winnerMotion.title}, backed by{' '}
          {result.supporters.length}/6.
        </p>
      )}
      <p className="section-title">streak</p>
      <p className="lede">
        {result.streak > 0 ? `${result.streak}-day streak` : 'Streak broken.'} · best {best}.
      </p>
      <div className="grid7" style={{ maxWidth: 280 }}>
        {history.length === 0 ? <div>-</div> : null}
        {history.map((won, i) => (
          <div key={i} className={won ? 'win' : 'loss'}>
            {won ? 'W' : 'L'}
          </div>
        ))}
      </div>
      <p className="section-title">what the neighborhood tabled</p>
      <CommunityBar community={community} choice={result.choice} />
      <div className="comment">
        <p style={{ fontWeight: 800, fontSize: 15 }}>
          {dissenter ? `${dissenter.name} said no. Make your case.` : 'Unanimous. Say thank you.'}
        </p>
        <span className="mono" style={{ fontSize: 10.5 }}>
          {countdown(init.nextAt, now)}
        </span>
        <button
          className="cta"
          onClick={() => {
            if (context.postId) navigateTo(`https://reddit.com/comments/${context.postId}`);
          }}
        >
          Comment
        </button>
      </div>
    </div>
  );
};

const Game = () => {
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
  const backersShown = sub ? sub.backers : (init.backers ?? []);

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
            <span>
              <b>
                {(result ?? { streak: init.streak }).streak}-day streak
              </b>
            </span>
          </div>
          <h1 className="title">
            Tonight: <span className="sel">the empty lot</span>
          </h1>
          <p className="rule">
            Six neighbors, one lot.{' '}
            <b>Pick the motion most of them will back.</b>
          </p>
          <span className="tag">The lot, today</span>
          {init.opinions.map((opinion) => {
            const i = indexOf(
              init.neighbors.map((n) => n.id),
              opinion.id
            );
            const yes = voted && backersShown.includes(opinion.id);
            return (
              <p
                key={opinion.id}
                data-i={i}
                className={`bub ${i < 3 ? 'l' : 'r'}${yes ? ' yes' : ''}`}
              >
                {opinion.text}
                <em>
                  <i style={{ background: opinion.tint }} />
                  {opinion.name} · {opinion.role}
                </em>
              </p>
            );
          })}
          {!voted && (
            <>
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
                  </button>
                ))}
              </div>
              <div className="foot">
                <p>
                  {init.community[0]! + init.community[1]! + init.community[2]!}{' '}
                  neighbors have voted today
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
      {result && sub && (
        <EndCard
          init={init}
          result={sub.result}
          backers={sub.backers}
          community={sub.community}
          history={sub.history}
          best={sub.best}
        />
      )}
      {result && !sub && (
        <EndCard
          init={init}
          result={init.result!}
          backers={init.backers ?? []}
          community={init.community}
          history={init.history}
          best={init.best}
        />
      )}
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Game />
  </StrictMode>
);
