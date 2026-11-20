/* End card overlay, straight from the locked planche (planches/v4/
   03-carte-de-fin.html): Yes/No labels above the heads in the scene, the
   score as a big sticker, the neighborhood split, a comment hook. */
import './endcard.css';

import { context, navigateTo } from '@devvit/web/client';
import { useEffect, useState } from 'react';

import type { InitResponse, SubmitResponse } from '../shared/api';
import { letterOf } from './scene';
import { countdown } from './format';

const pct = (count: number, total: number): number =>
  total === 0 ? 0 : Math.round((count / total) * 100);

const Split = ({ community, choice }: { community: number[]; choice: number | null }) => {
  const total = community.reduce((a, b) => a + b, 0);
  if (total === 0) return <p className="sub">No votes in yet. Yours was the first.</p>;
  return (
    <>
      {community.map((count, i) => (
        <div key={i} className="spl-row">
          <b>{letterOf(i)}</b>
          <div className={`spl-bar${i === choice ? ' me' : ''}`}>
            <i style={{ width: `${pct(count, total)}%` }} />
          </div>
          <span>{pct(count, total)}%</span>
        </div>
      ))}
    </>
  );
};

export const EndCard = ({
  init,
  result,
  backers,
  community,
}: {
  init: InitResponse;
  result: SubmitResponse['result'];
  backers: string[];
  community: number[];
}) => {
  const [now, setNow] = useState(0);
  useEffect(() => {
    setNow(Date.now());
    const timer = setInterval(() => setNow(Date.now()), 30000);
    return () => clearInterval(timer);
  }, []);

  const reasonOf = (id: string): string =>
    init.opinions.find((opinion) => opinion.id === id)?.text ?? '';
  const dissenter = init.neighbors.find((neighbor) => !backers.includes(neighbor.id));
  const winnerMotion = init.motions[result.winner];
  const total = community.reduce((a, b) => a + b, 0);
  const motion = init.motions[result.choice];

  return (
    <>
      {init.neighbors.map((neighbor, i) => {
        const back = backers.includes(neighbor.id);
        return (
          <span key={neighbor.id} data-i={i} data-side="t" className={`yn ${back ? 'y' : 'n'}`}>
            <b>{back ? 'Yes' : 'No'}</b>
            {reasonOf(neighbor.id)}
          </span>
        );
      })}
      <div className="stk score-stk">
        <p className="k">
          You tabled · {letterOf(result.choice)} · {motion?.title ?? ''}
        </p>
        <p className="big" style={{ fontSize: 92, marginTop: 8 }}>
          {result.score}
          <span style={{ fontSize: 48 }}>/6</span>
        </p>
        <p style={{ fontWeight: 800, fontSize: 15, marginTop: 2 }}>neighbors backed you</p>
        <p className="pips">
          {init.neighbors.map((neighbor) => (
            <i
              key={neighbor.id}
              style={{ background: backers.includes(neighbor.id) ? neighbor.tint : 'var(--white)' }}
            />
          ))}
        </p>
        {!result.won && winnerMotion && (
          <p style={{ fontSize: 12.5, lineHeight: 1.35, marginTop: 10 }}>
            Best motion today: <b>{letterOf(result.winner)} · {winnerMotion.title}</b>, backed
            by <b>{result.supporters.length}/6</b>.
          </p>
        )}
        <div className="divider">
          <p className="k">
            What {total.toLocaleString('en-US')} neighbors tabled
          </p>
          <Split community={community} choice={result.choice} />
        </div>
      </div>
      <div className="stk foot-stk">
        <div className="grow">
          <p className="hook">
            {dissenter ? `${dissenter.name} said no. Make your case.` : 'Unanimous. Say thank you.'}
          </p>
          <p className="sub">
            Your reply goes to the comments, signed with your {result.score}/6.
          </p>
        </div>
        <span className="k">{countdown(init.nextAt, now)}</span>
        <button
          className="cta"
          onClick={() => {
            if (context.postId) navigateTo(`https://reddit.com/comments/${context.postId}`);
          }}
        >
          Comment
        </button>
      </div>
    </>
  );
};
