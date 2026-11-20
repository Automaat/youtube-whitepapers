# Episode pipeline (`odczyt`)

One command takes a paper PDF to a verified video, thumbnail and YouTube metadata.
It stops only at owner gates and at checks it cannot fix itself.

- Code: `src/odczyt/` (Python package, CLI `odczyt`), Remotion in `youtube/remotion/`.
- Prompts: `youtube/prompts/pipeline/*.md`, one per LLM step.
- Defaults: `youtube/pipeline.yaml`; `episode.yaml` overrides any key.
- Design and rationale: `docs/research/2026-11-visual-explainer-pipeline.md`.
- Visual rules: `docs/design/visual-style.md`.

## Quick start

```bash
mise run install                     # uv sync + npm ci (once)
uv run odczyt new 74                 # youtube/pl/episodes/74-epaxos/episode.yaml
uv run odczyt run 74                 # runs until the script gate
#   read youtube/pl/episodes/74-epaxos/review.md and script.yaml
uv run odczyt approve 74 script
export BW_SESSION=$(bw unlock --raw) # ElevenLabs key from Bitwarden
uv run odczyt run 74                 # TTS → scenes → stills review → render
#   watch build/74-epaxos.mp4, check build/thumbnail.png and build/metadata.txt
uv run odczyt approve 74 video
uv run odczyt run 74                 # copies to youtube/output + youtube/thumbnails
mise run upload -- 74                # private upload (existing script)
```

`uv run odczyt status 74` shows what is fresh, `uv run odczyt list` shows every
episode's next stage, and `/generate-episode 74` drives the same steps from
Claude Code.

## Stages

| Stage | What | Kind |
|---|---|---|
| `paper` | `paper.txt` with `=== page N ===` markers | tracked |
| `meta` | title, subtitle, authors, paper URL into `episode.yaml` | create once |
| `storyboard` | chapters, scenes, cues, glossary, thumbnail pick | create once |
| `script` | narrator + skeptic segments with `[[cue:x]]` markers | create once |
| `review` | fact-check against the paper; `script-fix` and repeat until `pass` | tracked |
| `approve-script` | owner reads `review.md` | gate |
| `tts` | ElevenLabs per segment, cached by text hash | tracked |
| `timeline` | `narration.wav`, `timeline.json`, `captions.srt` | tracked |
| `layout` | shared diagram geometry `layout.ts` | create once |
| `scenes` | one `claude -p` agent per chapter, in parallel | create once |
| `stills-review` | frames after every cue, reviewed in parallel chunks; fix agents per part; repeat | tracked |
| `thumbnail` | 1280x720: big term + one frozen diagram frame | tracked |
| `metadata` | `TYTUŁ / OPIS / TAGI` with chapter timestamps | tracked |
| `render` | `build/{slug}.mp4`, duration and black-frame check | tracked |
| `approve-video` | owner watches the video | gate |
| `publish` | copy video, metadata, captions, thumbnail to `youtube/` | tracked |

- **Create once** stages run only while their output is missing, so hand edits are
  kept. Regenerate with `--force <stage>` or by deleting the file.
- **Tracked** stages rerun when the digest of their inputs changes. Editing
  `script.yaml` re-runs the review, invalidates the script approval, re-synthesizes
  only changed segments and re-renders.
- **Gates** are listed in `pipeline.gates`. An approval is tied to the exact content:
  a later change needs a new approval. Remove a gate from the list to run through it.
- State is in `build/state.json` (git-ignored). Outputs that exist without recorded
  state are adopted as fresh, unless an earlier stage ran in the same run.

## Costs

Every `claude -p` call appends to `build/costs.json`; `odczyt status` prints the sum
and the TTS characters still to synthesize (`eleven_v4`: about 0.5 credit per
character). The Raft pilot cost about $41 in LLM calls and 6.7k ElevenLabs credits.

## Thumbnails

The storyboard step picks `thumbnail: {term, tagline, scene, cue, crop}`. The
`Thumbnail` composition draws the term and the scene frozen 1.5 s after the cue,
cropped to `crop` (template A in `docs/research/2026-11-youtube-thumbnails.md`). The
video intro shows the same card for 5 s. To use a hand-made image instead, set
`thumbnail_image: path/to.png` in `episode.yaml`.

## Troubleshooting

- `⏸️ Gate`: do what it says, then `odczyt approve`.
- `No ElevenLabs key`: `export BW_SESSION=$(bw unlock --raw)`, set
  `ELEVENLABS_API_KEY`, or pass `--api-key-file`.
- Review or stills still failing after the configured rounds: read `review.md` or
  `build/stills-review.json`, fix by hand or rerun with `--force review` /
  `--force stills-review`.
- One LLM step by hand: `uv run odczyt step 74 metadata` (logs in
  `build/<label>.log.json`).

## Retiring the NotebookLM workflow

The NotebookLM scripts stay until the first episodes ship from this pipeline, then
get removed.

| Script | Plan |
|---|---|
| `transcribe.py`, `analyze_transcript.py`, `prepare_slides.py`, `generate_concat.py`, `verify_concat.py`, `generate_video.py`, `verify_video.py`, `rename_audio.py`, `rename_slides.py`, `archive_episode.py` | delete with `youtube/pl/{audio,slides,transcripts}` workflows and `/generate-video`, `/generate-slides`, `/generate-thumbnails` |
| `upload_youtube.py`, `publish_youtube.py`, `fetch_youtube_urls.py`, `youtube_config.py` | move into `odczyt` as `upload`, `publish` stages |
| `download_papers.py`, `status_utils.py`, `generate_status.py` | move into `odczyt`; drop `notebook_*`, `audio`, `slides` fields |
| `compress_images.py`, `rename_thumbnails.py` | drop; the pipeline renders thumbnails at the right size |
