/* Small text helpers shared by the screens. */

const pad = (value: number): string => String(value).padStart(2, '0');

export const dateLabel = (day: string): string =>
  new Date(day + 'T00:00:00Z').toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  });

export const weekdayLabel = (day: string): string =>
  new Date(day + 'T00:00:00Z').toLocaleDateString('en-US', {
    weekday: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  });

export const countdown = (nextAt: number, now: number): string => {
  if (!now) return '';
  const ms = Math.max(0, nextAt - now);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  return `Next session in ${h} h ${pad(m)} min`;
};
