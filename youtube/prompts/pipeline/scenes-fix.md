# Scene fix step

A reviewer checked rendered stills of the episode and found problems. Fix them in
the scene code.

## Inputs

- `{episode_dir}/build/stills-review.json`: findings; fix every `blocker` and as many
  `minor` items as is safe.
- `youtube/remotion/src/episodes/{slug}/part*.tsx`: scene code. Edit only these files.
- `youtube/prompts/pipeline/scenes.md`: the original rules; keep following them.
- `{episode_dir}/storyboard.yaml`, `{episode_dir}/script.yaml`, `{episode_dir}/claims.json`.
- `youtube/remotion/src/design/`: design-system API (read only).

## Task

1. Fix the findings in the part files.
2. `npm --prefix youtube/remotion run typecheck` must pass.
3. Re-render the affected scenes:
   `uv run python scripts/render_episode.py stills {episode} --scenes <ids>` and read
   the new stills to confirm each fix.

Reply with one line per finding: still, fixed or not, and why.
