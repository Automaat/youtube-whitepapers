# Script fix step

A fact-checker reviewed `{episode_dir}/script.yaml` against the paper and found
problems that block recording. Fix them.

## Inputs

- `{episode_dir}/paper.txt`: source of truth.
- `{episode_dir}/storyboard.yaml`
- `{episode_dir}/script.yaml`: the script to edit.
- `{episode_dir}/review.json`: the review; fix every item in `must_fix`.
- `youtube/prompts/pipeline/script.md`: the original format and content rules. Keep
  following them.

## Task

Edit `{episode_dir}/script.yaml` in place with the Edit tool. Fix every `must_fix`
item. Use the suggested fix when it is correct; otherwise write a better one that is
true per `paper.txt`. If a fix in the storyboard visuals is needed, edit
`{episode_dir}/storyboard.yaml` too. Keep segment ids stable; keep every cue marker.
Change nothing else.

Reply with one line per fixed item: segment id and what changed.
