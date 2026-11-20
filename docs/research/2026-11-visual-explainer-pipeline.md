# Research: diagram-first explainer pipeline (Claude script + ElevenLabs + code-rendered visuals)

Date: 2026-11-20. Goal: decouple the channel from NotebookLM. Claude Code writes the script and the visuals; ElevenLabs generates narration; visuals are diagrams/animations synced to words.

## Decisions (2026-11-20)

| Topic | Decision |
|---|---|
| POC paper | Raft — episode 73 (`whitepapers/distributed-computing/73-raft.pdf`) |
| Rendering | Remotion |
| Voice | ElevenLabs Voice Library voices: narrator Alex (`H5xTcsAIeS5RAykjz57a`), skeptic Asia (`Bz1e1clEKwgN71Vx7cxj`); `eleven_v4`. Library voices need a paid plan (Starter is enough for the POC) |
| Format | Narrator (prowadzący) + short skeptic voice (sceptyk) |
| Intro/outro | 5 s thumbnail intro over the greeting "Witamy ponownie w Głębokim Odczycie", closing invitation to next episode, 5 s silent outro. The outro is a new "Polub i subskrybuj" card in the episode style without the mascot (`Outro` composition), replacing `last-slide.png` for diagram-first episodes |
| Language | Everything in Polish: narration, on-screen labels, chart titles, metadata. Technical terms stay in English, as in the podcast prompt ("transformer", "leader election", "log replication"). Note: NotebookLM slides used to be English; this changes |
| Quality gate | Scenario review against the whitepaper before TTS (section 4a) |
| LLM steps | Headless Claude Code (`claude -p`), no direct Anthropic API calls (section 4b). ElevenLabs stays an HTTP API call: it is TTS, not LLM generation |
| Visual style | Ohara redesign palette (powder pink, bottle green, raspberry), dark theme; binding guide `docs/design/visual-style.md`, mockups `docs/design/mockups/raft-style.html` |

---

## 1. How to present paper ideas (evidence)

### Learning-science rules (Mayer multimedia principles; median effect sizes, approximate)

| Principle | d | Rule for this channel |
|---|---|---|
| Temporal contiguity | 1.22 | Each element appears/highlights when the narrator says it → drive reveals from TTS word timestamps |
| Spatial contiguity | 1.10 | Labels on/next to the thing they name; no legends |
| Coherence | 0.86 | No decoration, stock imagery, music under explanation, tangents |
| Redundancy | 0.86 | Never put narrated sentences on screen. ≤3-word labels OK (English terms as labels under Polish narration fit this) |
| Personalization | 0.79 | "my", "ty", conversational register |
| Segmenting | 0.77 | One idea per scene; 2–4 min chapters with mini-hook + recap; YouTube chapters |
| Modality | 0.76 | Explain diagrams by voice. Exception: long equations/definitions stay on screen (transient-information effect) |
| Pre-training | 0.75 | Introduce 3–5 key terms (name + role + color) before the mechanism |
| Voice | 0.74 | Human-like voice; native-speaker prosody check |
| Signaling | 0.41 | Highlight, dim, arrows, color to show what matters *now* |

- Animation vs static: modest gain (d≈0.2–0.4). Animate only what changes over time (congruence); long unbroken animations lose the gain — insert holds.
- Worked examples beat abstract statements for high element-interactivity ideas (attention, consensus).
- Visual clutter (esp. on-screen text) correlates with pauses/rewinds/dropouts (arXiv 2505.01753).

Sources: Mayer summary (my.chartered.college/?p=6958), Schneider et al. 2018 signaling meta-analysis, Höffler & Leutner 2007, Tversky et al. 2002, Rey et al. 2019, Leahy & Sweller.

### What strong explainer creators converge on

