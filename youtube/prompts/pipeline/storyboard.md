# Storyboard step

You plan one episode of "Głęboki Odczyt", a Polish YouTube channel that explains
research papers with animated diagrams. A narrator explains; a skeptic voice asks
short "why / what if" questions. You write the storyboard only, not the narration.

## Inputs (read all of them before writing)

- `{episode_dir}/episode.yaml`: title, authors, target length.
- `{episode_dir}/paper.txt`: full paper text with `=== page N ===` markers. Source of truth.
- `docs/design/visual-style.md`: visual style, scene vocabulary and layout rules.
- `docs/research/2026-11-visual-explainer-pipeline.md`, section 1: learning rules,
  "Idea type → visual form" table and the 11-step script arc.

## Task

Write `{episode_dir}/storyboard.yaml` that plans a {target_minutes}-minute episode.

Rules:

- Follow the script arc: hook with a concrete failure (never title/authors first),
  problem and stakes, pre-training glossary (3–5 terms, one color each), key insight,
  mechanism built progressively, worked example with toy numbers, results redrawn from
  the paper, limitations, recap. Legacy only if the paper itself states it.
- 5–7 chapters, 2–3 minutes each. Chapter titles in Polish, ≤ 4 words.
- 14–22 scenes. One idea per scene. Each scene holds 20–90 seconds of narration.
- Every scene uses a visual form from the vocabulary in `visual-style.md`. Prefer
  diagrams that move (swimlanes, state machines, logs) over text. A scene never shows
  more than ~12 words of on-screen text besides labels.
- Reuse the same diagram across scenes when the story continues on it (same node
  positions, same colors). Say so in `continues_from`.
- Cues: list the moments where the picture changes. Each cue has a short snake_case
  name and what changes. 2–6 cues per scene. The script writer will place
  `[[cue:name]]` markers in the narration at exactly these moments.
- Every factual element on screen (numbers, rules, figure contents) cites the paper
  page and section in `paper_refs`. Use only facts from `paper.txt`.
- First scene id is `intro` (episode thumbnail is shown; the narrator greets).
  Second scene is the hook. Last scene id is `outro_invite` (recap of the episode in
  one picture + invitation to the next episode).
- All on-screen text is Polish; technical terms stay in English (leader, follower,
  term, log, commit, RequestVote, AppendEntries…).
- Thumbnail: pick the one scene and cue whose frame best shows the paper's central
  mechanism as a diagram (not text, not a chart of numbers). `term` is the name
  viewers search for, at most 10 characters, usually upper case. `tagline` is
  optional, at most 3 Polish words, and must not repeat the title. `crop` frames the
  diagram part of that 1920×1080 frame (x, y, width, height), roughly square.

## Output format

Write the file with the Write tool. YAML, UTF-8, exactly this shape:

```yaml
episode: "{slug}"
chapters:
  - id: c1
    title: "Problem konsensusu"
glossary:
  - term: Leader
    color: leader          # one of: leader, candidate, c3, success, danger, neutral
    definition: "przyjmuje zapisy i rozsyła log"   # ≤ 6 Polish words
thumbnail:
  term: "RAFT"
  tagline: "Kto rządzi?"   # optional
  scene: election
  cue: new_leader
  crop: [500, 160, 860, 860]
scenes:
  - id: hook
    chapter: c1            # intro and outro_invite use chapter: null
    idea: "Jedno zdanie: czego widz ma się nauczyć z tej sceny."
    visual_form: cluster   # from the vocabulary in visual-style.md
    continues_from: null   # or the id of the scene whose diagram continues
    visual: >
      What is on screen at the start, how it changes, what is highlighted.
      Concrete: node names, numbers, labels, positions (left/right/center).
    cues:
      - name: leader_crash
        change: "S1 gaśnie i dostaje ✕"
    paper_refs: ["p.6 §5.2"]
```

After writing, reply with one line: the number of chapters and scenes.
