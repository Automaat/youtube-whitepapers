import type { ThemeName } from "./design/tokens";

export type Speaker = "narrator" | "skeptic";

export type TimelineScene = {
  id: string;
  chapter: string | null;
  /** Seconds from the start of the narration audio. */
  start: number;
  end: number;
  /** Cue name → seconds from the start of the narration audio. */
  cues: Record<string, number>;
};

export type TimelineSegment = {
  id: string;
  speaker: Speaker;
  scene: string;
  start: number;
  end: number;
};

/** Thumbnail art from storyboard.yaml: big term plus one frozen scene frame. */
export type ThumbnailArt = {
  term: string;
  scene: string;
  cue: string;
  tagline?: string;
  /** Region of the 1920×1080 scene to show: [x, y, width, height]. */
  crop?: [number, number, number, number];
};

export type Timeline = {
  slug: string;
  number: number;
  title: string;
  subtitle: string;
  authors: string;
  theme: ThemeName;
  fps: number;
  /** Narration file inside the public dir, or null for a silent preview. */
  audio: string | null;
  audioSeconds: number;
  introSeconds: number;
  outroSeconds: number;
  /** Thumbnail image inside the public dir, or null to use the Thumbnail card. */
  thumbnail: string | null;
  thumbnailArt?: ThumbnailArt | null;
  chapters: { id: string; title: string }[];
  scenes: TimelineScene[];
  segments: TimelineSegment[];
};

export const EMPTY_TIMELINE: Timeline = {
  slug: "73-raft",
  number: 73,
  title: "Raft",
  subtitle: "W poszukiwaniu zrozumiałego algorytmu konsensusu",
  authors: "Diego Ongaro, John Ousterhout · Stanford · 2014",
  theme: "dark",
  fps: 30,
  audio: null,
  audioSeconds: 10,
  introSeconds: 5,
  outroSeconds: 5,
  thumbnail: null,
  thumbnailArt: null,
  chapters: [],
  scenes: [],
  segments: [],
};
