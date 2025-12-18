# YouTube Video Generation Pipeline

![cookie_superhero](cookie_superhero.png)

**Channel:** [Głęboki Odczyt](https://www.youtube.com/@GlebokiOdczyt) | **Request episode:** [Create issue](https://github.com/Automaat/youtube-whitepapers/issues/new) with whitepaper link

Generate YouTube videos from NotebookLM podcasts about AI/ML milestone papers.

## Directory Structure

```text
youtube-whitepapers/
├── scripts/                  # Python automation scripts
│   ├── compress_images.py    # Batch PNG compression (>threshold)
│   ├── generate_video.py     # Generate video from concat.txt + audio
│   ├── prepare_slides.py     # Extract/normalize slides from PDF
│   ├── rename_thumbnails.py  # Rename thumbnails to match whitepapers
│   ├── transcribe.py         # Batch transcription with Whisper
│   └── verify_video.py       # Verify video quality
├── tests/                    # Pytest test suite
├── mise.toml                 # Task runner configuration
└── youtube/
    ├── pl/                   # Polish language assets
    │   ├── audio/            # NotebookLM podcast audio (.m4a)
    │   ├── slides/           # Presentation PDFs + extracted PNGs
    │   └── transcripts/      # Whisper transcriptions (.json)
    ├── output/               # Final videos (.mp4) + metadata (.txt)
    └── thumbnails/           # Video thumbnails (.png)
```

## Full Workflow

### 1. Add Audio from NotebookLM

Export podcast from NotebookLM and save to `audio/`:

```text
audio/XX-paper-name.m4a
```

Naming convention: `{number}-{paper-name}.m4a` (e.g., `02-gpt.m4a`)

### 2. Transcribe Audio

Run batch transcription (uses Whisper, Polish language):

```bash
mise run transcribe
# Or with custom parallelization:
mise run transcribe -- 4
```

Output: `youtube/pl/transcripts/XX-paper-name.json`

### 3. Generate Slides (NotebookLM)

#### Option A: Use existing prompt template

```bash
# Read transcript and create slide prompt
cat prompts/generate-slides-command.md
```

#### Option B: Use Claude Code

Run in fresh Claude Code session:

```text
Read the transcript file at milestone-papers/youtube/transcripts/XX-paper-name.json
and create a detailed NotebookLM prompt for generating 10 presentation slides.
```

Then paste the generated prompt into NotebookLM to create slides PDF.

Save slides to: `slides/XX-paper-name.pdf`

### 4. Add Thumbnail

Generate thumbnail in NotebookLM or externally.
Save to: `youtube/thumbnails/XX-paper-name.png`

Rename numeric thumbnails to match whitepaper names and compress:

```bash
mise run rename-thumbnails            # Rename + compress to <1.9MB
mise run rename-thumbnails --dry-run  # Preview changes
```

### 5. Generate Video

#### Prepare slides

```bash
mise run prepare -- 28  # Extracts PDF, normalizes images
```

#### Generate video (after creating concat.txt)

```bash
mise run video -- 28
# Or skip verification:
mise run video -- 28 --skip-verify
```

#### Or use Claude Code slash command

```bash
/generate-video 28
```

This runs the full video generation workflow with proper timings.

### 6. Output

Final files in `output/`:

- `XX-paper-name.mp4` - Video file
- `XX-paper-name-metadata.txt` - Title, description, tags for YouTube

## File Naming Convention

All files must follow: `{XX}-{paper-name}` where:

- `XX` = 2-digit episode number (01, 02, ... 19)
- `paper-name` = lowercase, hyphenated paper identifier

Examples:

- `01-attention-is-all-you-need`
- `02-gpt`
- `03-bert`
- `19-chain-of-thought`

## Episode Status

| # | Paper | Audio | Slides | Transcript | Thumbnail |
|---|-------|-------|--------|------------|-----------|
| 01 | Attention Is All You Need | ✅ | ✅ | ✅ | ✅ |
| 02 | GPT | ✅ | ✅ | ✅ | ✅ |
| 03 | BERT | ✅ | ✅ | ✅ | ✅ |
| 04 | GPT-2 | ✅ | ✅ | ✅ | ✅ |
| 05 | Megatron-LM | ✅ | ✅ | ✅ | ✅ |
| 06 | T5 | ✅ | ✅ | ✅ | ✅ |
| 07 | ZeRO | ✅ | ✅ | ✅ | ✅ |
| 08 | Scaling Laws | ✅ | ✅ | ✅ | ✅ |
| 09 | GPT-3 | ✅ | ✅ | ✅ | ✅ |
| 10 | Switch Transformers | ✅ | ✅ | ✅ | ✅ |
| 11 | Codex | ✅ | ❌ | ✅ | ✅ |
| 12 | Foundation Models | ✅ | ❌ | ✅ | ✅ |
| 13 | FLAN | ✅ | ❌ | ✅ | ✅ |
| 14 | T0 | ✅ | ❌ | ✅ | ✅ |
| 15 | GLaM | ✅ | ❌ | ✅ | ✅ |
| 16 | WebGPT | ✅ | ❌ | ✅ | ✅ |
| 17 | RETRO | ✅ | ❌ | ✅ | ✅ |
| 18 | Gopher | ✅ | ❌ | ✅ | ✅ |
| 19 | Chain-of-Thought | ✅ | ❌ | ✅ | ✅ |

## Paper URLs Reference

| Episode | arXiv/Paper URL |
|---------|-----------------|
| 01-attention-is-all-you-need | <https://arxiv.org/abs/1706.03762> |
| 02-gpt | <https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf> |
| 03-bert | <https://arxiv.org/abs/1810.04805> |
| 04-gpt2 | <https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf> |
| 05-megatron-lm | <https://arxiv.org/abs/1909.08053> |
| 06-t5 | <https://arxiv.org/abs/1910.10683> |
| 07-zero | <https://arxiv.org/abs/1910.02054> |
| 08-scaling-laws | <https://arxiv.org/abs/2001.08361> |
| 09-gpt3 | <https://arxiv.org/abs/2005.14165> |
| 10-switch-transformers | <https://arxiv.org/abs/2101.03961> |
| 11-codex | <https://arxiv.org/abs/2107.03374> |
| 12-foundation-models | <https://arxiv.org/abs/2108.07258> |
| 13-flan | <https://arxiv.org/abs/2109.01652> |
| 14-t0 | <https://arxiv.org/abs/2110.08207> |
| 15-glam | <https://arxiv.org/abs/2112.06905> |
| 16-webgpt | <https://arxiv.org/abs/2112.09332> |
| 17-retro | <https://arxiv.org/abs/2112.04426> |
| 18-gopher | <https://arxiv.org/abs/2112.11446> |
| 19-chain-of-thought | <https://arxiv.org/abs/2201.11903> |

## Requirements

- **whisper** - Audio transcription (`pip install openai-whisper`)
- **ffmpeg** - Video generation (`brew install ffmpeg`)
- **poppler** - PDF to PNG (`brew install poppler`)
- **imagemagick** - Image processing (`brew install imagemagick`)
- **jq** - JSON processing (`brew install jq`)

Install Python dependencies:

```bash
mise run install
```

## YouTube Upload Setup

Automated upload requires Google Cloud OAuth credentials.

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable **YouTube Data API v3**:
   - APIs & Services → Library → search "YouTube Data API v3" → Enable

### 2. Create OAuth Credentials

1. APIs & Services → Credentials → Create Credentials → OAuth client ID
2. Application type: **Desktop app**
3. Download JSON → rename to `client_secret.json`
4. Move to `.youtube-credentials/client_secret.json`

### 3. Configure Playlists (optional)

Set playlist IDs via environment variables:

```bash
export YOUTUBE_PLAYLIST_LLM="PLxxxxxxxxxx"
export YOUTUBE_PLAYLIST_DISTRIBUTED_COMPUTING="PLyyyyyyyyyy"
export YOUTUBE_PLAYLIST_SECURITY="PLzzzzzzzzzz"
```

Or create `youtube/config.json`:

```json
{
  "playlists": {
    "llm": "PLxxxxxxxxxx",
    "distributed-computing": "PLyyyyyyyyyy",
    "security": "PLzzzzzzzzzz"
  }
}
```

### 4. Upload Video

```bash
mise run upload -- 28           # Upload episode 28 (private)
mise run upload -- 28 --dry-run # Validate without uploading
mise run upload -- 28 --privacy unlisted
```

First run opens browser for Google OAuth. Token saved to `.youtube-credentials/token.json`.

## Quick Start Example

```bash
# 1. Transcribe new audio
mise run transcribe

# 2. Prepare slides for episode
mise run prepare -- 28

# 3. Run Claude Code slash command (or generate video manually)
# /generate-video 28
mise run video -- 28

# 5. Upload to YouTube:
#    - Video: youtube/output/28-paper-name.mp4
#    - Metadata: youtube/output/28-paper-name-metadata.txt
#    - Thumbnail: youtube/thumbnails/28-paper-name.png
```
