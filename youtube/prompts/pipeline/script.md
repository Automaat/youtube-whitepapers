# Script step

You write the narration for one episode of "Głęboki Odczyt", a Polish YouTube
channel that explains research papers with animated diagrams. Two voices:

- `narrator`: explains. Calm, concrete, conversational Polish. Talks to one viewer.
- `skeptic`: asks short deep questions ("dlaczego…?", "a co jeśli…?", "czemu nie po
  prostu…?") or raises an objection that sets up the next idea.

## Inputs (read all of them before writing)

- `{episode_dir}/episode.yaml`
- `{episode_dir}/paper.txt`: source of truth, with `=== page N ===` markers.
- `{episode_dir}/storyboard.yaml`: chapters, scenes, cues. Follow it.
- `docs/research/2026-11-visual-explainer-pipeline.md`, section 1 (narrator and
  skeptic rules).

## Task

Write `{episode_dir}/script.yaml`: the full narration, split into segments.

Content rules:

- Every claim must be true according to `paper.txt`. Do not add history, adoption or
  benchmarks that the paper does not state. If you simplify, the simplification must
  not contradict the paper's rules.
- Concrete before abstract: describe what happens on screen ("S3 pierwszy kończy
  odliczanie…") rather than defining things in the abstract.
- The narration must match the picture. Mention each element when it appears.
- Total length: about {target_chars} characters of narration (≈{target_minutes} min).

Format rules:

- Segment 1: `speaker: narrator`, `scene: intro`, text starts exactly with
  "Witamy ponownie w Głębokim Odczycie." followed by one sentence naming the paper.
- Last segment: `speaker: narrator`, `scene: outro_invite`, ends with an invitation to
  the next episode of "Głęboki Odczyt".
- Skeptic: 6–10 segments, each 1–2 sentences, placed at chapter boundaries and before
  key insights. No banter, no agreement filler ("Wow", "Dokładnie", "Świetne pytanie").
  The narrator's very next segment answers the question explicitly.
- Narrator segments: 1–5 sentences, ≤ 600 characters. One scene per segment;
  segments of the same scene are consecutive and in storyboard order.
- Cues: put every cue of the scene, exactly once, as `[[cue:name]]` directly before
  the word that the picture change belongs to. Names must match `storyboard.yaml`.
- Language: Polish only. Technical terms stay in English (leader, follower, candidate,
  term, log, commit, heartbeat, RequestVote, AppendEntries, split vote…). Never a full
  English sentence.
- TTS-ready text (it goes straight to a speech synthesizer):
  - write numbers as Polish words with correct inflection ("sto pięćdziesiąt do
    trzystu milisekund", "dwadzieścia pięć i siedem dziesiątych punktu");
  - no symbols, abbreviations, brackets, bullet lists or markdown;
  - spell out what a listener should hear ("RPC" stays RPC; "§5.2" → "w sekcji pięć
    dwa"; "S1" → "S jeden").
- `refs`: for every segment that states a fact from the paper, list
  `"p.N §X: '<short exact English quote from paper.txt>'"`. Quotes must be copied
  verbatim (hyphenation at line ends may be joined). Skeptic segments use `refs: []`.

## Output format

Write the file with the Write tool. YAML, UTF-8, exactly this shape:

```yaml
episode: "{slug}"
segments:
  - id: s001
    speaker: narrator      # narrator | skeptic
    scene: intro           # scene id from storyboard.yaml
    text: "Witamy ponownie w Głębokim Odczycie. …"
    refs: []
```

Use ids s001, s002, … in order. After writing, reply with one line: number of
segments, skeptic segments and total characters.
