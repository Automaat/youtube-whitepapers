# YouTube Whitepapers

Generate YouTube videos from NotebookLM podcasts about AI/ML milestone papers.

**Tech Stack:** Python 3, Bash, ffmpeg, whisper, pdftoppm, imagemagick

**Primary Tasks:** Video generation sessions, Python automation scripts

---

## Project Structure

```text
youtube-whitepapers/
├── scripts/                    # Python automation scripts
│   ├── compress_images.py      # Batch PNG compression (>threshold)
│   ├── generate_video.py       # Generate video from concat.txt + audio
│   ├── prepare_slides.py       # Prepare slides (extract, scale, normalize)
│   ├── rename_thumbnails.py    # Rename thumbnails to match whitepapers + compress
│   ├── transcribe.py           # Batch transcription with Whisper
│   ├── verify_concat.py        # Verify concat.txt (files, duration, structure)
│   └── verify_video.py         # Verify video (no black frames, correct duration)
├── tests/                      # Pytest test suite
├── pyproject.toml              # Project config (ruff, pytest)
├── mise.toml                   # Task runner configuration
├── whitepapers/
│   ├── llm/                    # LLM research papers
│   └── distributed-computing/  # Distributed systems papers
└── youtube/
    ├── pl/                     # Polish language assets
    │   ├── audio/              # NotebookLM podcast audio (.m4a)
    │   ├── slides/             # Presentation PDFs + extracted PNGs
    │   └── transcripts/        # Whisper transcriptions (.json)
    ├── output/                 # Final videos (.mp4) + metadata (.txt)
    ├── thumbnails/             # Episode thumbnails (.png)
    └── prompts/                # Claude Code prompt templates
```

---

## Naming Convention

**ALWAYS use:** `{XX}-{paper-name}`

- `XX` = 2-digit episode number (01, 02, ... 99)
- `paper-name` = lowercase, hyphenated identifier

**Examples:**

```text
01-llm-attention-is-all-you-need
15-llm-glam
42-distributed-computing-raft
```

**Apply to ALL files:** audio, slides, transcripts, thumbnails, output videos, metadata

---

## Video Generation Workflow

### Critical: Image Format Consistency

**All images in concat MUST have identical dimensions and format.** ffmpeg concat demuxer drops frames when image parameters change.

**Common failure modes:**

- ❌ Thumbnail at 1920x1080, slides at 2867x1600 → black/missing frames at start
- ❌ Mixing RGB and grayscale images → filter graph reconfiguration
- ❌ Different colorspaces between images → ffmpeg filter errors

**Solution:** Use `scripts/prepare_slides.py` to ensure consistency:

```bash
mise run prepare -- 26  # Prepares episode 26
```

This script:

1. Extracts slides from PDF using pdftoppm
2. Normalizes all slides to sRGB colorspace (prevents ffmpeg errors)
3. Scales thumbnail to match slide dimensions
4. Scales last-slide.png to match slide dimensions
5. Copies all files to `youtube/pl/slides/{ep}/` folder

### Critical: Timing Alignment

**Main pain point is timing misalignment.** Follow this process exactly:

1. **Prepare slides** (handles image consistency automatically)

   ```bash
   mise run prepare -- {ep_number}
   ```

2. **Read each slide image** - understand content/topic of every slide

3. **Analyze transcript timestamps**
   - Read `transcripts/{ep}.json` carefully
   - Note exact timestamps where topics change
   - Map each topic to corresponding slide

4. **Create timing table BEFORE generating concat.txt**

   ```text
   | Slide | Start    | End      | Topic                    |
   |-------|----------|----------|--------------------------|
   | 1     | 0:00     | 1:23     | Introduction             |
   | 2     | 1:23     | 3:45     | Architecture overview    |
   ```

5. **Verify timing logic**
   - Slides should transition when speaker changes topic
   - No slide should be shown for less than 5 seconds
   - No slide should exceed 3 minutes unless justified

6. **Generate concat.txt using template script**

   ```bash
   # Automatically adds 5s thumbnail intro + 5s silent outro
   mise run generate-concat -- 55 --durations slide-01:180,slide-02:150,slide-03:120

   # Or from JSON file
   mise run generate-concat -- 55 --json timings.json

   # Preview without writing
   mise run generate-concat -- 55 --durations ... --dry-run
   ```

   The script handles:
   - 5s thumbnail intro (duplicated to avoid ffmpeg drop bug)
   - Content slides with your specified durations
   - 5s silent outro with last-slide.png

