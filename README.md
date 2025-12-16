# YouTube Video Generation Pipeline

Generate YouTube videos from NotebookLM podcasts about AI/ML milestone papers.

## Directory Structure

```
youtube/
├── audio/                    # NotebookLM podcast audio files (.m4a)
├── transcripts/              # Whisper transcriptions (.json)
├── slides/                   # Presentation PDFs and extracted PNGs
├── thumbnails/               # Video thumbnails (.png)
├── output/                   # Final videos (.mp4) and metadata (.txt)
├── prompts/                  # Claude Code prompts for automation
├── transcribe.sh             # Batch transcription script
├── generate-prompt.sh        # Generate Claude Code prompt for video
└── README.md
```

## Full Workflow

### 1. Add Audio from NotebookLM

Export podcast from NotebookLM and save to `audio/`:
```
audio/XX-paper-name.m4a
```

Naming convention: `{number}-{paper-name}.m4a` (e.g., `02-gpt.m4a`)

### 2. Transcribe Audio

Run batch transcription (uses Whisper, Polish language):
```bash
./transcribe.sh
# Or with custom parallelization:
./transcribe.sh 4  # 4 parallel jobs
```

Output: `transcripts/XX-paper-name.json`

### 3. Generate Slides (NotebookLM)

#### Option A: Use existing prompt template
```bash
# Read transcript and create slide prompt
cat prompts/generate-slides-command.md
```

#### Option B: Use Claude Code
Run in fresh Claude Code session:
```
Read the transcript file at milestone-papers/youtube/transcripts/XX-paper-name.json
and create a detailed NotebookLM prompt for generating 10 presentation slides.
```

Then paste the generated prompt into NotebookLM to create slides PDF.

Save slides to: `slides/XX-paper-name.pdf`

### 4. Add Thumbnail

Generate thumbnail in NotebookLM or externally.
Save to: `thumbnails/XX-paper-name.png`

Compress if >2MB:
```bash
pngquant 200 --force --output thumbnails/XX-paper-name-optimized.png thumbnails/XX-paper-name.png
```

### 5. Generate Video

#### Generate Claude Code prompt:
```bash
./generate-prompt.sh XX
# Example:
./generate-prompt.sh 02
```

This outputs:
- File status check (✅/❌)
- Paper URL
- Ready-to-copy Claude Code prompt

#### Run in Claude Code:
Copy the generated prompt and run in a fresh Claude Code session.

The prompt will:
1. Extract slides from PDF to PNG
2. Analyze transcript for slide timing
3. Match slides to transcript content
4. Generate video with ffmpeg
5. Create metadata file with Polish title/description
6. Compress thumbnail if needed

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
| 01-attention-is-all-you-need | https://arxiv.org/abs/1706.03762 |
| 02-gpt | https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf |
| 03-bert | https://arxiv.org/abs/1810.04805 |
| 04-gpt2 | https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf |
| 05-megatron-lm | https://arxiv.org/abs/1909.08053 |
| 06-t5 | https://arxiv.org/abs/1910.10683 |
| 07-zero | https://arxiv.org/abs/1910.02054 |
| 08-scaling-laws | https://arxiv.org/abs/2001.08361 |
| 09-gpt3 | https://arxiv.org/abs/2005.14165 |
| 10-switch-transformers | https://arxiv.org/abs/2101.03961 |
| 11-codex | https://arxiv.org/abs/2107.03374 |
| 12-foundation-models | https://arxiv.org/abs/2108.07258 |
| 13-flan | https://arxiv.org/abs/2109.01652 |
| 14-t0 | https://arxiv.org/abs/2110.08207 |
| 15-glam | https://arxiv.org/abs/2112.06905 |
| 16-webgpt | https://arxiv.org/abs/2112.09332 |
| 17-retro | https://arxiv.org/abs/2112.04426 |
| 18-gopher | https://arxiv.org/abs/2112.11446 |
| 19-chain-of-thought | https://arxiv.org/abs/2201.11903 |

## Requirements

- **whisper** - Audio transcription (`pip install openai-whisper`)
- **ffmpeg** - Video generation (`brew install ffmpeg`)
- **poppler** - PDF to PNG (`brew install poppler`)
- **pngquant** - PNG compression (`brew install pngquant`)
- **jq** - JSON processing (`brew install jq`)

## Quick Start Example

```bash
# 1. Transcribe new audio (if not done)
./transcribe.sh

# 2. Generate prompt for episode 02
./generate-prompt.sh 02

# 3. Copy output and run in Claude Code

# 4. Upload to YouTube:
#    - Video: output/02-gpt.mp4
#    - Metadata: output/02-gpt-metadata.txt
#    - Thumbnail: thumbnails/02-gpt.png (or optimized version)
```
