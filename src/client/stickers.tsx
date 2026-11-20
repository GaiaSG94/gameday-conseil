/* Sticker furniture from the locked style: selection frame handles and the
   little cursor that points at the motion you tabled. */

export const Handles = () => (
  <>
    <s />
    <s />
    <s />
    <s />
  </>
);

export const Cursor = () => (
  <svg
    className="cur"
    width="22"
    height="26"
    viewBox="0 0 22 26"
    aria-hidden="true"
    focusable="false"
  >
    <path
      d="M2 2l16 10-7 1.5 4 8-3 1.5-4-8-6 5z"
      fill="#151515"
      stroke="#fff"
      strokeWidth="1.5"
      strokeLinejoin="round"
    />
  </svg>
);
