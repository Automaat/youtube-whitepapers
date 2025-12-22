# YouTube Video Generation Pipeline

![cookie_superhero](cookie_superhero.png)

**Channel:** [Głęboki Odczyt](https://www.youtube.com/@GlebokiOdczyt) | **Request episode:** [Create issue](https://github.com/Automaat/youtube-whitepapers/issues/new) with whitepaper link

Generate YouTube videos from NotebookLM podcasts about computer science milestone papers - covering LLMs, distributed systems, networking, operating systems, and security.

## Directory Structure

```text
youtube-whitepapers/
├── scripts/                    # Python automation scripts
│   ├── compress_images.py      # Batch PNG compression (>threshold)
│   ├── generate_status.py      # Generate status report for tracking
│   ├── generate_video.py       # Generate video from concat.txt + audio
│   ├── prepare_slides.py       # Extract/normalize slides from PDF
│   ├── rename_thumbnails.py    # Rename thumbnails to match whitepapers
│   ├── transcribe.py           # Batch transcription with Whisper
│   └── verify_video.py         # Verify video quality
├── tests/                      # Pytest test suite
├── mise.toml                   # Task runner configuration
├── whitepapers/
│   ├── distributed-computing/  # Distributed systems papers
│   ├── llm/                    # LLM research papers
│   ├── networking/             # Networking protocols & systems
│   ├── operating-systems/      # OS research papers
│   └── security/               # Security research papers
└── youtube/
    ├── pl/                     # Polish language assets
    │   ├── audio/              # NotebookLM podcast audio (.m4a)
    │   ├── slides/             # Presentation PDFs + extracted PNGs
    │   └── transcripts/        # Whisper transcriptions (.json)
    ├── output/                 # Final videos (.mp4) + metadata (.txt)
    ├── thumbnails/             # Video thumbnails (.png)
    └── prompts/                # Claude Code prompt templates
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
Read the transcript file at youtube/pl/transcripts/XX-paper-name.json
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

#### Create concat.txt from slide timings

Use the template script which automatically handles intro/outro:

```bash
# Provide content slide durations (thumbnail/outro added automatically)
mise run generate-concat -- 28 --durations slide-01:180,slide-02:150,slide-03:120

# Preview without writing:
mise run generate-concat -- 28 --durations ... --dry-run

# From JSON file:
mise run generate-concat -- 28 --json timings.json
```

The script automatically adds:

- 5s thumbnail intro (duplicated to avoid ffmpeg drop bug)
- Your content slides with specified durations
- 5s silent outro with last-slide.png

#### Verify concat.txt

```bash
mise run verify-concat -- 28 --check-dims
```

#### Generate video

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

- `XX` = episode number with leading zeros (01, 02, ... 99, 100+)
- `paper-name` = lowercase, hyphenated paper identifier

Examples:

- `01-attention-is-all-you-need`
- `73-raft`
- `130-trusting-trust`
- `200-pastry`

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
export YOUTUBE_PLAYLIST_NETWORKING="PLaaaaaaaaa"
export YOUTUBE_PLAYLIST_OPERATING_SYSTEMS="PLbbbbbbbbb"
```

Or create `youtube/config.json`:

```json
{
  "playlists": {
    "llm": "PLxxxxxxxxxx",
    "distributed-computing": "PLyyyyyyyyyy",
    "security": "PLzzzzzzzzzz",
    "networking": "PLaaaaaaaaa",
    "operating-systems": "PLbbbbbbbbb"
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
