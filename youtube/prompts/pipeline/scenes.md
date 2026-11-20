# Scene code step

You write Remotion (React + TypeScript) scene components for one episode of
"Głęboki Odczyt", a Polish YouTube channel that explains papers with animated
diagrams. Narration audio and cue timestamps already exist; your scenes animate on
those cues.

You own exactly one file: `youtube/remotion/src/episodes/{slug}/{part}.tsx`.
It must export `scenes: Record<string, FC>` with these scene ids as keys:
{scene_ids}. Do not edit any other file. Other agents write the other parts in
parallel.

## Read first

- `docs/design/visual-style.md`: binding style rules (palette, type, layout, motion,
  scene vocabulary).
- `docs/design/mockups/raft-style.html`: approved look (SVG primitives, frame layouts).
- `youtube/remotion/src/design/*.ts*`: the design-system API. Import only from
  `"../../design"`, `"react"` and `"remotion"`. Read `scene.tsx`, `svg.tsx`, `ui.tsx`,
  `motion.ts`, `tokens.ts`, `cards.tsx` before writing code.
- `youtube/remotion/src/episodes/{slug}/layout.ts`: shared geometry (ring, lanes, log
  grid). Use it so diagrams that continue across scenes stay in place.
- `{episode_dir}/storyboard.yaml`: your scenes' `visual`, `cues` and `continues_from`.
- `{episode_dir}/script.yaml`: what the narrator says while each scene is on screen.
- `{episode_dir}/claims.json`: verified facts; numbers on screen must match.
- `{episode_dir}/build/public/timeline.json`: real scene lengths and cue times.

## How a scene works

```tsx
import type { FC } from "react";
import { Diagram, RoleNode, enter, progress, useScene, useTheme } from "../../design";

const Hook: FC = () => {
  const { frame, cue, duration } = useScene();   // frame is relative to scene start
  const t = useTheme();
  const crashed = frame >= cue("leader_crash");
  return (
    <Diagram>
      <RoleNode x={960} y={540} label="S1" role={crashed ? "crashed" : "leader"} />
    </Diagram>
  );
};

export const scenes: Record<string, FC> = { hook: Hook };
```

- Every visual change starts at `cue("name")` for a cue listed in the storyboard for
  that scene. Continuous motion (timers, flying messages) starts at a cue and lasts
  15–45 frames (or until the next cue). Use `progress`, `linear`, `enter`,
  `focusOpacity` from the design system.
- The Episode composition already draws: brand mark (top-left), chapter progress
  (top-right), speaker chip (bottom-left), chapter card overlay (first 2.5 s of a
  chapter), the thumbnail over the first 5 s of the video, and the outro. Do not draw
  these yourself.
- Draw diagrams with the SVG primitives inside `<Diagram>`; text blocks and cards
  with the HTML primitives (`Box`, `Card`, `Text`, `Serif`, `ListItem`, `BarChart`…).
  Add small local helpers if needed; do not edit the design system.
- Layout: keep content inside x 96–1824, y 150–960; keep the area x < 520, y > 950
  free for the speaker chip. Text ≥ 22 px. Labels must not overlap nodes, arrows or
  each other. Prefer fewer, larger elements.
- On-screen text in Polish, technical terms in English, max ~12 words of text besides
  labels per scene. Numbers exactly as in `claims.json` (Polish decimal comma: 25,7).
- Signaling: only the element being discussed is at full opacity with glow; others at
  30% (`DIM`). Role colors only via `role` props / theme tokens, never hex literals.
- No comments in code except a short "why" where the logic is not obvious.

## Verify before you finish

1. `npm --prefix youtube/remotion run typecheck` must pass (errors in other part files
   are not yours; report them).
2. Render your stills: `uv run odczyt stills {episode} --scenes <your ids comma-separated>`.
   PNGs land in `{episode_dir}/build/stills/` named `NN-<scene>--<cue>.png`.
3. Read every still of your scenes. Fix overlaps, clipped text, empty frames, wrong
   numbers, elements outside the safe area, and anything that does not match the
   storyboard and the narration. Re-render and re-check after fixes.

Reply with one line per scene: id, status, and anything you could not fix.
