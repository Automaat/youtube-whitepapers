# Command for Claude Code - Generate Slide Prompts

Run this in a fresh Claude Code session for each transcript:

---

## Command

```text
Read the transcript file at ./youtube/transcripts/6 and create a detailed NotebookLM prompt for generating 11 presentation slides.

Requirements:
- Audience: technical Software Engineering experts
- 11 slides total
- Slides 1-10: title + 4-6 detailed bullet points covering paper content
- Slide 11: Question slide - extract the question asked at the end of the podcast transcript (display only the question text)
- Use original English names for technical terms, architectures, methods, and metrics

Analyze the podcast flow and create specific slide content that matches what was discussed. Include:
- Exact technical terms mentioned
- Specific numbers/results from experiments
- Key comparisons and benchmarks
- Named architectures and methods

Output format - a complete prompt ready to paste into NotebookLM:

## NotebookLM Prompt

Generate 11 presentation slides based on the podcast about [PAPER NAME].

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

### Slide 1: [Title]
Content to include:
- [detailed point 1]
- [detailed point 2]
...

### Slide 2-10: [Titles]
(content slides covering the paper)

### Slide 11: Question for You
Display only the question asked at the end of the podcast (find it in the transcript).

When done save to ./youtube/prompts/slides/
```

---

## Episode list

Replace [EPISODE] with:

- 01-attention-is-all-you-need
- 02-gpt
- 03-bert
- 04-gpt2
- 05-megatron-lm
- 06-t5
- 07-zero
- 08-scaling-laws
- 09-gpt3
- 10-switch-transformers
- 11-codex
- 12-foundation-models
- 13-flan
- 14-t0
- 15-glam
- 16-webgpt
- 17-retro
- 18-gopher
- 19-chain-of-thought
