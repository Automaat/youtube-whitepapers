import { Easing, interpolate } from "remotion";

const ease = Easing.bezier(0.33, 0, 0.2, 1);

/** 0→1 between `at` and `at + dur` frames, eased, clamped. */
export const progress = (frame: number, at: number, dur = 15): number =>
  interpolate(frame, [at, at + Math.max(1, dur)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

/** 0→1 linear (for timers and real-time motion). */
export const linear = (frame: number, at: number, dur: number): number =>
  interpolate(frame, [at, at + Math.max(1, dur)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

/** Fade + 24 px rise starting at `at`. Spread into an element's style. */
export const enter = (frame: number, at: number, dur = 15): { opacity: number; transform: string } => {
  const p = progress(frame, at, dur);
  return { opacity: p, transform: `translateY(${(1 - p) * 24}px)` };
};

/** Opacity for the active/dim signaling rule: 1 while active, DIM otherwise, with a short crossfade. */
export const focusOpacity = (frame: number, from: number, until = Infinity, dim = 0.3): number => {
  const on = progress(frame, from, 10);
  const off = until === Infinity ? 0 : progress(frame, until, 10);
  return dim + (1 - dim) * Math.max(0, on - off);
};

/** Interpolate a point along a straight line. */
export const along = (x1: number, y1: number, x2: number, y2: number, t: number): [number, number] => [
  x1 + (x2 - x1) * t,
  y1 + (y2 - y1) * t,
];

/** Interpolate a point along a quadratic Bézier curve. */
export const alongCurve = (
  x1: number, y1: number, cx: number, cy: number, x2: number, y2: number, t: number,
): [number, number] => {
  const u = 1 - t;
  return [u * u * x1 + 2 * u * t * cx + t * t * x2, u * u * y1 + 2 * u * t * cy + t * t * y2];
};
