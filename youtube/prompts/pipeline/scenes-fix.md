# Scene fix step

A reviewer checked rendered stills of the episode and found problems. Fix them in
the scene code. Other agents fix other files in parallel.

## Inputs

- `{episode_dir}/build/stills-review.json`: findings. Handle only findings whose
  `scene` is one of: {scene_ids}. Fix every `blocker` and as many `minor` items as
  is safe.
- `youtube/remotion/src/episodes/{slug}/{part}.tsx`: the scene code. Edit only this
  file.
- `youtube/prompts/pipeline/scenes.md`: the original rules; keep following them.
- `youtube/remotion/src/episodes/{slug}/layout.ts`: shared geometry (read only).
- `{episode_dir}/storyboard.yaml`, `{episode_dir}/script.yaml`, `{episode_dir}/claims.json`.
- `youtube/remotion/src/design/`: design-system API (read only).

## Task

1. Fix the findings in `{part}.tsx`.
2. `npm --prefix youtube/remotion run typecheck` must pass (errors in other part
   files are not yours).
3. Re-render your scenes: `uv run odczyt stills {episode} --scenes {scene_ids}` and
   read the new stills to confirm each fix.

Reply with one line per finding: still, fixed or not, and why.