- **Concrete before abstract** (3Blue1Brown, stated). Puzzle/failure first, general form later.
- **Black box → open layer by layer** (Jay Alammar, Illustrated Transformer). One running example throughout; 512-dim vectors drawn as 4 colored boxes.
- **One persistent diagram that grows**, instead of a new slide per point.
- **Fixed color per concept** for the whole video; same color in equations and diagrams.
- **Toy-sized numbers** (StatQuest: 3–5 data points; Karpathy: smallest working version first).
- **Show state after every step** (Bret Victor, Learnable Programming).
- **Redraw, don't paste** the paper's figures (distill.pub "Research Debt": notation is the UI of research). Show the original figure briefly for authenticity.
- **Protocol animation references**: RaftScope (raft.github.io), The Secret Lives of Data.
- **Animated flow on architecture diagrams** (ByteByteGo style).

### Idea type → visual form

| Idea type | Visual | Motion |
|---|---|---|
| Architecture (Transformer, AFS) | Block diagram built progressively; active path highlighted, rest dimmed | Animate build-up, hold while narrating |
| Algorithm (attention, PageRank) | Step-through on 3–4 element toy input with real numbers + step counter | Animate state changes, pause per step |
| Distributed protocol (Raft, Paxos, 2PC, Coda) | Swimlanes per node, messages as moving dots, term/clock on screen, failure injection as climax | Animate (timing *is* the content) |
| Data structure (LSM, B-tree, CRDT) | Concrete instance; before → after per operation | Animate ops |
| Math | Term-by-term reveal, variables color-matched to diagram | Equation static, highlights animated |
| Results/benchmarks | Redrawn chart, one takeaway, title = takeaway, key series colored, rest gray | Static (animate arrival of key bar at most) |
| Trade-offs (CAP etc.) | 2×2 or comparison table, paper vs predecessors | Static, built cell by cell |
| History/lineage | Timeline with paper as pivot + descendants | Static, pan/zoom |
| Limitations | Same diagram re-run with failure in red | Animate |

### Script arc (15–20 min, chaptered)

1. Hook (≤45 s): concrete puzzle/failure ("Dwa serwery myślą, że są liderem…"). Never open with title/authors.
2. Problem & stakes in that year.
3. Prior approaches and why they fail — on the same diagram that will hold the solution.
4. Pre-training: 3–5 terms, fixed colors/icons.
5. Key insight: one sentence + one visual.
6. Mechanism: progressive build, one segment per subcomponent.
7. Worked example: full run with toy numbers / failure scenario.
8. Results: 1–3 redrawn charts.
9. Limitations: counterexample on the same diagram.
10. Legacy: timeline of descendants.
11. Recap: final full diagram, one line per part.

### One narrator vs two hosts

- Vicarious-learning gains come from **deep "why / what if" questions**, which work equally inside a monologue (Craig et al. 2006). The second voice is not the active ingredient.
- Chi's dialogue-video advantage appeared mainly with paired viewers; YouTube viewers watch solo.
- AI two-host podcasts (PAIGE, arXiv 2409.04645): rated attractive, but generic ones never beat a textbook on learning; >50% of feedback asked for visuals.
- No evidence found on YouTube retention for 1 vs 2 hosts.
- **Recommendation:** single conversational narrator with scripted deep questions. Optional: a short second "skeptic" voice for 1–2 sentence questions.
- **Chosen:** narrator + skeptic. Skeptic rules:
  - 1–2 sentences per line, ~6–10 lines per episode, at chapter boundaries and before key insights.
  - Only "why / what if / why not simply…" questions and objections that set up the next idea; no banter, no agreement filler ("Wow", "Dokładnie").
  - Every skeptic question gets an explicit answer from the narrator in the next segment.
  - Its own visual cue (e.g. a question badge in the corner), so viewers see who speaks.

### Automated paper→video research (2025–26)

- **Code2Video** (arXiv 2510.01174): Planner → Manim coder → VLM critic on rendered frames. Ablation drops in TeachQuiz: no storyboard −41.5, no asset DB −30.0, no layout anchors (6×6 grid) −26.8, no critic −21.3. Pixel video models (Veo3, Wan) ≈ 0. Aesthetics vs learning r=0.97.
- **Paper2Video** (arXiv 2510.05096): cursor highlight raised localization 0.084 → 0.633 (signaling). Talking head helps author recall, not comprehension.
- **TheoremExplainAgent** (arXiv 2502.19400): agentic planning essential for long videos; most failures are layout (overlap, misalignment).
- **AutoPresent** (arXiv 2501.00912): slides-as-code beat image generation. **Paper2Poster**: text density hurts quiz scores.
- Takeaways: storyboard first → render via code → fixed layout grid → vision critique of rendered frames → quiz-based QA metric.

