# NotebookLM Automator

CLI tool to automate NotebookLM interactions via Playwright browser automation.

## Features

- Add URL/PDF sources to notebooks
- Generate Audio Overview (podcast) + download
- Generate Slides via prompt + export PDF
- Full pipeline automation

## Installation

```bash
cd notebooklm-automator
mise install        # Install Python 3.13 + uv
mise run install    # Install deps + Playwright
```

## Setup

1. Initialize Chrome profile:
```bash
mise run init
```

2. Login to Google (one-time):
```bash
mise run login
```

3. Sign in with your Google account in the browser window.

## Usage

### Create notebook with source

```bash
uv run notebooklm-automator notebook create \
  --name "GLaM Paper" \
  --source "https://arxiv.org/abs/2112.06905"
```

### Generate audio

```bash
uv run notebooklm-automator audio generate \
  --notebook-url "https://notebooklm.google.com/notebook/xxx" \
  --output ./audio/15-glam.m4a
```

### Generate slides

```bash
uv run notebooklm-automator slides generate \
  --notebook-url "https://notebooklm.google.com/notebook/xxx" \
  --prompt-file ./prompts/slides.md \
  --output ./slides/15-glam.pdf
```

### Full pipeline

```bash
uv run notebooklm-automator pipeline \
  --source "https://arxiv.org/abs/2112.06905" \
  --name "15-glam" \
  --output-dir ./output \
  --audio \
  --slides-prompt ./prompts/slides.md
```

## Configuration

Set via environment variables (prefix: `NOTEBOOKLM_`) or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `CHROME_PROFILE_DIR` | `~/.notebooklm-chrome` | Chrome profile directory |
| `CHROME_DEBUG_PORT` | `9222` | Chrome remote debugging port |
| `HEADLESS` | `false` | Run headless (not for login) |
| `AUDIO_GENERATION_TIMEOUT` | `900` | Audio gen timeout (seconds) |

See `.env.example` for all options.

## Development

```bash
# Lint
mise run lint

# Format
mise run format

# Check (lint + format)
mise run check

# Test selectors
uv run notebooklm-automator test-selectors --notebook-url "https://..."
```

## Notes

- Selectors may need updates when NotebookLM UI changes
- Audio generation takes 5-15 minutes
- Personal use only - respect Google ToS
