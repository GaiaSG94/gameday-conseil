import { reddit } from '@devvit/web/server';
import { dayKeyUTC, generateSession } from '../../shared/game';

export const createPost = async () => {
  const session = generateSession(dayKeyUTC());
  return await reddit.submitCustomPost({
    title: `Council — Session ${session.session}`,
  });
};