---

## 2. Rendering stack

| Engine | Status (2026-11) | Fit |
|---|---|---|
| **Remotion** (React/TS, headless Chrome) | v4.0.545, daily commits. Free for individuals / companies ≤3 people, incl. commercial | **Primary.** `calculateMetadata()` sets duration from audio; `<Sequence>` per segment; cues → frames; official Claude Code skills/plugin; `remotion still --frame=N` for self-check; DOM bbox lint for overlaps |
| HyperFrames (HeyGen, HTML+GSAP) | v0.9.72, Apache-2.0, pre-1.0, fast churn | Fallback if Remotion license/React becomes a problem |
| Manim CE | v0.22.1, active, API churn each minor | Specialist: equation morphs, geometric proofs. Pin version. Embed as clip |
| manim-voiceover | ElevenLabs service stale (2023 SDK, Whisper-based bookmarks) | Don't use |
| Motion Canvas | Last code commit 2025-02 | Avoid |
| Typst + touying | typst 0.15.1, touying 0.8.0 | Cheapest step: `#pause` step slides → PNG per step → existing concat flow, timed from cues. No real motion |
| Slidev / reveal.js+decktape | Active | Per-click PNG export; alternative to Typst |

Diagrams and data:

- **D2** (themes, sketch mode, ELK layout) for static architecture/flow → SVG; reveal/highlight by SVG element id inside Remotion so positions stay stable across steps.
- **elkjs** inside Remotion components for diagrams that move (Raft messages, attention flow).
- **Mermaid** for quick sequence diagrams (layout reshuffles on edits; no native steps).
- **d3-scale / d3-shape** inside Remotion for animated result charts; Vega-Lite (vl-convert) for static charts.
- Polish diacritics: Google Fonts `latin-ext` subset (Inter, IBM Plex Sans, Noto Sans).

### 2a. Visual style (from ohara redesign)

Source: `Automaat/ohara` `docs/design/redesign/README.md` (origin/main). Mockups: `docs/design/mockups/raft-style.html` (12 frames at 1920×1080, dark/light toggle).

| Token | Dark (proposed) | Light | Use in video |
|---|---|---|---|
| canvas | `#0E1B17` | `#F8E9E6` | Frame background |
| surface | `#16261F` | `#FFF7F5` | Cards |
| inset / line | `#1E3029` / `#2B4038` | `#F1DAD6` / `#E6CBC6` | Chips, lanes, grid |
| ink / muted | `#F7E6E3` / `#A9B3AE` | `#1F3B33` / `#59635E` | Text; Follower (neutral) |
| heading | `#F4C6CC` | `#1F3B33` | Titles, active-element glow |
| success | `#6FBF97` | `#276B4E` | Committed, vote ✓ |
| danger | `#F08A7E` | `#A3322A` | Failure, always with ✕ icon |
| leader (raspberry) | `#DC5C8A` | `#B4245D` | Leader; key chart series |
| candidate (ochre) | `#BF8530` | `#A3620C` | Candidate |
| c3 (blue) | `#4F97CF` | `#1F6FAE` | Reserved 3rd category |

- Role colors are new (ohara has a single accent). Leader/candidate/c3 pass the dataviz validator (lightness band, chroma, CVD ΔE ≥ 8, normal-vision ΔE ≥ 15) in both themes. Ohara's own `#F2779F` accent failed against danger (ΔE 7.3) and green (deutan ΔE 1.5), so it is not used as a role color.
- Type: Fraunces 600 (titles, chapter cards, big numbers), Plus Jakarta Sans (labels), JetBrains Mono (technical terms, values, term/index).
- Frame rules: 96 px margins; text ≥22 px at 1080p; brand top-left, chapter progress top-right, speaker chip bottom-left (narrator neutral, skeptic pink); no burned-in narration (captions as CC from SRT); active element = full opacity + pink glow, rest at 30%.

---

## 3. Audio: ElevenLabs

