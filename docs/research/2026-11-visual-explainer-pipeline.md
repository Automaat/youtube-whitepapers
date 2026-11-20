# Research: diagram-first explainer pipeline (Claude script + ElevenLabs + code-rendered visuals)

Date: 2026-11-20. Goal: decouple the channel from NotebookLM. Claude Code writes the script and the visuals; ElevenLabs generates narration; visuals are diagrams/animations synced to words.

## Decisions (2026-11-20)

| Topic | Decision |
|---|---|
| POC paper | Raft — episode 73 (`whitepapers/distributed-computing/73-raft.pdf`) |
| Rendering | Remotion |
| Voice | ElevenLabs Voice Library voices (no own-voice clone for POC) |
| Format | Narrator (prowadzący) + short skeptic voice (sceptyk) |
| Intro/outro | Unchanged: 5 s thumbnail intro, opening phrase "Witamy ponownie w Głębokim Odczycie", closing invitation to next episode, 5 s silent outro with `last-slide.png` |
| Language | Everything in Polish: narration, on-screen labels, chart titles, metadata. Technical terms stay in English, as in the podcast prompt ("transformer", "leader election", "log replication"). Note: NotebookLM slides used to be English; this changes |
| Quality gate | Scenario review against the whitepaper before TTS (section 4a) |

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
  refs: ["§5.2: 'If a follower receives no communication over a period of time called the election timeout…'"]
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

Repo impact:

- Keep: `verify_video.py`, encode/mux parts of `generate_video.py`, thumbnails, download, upload/status scripts.
- Keep only for Typst path: `generate_concat.py`, `verify_concat.py` (durations from cues, not by hand).
- Retire for new episodes: `prepare_slides.py`, `analyze_transcript.py`, Whisper timing (keep Whisper/forced alignment as pronunciation QA).
- Add: Node to `mise.toml`, tasks `storyboard`, `tts`, `timeline`, `stills`, `render`.

QA metric per episode: generate 5–10 quiz questions from the paper; a model answers from frames + narration only; track score.

---

## 5. Open questions

- Output name for the POC: replace the existing episode 73 video or publish as a new episode (e.g. `73-raft-v2`)?
- Which two library voices (narrator, skeptic)? Pick after a short Polish listening test.
- Owner sign-off on the scenario review: every episode, or only until the reviewer proves reliable?

## 6. Unverified

- ElevenLabs v4 Polish quality and English-term handling (no independent benchmark) — listening test mandatory.
- v4 timestamps on with-timestamps; stitching + timestamps; Text to Dialogue beta/commercial status; v4 speed setting; non-English phoneme rules (docs conflict).
- Remotion render throughput on this Mac (estimate 0.5–2× real time at 1080p30) — run a 60 s pilot.
- No benchmark compares LLM success on Remotion vs Manim; ranking inferred.
- Most creator techniques are observations, not creator-documented (except Sanderson, Alammar, Karpathy, Distill, Victor).