7. **Verify concat.txt**

   ```bash
   mise run verify-concat -- 55 --check-dims
   ```

8. **Generate video**

   ```bash
   # Recommended: use generate_video.py (auto-verifies)
   mise run video -- 28

   # Or manual ffmpeg:
   ffmpeg -y -f concat -safe 0 -i concat.txt -i audio.m4a \
     -c:v libx264 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
     -pix_fmt yuv420p -c:a aac -b:a 192k output.mp4
   ```

9. **Verify duration** (automatic with generate_video.py)

   ```bash
   # Manual verification:
   ffprobe -v error -show_entries format=duration -of csv=p=0 audio.m4a
   ffprobe -v error -show_entries format=duration -of csv=p=0 output.mp4
   ```

### Output Requirements

- **5-second silent outro** using `slides/last-slide.png`
- **Video duration** = audio duration + 5 seconds (±0.5s tolerance)
- **Polish metadata** in `output/{ep}-metadata.txt`:

  ```text
  TYTUŁ:
  [Polish title] | Deep Dive

  OPIS:
  [Polish description]

  W tym odcinku omawiamy:
  • [Topic 1]
  • [Topic 2]

  📄 Oryginalny artykuł: [arxiv URL]

  TAGI:
  #AI #MachineLearning #DeepLearning
  ```

---

## Diagram-First Workflow (ElevenLabs + Remotion, pilot: 73-raft)

Replaces NotebookLM audio and slides for new episodes. Design:
`docs/research/2026-11-visual-explainer-pipeline.md`. Visual style (binding):
`docs/design/visual-style.md`. Episode files: `youtube/pl/episodes/{ep}/`
(`build/` is git-ignored).

```bash
mise run paper-text -- 73                       # paper.txt with page markers
mise run llm-step -- 73 storyboard              # storyboard.yaml (claude -p)
mise run llm-step -- 73 script                  # script.yaml
mise run llm-step -- 73 review                  # review.md, review.json, claims.json
mise run llm-step -- 73 script-fix              # repeat fix + review until verdict pass
mise run tts -- 73 --api-key-file PATH          # ElevenLabs per segment, cached by hash
mise run timeline -- 73                         # narration.wav, timeline.json, captions.srt
mise run llm-step -- 73 scenes --var part=part1 --var scene_ids=intro,hook
mise run stills -- 73                           # review frames after every cue
mise run llm-step -- 73 stills-review           # then scenes-fix if blockers
mise run render -- 73                           # build/{slug}.mp4 + verify_video
```

Rules:

- Every LLM step is a separate `claude -p` process (`scripts/run_llm_step.py`):
  restricted tools, no MCP, budget cap. The reviewer never sees the writer's session.
- No TTS before the scenario review says `pass` and the owner has read `review.md`.
- Timing comes from ElevenLabs character timestamps (`[[cue:name]]` markers in
  `script.yaml`), never from guessed durations.
- Intro: thumbnail (or the `Thumbnail` title card) over the first 5 s of narration.
  Outro: 5 s silent `Outro` card in the episode style (replaces `last-slide.png`).
- ElevenLabs key: Bitwarden item "ElevenLabs API key (Głęboki Odczyt)". `eleven_v4`
  costs about 0.5 credit per character; library voices need a paid plan.

---

## Timing Alignment Rules

**NEVER:**

- Guess slide timings without reading transcript
- Use uniform durations for all slides
- Skip the timing verification step
- Generate video without creating timing table first

**ALWAYS:**

- Read transcript JSON for exact timestamps
- Match slide content to what speaker discusses
- Show timing table before proceeding
- Verify final video duration matches expected

**If timing seems off:**

1. Re-read relevant transcript section
2. Identify topic boundaries
3. Adjust timing table
4. Regenerate concat.txt
5. Regenerate video

---

## Python Conventions

### Style

- **Use:** pathlib for all file operations
- **Use:** type hints for function signatures
- **Use:** early returns for error handling

### Example Pattern

```python
from pathlib import Path

def find_episode(ep_num: str) -> Path | None:
    """Find audio file matching episode number."""
    audio_dir = SCRIPT_DIR / "audio"
    matches = list(audio_dir.glob(f"{ep_num}-*.m4a"))
    return matches[0] if matches else None

def check_file(path: Path, label: str) -> None:
    """Print file status."""
    status = "✅" if path.exists() else "❌"
    print(f"{status} {label}: {path}")
```