- **Model:** `eleven_v4` (2026-09-28): Polish, 10k chars/request, audio tags, request stitching, inline IPA, phoneme dictionary rules. v3 is "previous generation" (5k, no stitching). `eleven_multilingual_v2` = fallback.
- **Timestamps:** `POST /v1/text-to-speech/{voice_id}/with-timestamps` → `alignment.characters` + start/end seconds per char. Group on whitespace for words. Use `alignment` (maps to original text), not `normalized_alignment`.
  - To verify: timestamps on v4, and stitching combined with with-timestamps.
- **Backup timing:** Forced Alignment API (`POST /v1/forced-alignment`, audio + plain text → words with `loss`), Polish supported, ≈$0.07/episode. `loss` flags mispronounced words.
- **Dialogue:** `POST /v1/text-to-dialogue/with-timestamps` exists (per-char alignment + `voice_segments`), but ≤2,000 chars/request (~10 requests/episode) and "under active development"; possible "Beta Service" exclusion from commercial license — unverified.
- **GenFM:** rewrites your script → unusable for a Claude-authored script.
- **No SSML on v4.** Pauses via punctuation/ellipses/tags.
- **English terms in Polish:** test `language_code="pl"` vs unset; project pronunciation dictionary (alias rules, one entry per inflected form: transformera, transformerem; both capitalizations); Claude writes TTS-ready text (numbers/acronyms spelled out). Build a 30-term listening test before the first episode.
- **Voices:** ElevenLabs default voices expire 2026-12-31 — don't build on them. Best long-term: Professional Voice Clone of the owner (Creator+, 1–3 h clean Polish audio, fine-tuned for v4). Interim: a Polish Voice Library voice.
- **Cost:** ~13 episodes/month × 18k chars ≈ 234k (≈300k with retakes). API Creator $22/month includes 275k v4 chars; overage $0.08/1k chars. Pro ($99) only for WAV output or >15 episodes/month. Paid plans include commercial license.
- **SDK:** `elevenlabs` 2.79.0 (`text_to_speech.convert_with_timestamps`, `pronunciation_dictionaries.create_from_file`).
- Alternatives checked: OpenAI TTS shutting down 2027-01-06; Gemini TTS (Polish GA, no word timestamps found) is the only credible cheaper fallback; Azure most controllable but flatter; open-source weights non-commercial or English-only.

---

## 4. Proposed pipeline

Implemented as the `odczyt` package (`src/odczyt/`); the stage list and commands
are in `docs/pipeline.md`. The sketch below is the original proposal.

```text
paper PDF
  → paper.txt              (pdftotext with page markers; source of truth for review)
  → storyboard.yaml        (Claude: chapters, scenes, one idea + visual form per scene, color/term glossary)
  → script.yaml            (Claude: Polish narration per segment, speaker narrator|skeptic, [[cue:x]] markers, TTS-ready)
  → SCENARIO REVIEW        (clean-context reviewer vs paper.txt → review.md; gate + owner sign-off; see 4a)
  → tts_segments.py        (ElevenLabs v4 with-timestamps per segment, voice per speaker, stitching, dictionary, cache by hash)
  → build_timeline.py      (segment offsets, cue times, narration.wav loudnorm −14 LUFS, SRT captions)
  → Remotion scenes        (Claude: one component per scene, shared design system + 6×6 layout grid)
  → verify stills          (render frame at each cue+0.5s; Claude reviews layout + that numbers/labels match script; DOM overlap lint)
  → render segments        (parallel MP4s; only changed segments re-render) → ffmpeg concat + mux
  → verify_video.py        (existing: duration, black frames)
  → metadata/upload        (existing scripts)
```

Example segments:

```yaml
- id: s07
  speaker: skeptic
  scene: RaftElection
  text: "Ale skąd follower ma wiedzieć, że lider naprawdę padł, a nie tylko ma wolną sieć?"
  refs: []
- id: s08
  speaker: narrator
  scene: RaftElection
  text: "Nie wie tego na pewno. Gdy przez election timeout nie dostanie heartbeatu, [[cue:timeout]] zwiększa swój term [[cue:term]] i prosi pozostałe serwery o głosy."
  refs: ["p.6 §5.2: 'If a follower receives no communication over a period of time called the election timeout…'"]
```

