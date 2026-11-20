import { createContext, useContext } from "react";
import { useCurrentFrame } from "remotion";
import type { Speaker } from "../timeline";

export type SceneInfo = {
  id: string;
  /** Scene length in frames. */
  duration: number;
  /** Cue name → frame relative to the scene start. */
  cues: Record<string, number>;
  /** Speaker ranges relative to the scene start, in frames. */
  speakers: { speaker: Speaker; from: number; to: number }[];
};

export const SceneContext = createContext<SceneInfo>({ id: "", duration: 1, cues: {}, speakers: [] });

/**
 * Scene hook for scene components. `cue(name)` returns the frame (relative to the
 * scene start) where the narrator reaches the cue; unknown cues return 0 so the
 * element still shows, and the stills review catches the mismatch.
 */
export const useScene = () => {
  const info = useContext(SceneContext);
  const frame = useCurrentFrame();
  const cue = (name: string): number => info.cues[name] ?? 0;
  const speaker: Speaker =
    info.speakers.find((s) => frame >= s.from && frame < s.to)?.speaker ?? "narrator";
  return { frame, duration: info.duration, cue, speaker, id: info.id };
};
