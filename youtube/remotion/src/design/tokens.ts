// Source of truth for the visual style; docs/design/visual-style.md explains it.
export type ThemeName = "dark" | "light";

export type Theme = {
  name: ThemeName;
  canvas: string;
  surface: string;
  inset: string;
  line: string;
  ink: string;
  muted: string;
  heading: string;
  glow: string;
  success: string;
  successSoft: string;
  danger: string;
  leader: string;
  candidate: string;
  c3: string;
  onRole: string;
  brandTint: string;
  brandInk: string;
};

export const THEMES: Record<ThemeName, Theme> = {
  dark: {
    name: "dark",
    canvas: "#0E1B17",
    surface: "#16261F",
    inset: "#1E3029",
    line: "#2B4038",
    ink: "#F7E6E3",
    muted: "#A9B3AE",
    heading: "#F4C6CC",
    glow: "rgba(244, 198, 204, 0.55)",
    success: "#6FBF97",
    successSoft: "#183A2C",
    danger: "#F08A7E",
    leader: "#DC5C8A",
    candidate: "#BF8530",
    c3: "#4F97CF",
    onRole: "#0E1B17",
    brandTint: "#F4C6CC",
    brandInk: "#1F3B33",
  },
  light: {
    name: "light",
    canvas: "#F8E9E6",
    surface: "#FFF7F5",
    inset: "#F1DAD6",
    line: "#E6CBC6",
    ink: "#1F3B33",
    muted: "#59635E",
    heading: "#1F3B33",
    glow: "rgba(180, 36, 93, 0.35)",
    success: "#276B4E",
    successSoft: "#D9ECDF",
    danger: "#A3322A",
    leader: "#B4245D",
    candidate: "#A3620C",
    c3: "#1F6FAE",
    onRole: "#FFF7F5",
    brandTint: "#F4C6CC",
    brandInk: "#1F3B33",
  },
};

export const WIDTH = 1920;
export const HEIGHT = 1080;
export const FPS = 30;
export const MARGIN = 96;
export const DIM = 0.3;

/** Center of cell (col, row) of the 6×6 layout grid inside the safe margins; 0-based, fractions allowed. */
export const grid = (col: number, row: number): [number, number] => {
  const cw = (WIDTH - 2 * MARGIN) / 6;
  const ch = (HEIGHT - 2 * MARGIN) / 6;
  return [MARGIN + cw * (col + 0.5), MARGIN + ch * (row + 0.5)];
};

/** Points on a circle, first point at the top, clockwise. */
export const ring = (cx: number, cy: number, r: number, n: number): [number, number][] =>
  Array.from({ length: n }, (_, i) => {
    const a = (-90 + (360 / n) * i) * (Math.PI / 180);
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  });