### New Scripts

- Place in `scripts/` directory
- Use snake_case naming (e.g., `my_script.py`)
- Use `#!/usr/bin/env python3`
- Include docstring describing purpose
- Use emoji for status output (✅ ❌ 🔄 📋)
- Add corresponding tests in `tests/`

---

## Bash Conventions

### Style

- **Always:** `set -e` at start
- **Use:** `SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"`
- **Use:** emoji for output feedback
- **Use:** xargs for parallel operations

### Example Pattern

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARALLEL_JOBS="${1:-3}"

echo "🎙️ Starting transcription..."

find "$AUDIO_DIR" -name "*.m4a" | sort | \
    xargs -P "$PARALLEL_JOBS" -I {} bash -c 'transcribe_file "$1"' _ {}

echo "🎉 Complete!"
```

---

## External Tools

### Commands Reference

```bash
# Transcription (Polish)
whisper audio.m4a --model small --language pl --output_format json

# PDF to PNG extraction
pdftoppm -png -r 150 input.pdf output_prefix

# ImageMagick - get dimensions
identify -format "%wx%h" image.png

# ImageMagick - scale with padding
convert input.png -colorspace sRGB -resize WxH -background black -gravity center -extent WxH output.png

# ImageMagick - normalize colorspace (in-place)
mogrify -colorspace sRGB image.png

# ImageMagick - compress PNG
convert input.png -quality 80 -colors 256 output.png

# ImageMagick - check brightness (for black frame detection)
magick image.png -colorspace Gray -format "%[fx:mean]" info:

# Video generation
ffmpeg -y -f concat -safe 0 -i concat.txt -i audio.m4a \
  -c:v libx264 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -pix_fmt yuv420p -c:a aac -b:a 192k output.mp4

# Duration check
ffprobe -v error -show_entries format=duration -of csv=p=0 file.mp4
```

### Improvements Welcome

Suggest optimizations to ffmpeg/tool commands when you identify:

- Performance improvements
- Quality enhancements
- File size reductions

---

## Common Commands

```bash
# Download papers from file with auto-indexing
mise run download -- future/my-papers.md
mise run download -- future/my-papers.md --dry-run

# Transcribe all new audio files
mise run transcribe

# Transcribe with more parallelization
mise run transcribe -- 4

# Analyze transcript for slide generation
mise run analyze-transcript -- 73

# Prepare slides for an episode
mise run prepare -- 26

# Generate video from concat.txt
mise run video -- 28
mise run video -- 28 --skip-verify

# Compress large PNG files
mise run compress -- youtube/thumbnails/
mise run compress -- youtube/thumbnails/ --threshold 1MB --dry-run

# Rename thumbnails to match whitepaper names + compress
mise run rename-thumbnails            # Rename + compress to <1.9MB
mise run rename-thumbnails --dry-run  # Preview changes

# Verify concat.txt before generating video
mise run verify-concat -- 28                 # Basic checks
mise run verify-concat -- 28 --check-dims    # Also check image dimensions

# Verify a generated video
mise run verify -- youtube/output/26-opt.mp4 youtube/pl/audio/26-opt.m4a

# Run linter
mise run lint

# Format code
mise run format

# Run tests
mise run test

# Check video duration
ffprobe -v error -show_entries format=duration -of csv=p=0 youtube/output/*.mp4
```

---

## Anti-Patterns

❌ **NEVER:**

- Generate video without reading slides first
- Use placeholder timings
- Skip duration verification
- Hardcode paths (use pathlib/variables)
- Create metadata without reading transcript
- Assume slide order matches topic order in podcast

✅ **ALWAYS:**

- Read all inputs before generating outputs
- Create timing table before video generation
- Verify durations match expectations
- Use consistent naming convention
- Show progress with emoji status output

---

## Project-Specific Context

### Categories

Current paper categories:

- `llm` - Language models (GPT, BERT, LLaMA, etc.)
- `distributed-computing` - Distributed systems papers
- `security` - Security research (planned)

### Language Support

- **Current:** Polish (`youtube/pl/`)
- **Planned:** English version (future)

### Growth

Project is actively growing:

- Episode numbers will exceed 63
- New categories will be added
- Multi-language support planned

---

## Requirements

Install these tools:

```bash
pip install openai-whisper
brew install ffmpeg poppler jq imagemagick

# Development dependencies
pip install ruff pytest pytest-mock
```