Two voices without the Dialogue API: each segment is a normal single-voice `with-timestamps` call using the speaker's voice. Keeps the 10k-char limit, timestamps and commercial license; avoids the 2k-char beta Dialogue endpoint. To verify: whether `previous_request_ids` can chain across different voices or only within one voice.

### 4a. Scenario review (fidelity to the whitepaper)

Runs after `script.yaml`, before TTS — TTS costs money and every scene depends on the script. Lesson from TheoremExplainAgent: generated explanations hide reasoning errors that a careful pass exposes.

- **Reviewer:** a separate clean-context agent that did not write the script. Gets only `paper.txt`, `storyboard.yaml`, `script.yaml`. Instructed to assume errors exist.
- **Checks:**
  1. **Claims:** extract every factual claim (mechanism, ordering, guarantee, number, comparison, attribution). For each: paper location (page/section) + English quote + verdict `supported | simplified-ok | misleading | unsupported | wrong`.
  2. **Coverage:** list the paper's key contributions (abstract, contributions list, conclusion); each must appear in the script or be listed as a deliberate omission with a reason.
  3. **Skeptic loop:** every skeptic question is answered, and the answer is correct per the paper.
  4. **Simplifications:** toy examples (3–5 servers, terms, logs) must not contradict paper rules (e.g. Raft election restriction, commit rule for previous-term entries).
  5. **External claims:** anything not in the paper (history, adoption — etcd, Consul) marked `external` and needs a source URL, or is cut.
  6. **Numbers:** every figure and benchmark number matches the paper exactly (e.g. user-study results, timeout ranges).
  7. **Language:** Polish, technical terms in English, no English sentences, TTS-ready (numbers and acronyms spelled out).
- **Output:** `review.md` (summary table + findings) and `claims.json` (machine-readable, reused by the stills check).
- **Gate:** zero `wrong` / `unsupported`; every `misleading` fixed; coverage complete. Fix → re-review the changed segments + one full coverage pass. Then the owner reads `review.md` and approves before TTS.
- **Second, lighter check after rendering stills:** numbers, labels and diagram states shown on screen match `claims.json` (a correct script can still get a wrong visual).

### 4b. LLM steps run as headless Claude Code

Every LLM step is one `claude -p` run started by a mise task or a Python orchestrator (`subprocess`), using the CLI's existing login. No Anthropic SDK or API key in the repo.

| Step | Prompt file (planned) | Tools | Output |
|---|---|---|---|
| Storyboard | `youtube/prompts/pipeline/storyboard.md` | Read | `storyboard.yaml` |
| Script | `youtube/prompts/pipeline/script.md` | Read, Write | `script.yaml` |
| Scenario review | `youtube/prompts/pipeline/review.md` | Read only | `review.md`, `claims.json` (via `--json-schema`) |
| Scene code | `youtube/prompts/pipeline/scenes.md` | Read, Write, Edit, Bash (`npx remotion still`) | Remotion components |
| Stills review | `youtube/prompts/pipeline/stills-review.md` | Read (PNG frames) | findings JSON |

- Flags (checked with `claude --help`, 2026-11-20): `-p`, `--output-format json`, `--json-schema` (structured findings), `--allowedTools` (per-step allowlist), `--permission-mode`, `--append-system-prompt`, `--model`, `--max-budget-usd`, `--add-dir`, `--no-session-persistence`.
- Clean context for the reviewer comes free: a separate `claude -p` process that never saw the writer's session.
- Each step reads and writes files under `youtube/pl/episodes/{ep}/`, so steps can be re-run one at a time and diffed in git.
- Claude reviews rendered stills by reading the PNGs inside the session.

Repo impact:

- Keep: `verify_video.py`, encode/mux parts of `generate_video.py`, thumbnails, download, upload/status scripts.
- Keep only for Typst path: `generate_concat.py`, `verify_concat.py` (durations from cues, not by hand).
- Retire for new episodes: `prepare_slides.py`, `analyze_transcript.py`, Whisper timing (keep Whisper/forced alignment as pronunciation QA).
- Add: Node to `mise.toml`, tasks `storyboard`, `tts`, `timeline`, `stills`, `render`.

QA metric per episode: generate 5–10 quiz questions from the paper; a model answers from frames + narration only; track score.

---

## 5. Open questions

- Output name for the POC: replace the existing episode 73 video or publish as a new episode (e.g. `73-raft-v2`)?
- Voices: Alex (narrator) and Asia (skeptic) were picked for the POC without a listening test of English terms; confirm or swap.
- Owner sign-off on the scenario review: every episode, or only until the reviewer proves reliable?
- Tooling gaps on this Mac: poppler and ImageMagick (`magick`, used by `verify_video.py` for black-frame checks) are not on PATH; `mise.toml` is untrusted. `pypdf` replaces poppler for text; brightness was checked with ffmpeg by hand.
- Existing tests `test_archive_episode.py`, `test_generate_video.py` and `test_transcribe.py` rewrite the real `whitepapers/status.json` when run.

## 6. POC results: episode 73 (Raft), 2026-11-20

Output: `youtube/pl/episodes/73-raft/build/73-raft.mp4` (17:54, 1920×1080, 30 fps, h264 + AAC). Not committed; text artifacts (storyboard, script, review, claims, timeline) and scene code are.

| Step | Result | Cost (`claude -p` reported) |
|---|---|---|
| Storyboard | 5 chapters, 21 scenes, 2–6 cues each | $1.29 |
| Script | 52 segments (10 skeptic), 13.3k characters | $2.09 |
| Scenario review | 4 rounds: fail → fail → fail → pass | $4.39 + fixes $1.41 |
| TTS | 52 ElevenLabs `eleven_v4` requests, ≈6.7k credits, character alignment matched audio length in every segment | Starter plan |
| Scene code | 5 parallel `claude -p` runs, ~2.9k lines TSX, each checked its own stills | $12.00 |
| Stills review | 3 runs (one full, two scoped), 1 + 6 blockers, 43 minor findings | $12.44 |
| Scene fixes | 2 rounds | $6.97 |
| Render | 3 min 44 s for 17:54 of video (≈4.8× real time) on this Mac | – |

Total LLM cost ≈ $41 as reported by `claude -p` (API-equivalent; billed against the CLI login).

What the gates caught:

- Scenario review, round 1: a real protocol error. The log-repair example started the leader's `nextIndex` at 5, but per §5.3/Fig. 2 it is set when the leader comes to power (3 in that story), so the two rejections shown could not happen. Plus three storyboard visuals that misstated facts (overwrites on a server that never had the entry, wrong trial count).
- Round 2: joint consensus overstated (both majorities only once a server has `C_old,new`). Round 3: a missing abstract-level contribution (equivalent to multi-Paxos, as efficient). Round 1 had judged that same omission acceptable, so the reviewer is not deterministic; keep a final full pass.
- Stills review: a joint-consensus frame showing `C_new` committed on 2 of 5 servers; heartbeats and RequestVote drawn as a relay chain S1→S2→S3 instead of parallel RPCs; a vote hull implying votes that were refused; animation finishing after the narrator already described it.

Lessons:

- One stills reviewer for 132 frames ran out of context (lost the first 45 frames). Scope reviews to ≤ 70 frames (`--var scope=…`).
- Scene coders asked for extra cues twice and used fixed frame offsets instead; let the scene step propose new `[[cue:…]]` markers back to the script (re-TTS is cached per segment).
- The dark canvas measures ~0.11 mean brightness; `verify_video.py` flags < 0.05 as black, so the margin is small.

## 7. Unverified

- ElevenLabs v4 Polish quality and English-term handling (no independent benchmark) — listening test mandatory.
- v4 timestamps on with-timestamps; stitching + timestamps; Text to Dialogue beta/commercial status; v4 speed setting; non-English phoneme rules (docs conflict).
- Remotion render throughput on this Mac (estimate 0.5–2× real time at 1080p30) — run a 60 s pilot.
- No benchmark compares LLM success on Remotion vs Manim; ranking inferred.
- Most creator techniques are observations, not creator-documented (except Sanderson, Alammar, Karpathy, Distill, Victor).
