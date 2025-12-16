#!/usr/bin/env python3
"""Generate Claude Code prompt for video creation."""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMPLATE_FILE = SCRIPT_DIR / "prompts" / "generate-video-command.md"

PAPER_URLS = {
    "01-attention-is-all-you-need": "https://arxiv.org/abs/1706.03762",
    "02-gpt": "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf",
    "03-bert": "https://arxiv.org/abs/1810.04805",
    "04-gpt2": "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf",
    "05-megatron-lm": "https://arxiv.org/abs/1909.08053",
    "06-t5": "https://arxiv.org/abs/1910.10683",
    "07-zero": "https://arxiv.org/abs/1910.02054",
    "08-scaling-laws": "https://arxiv.org/abs/2001.08361",
    "09-gpt3": "https://arxiv.org/abs/2005.14165",
    "10-switch-transformers": "https://arxiv.org/abs/2101.03961",
    "11-codex": "https://arxiv.org/abs/2107.03374",
    "12-foundation-models": "https://arxiv.org/abs/2108.07258",
    "13-flan": "https://arxiv.org/abs/2109.01652",
    "14-t0": "https://arxiv.org/abs/2110.08207",
    "15-glam": "https://arxiv.org/abs/2112.06905",
    "16-webgpt": "https://arxiv.org/abs/2112.09332",
    "17-retro": "https://arxiv.org/abs/2112.04426",
    "18-gopher": "https://arxiv.org/abs/2112.11446",
    "19-chain-of-thought": "https://arxiv.org/abs/2201.11903",
}

def load_template() -> str:
    """Load prompt template from markdown file."""
    template = TEMPLATE_FILE.read_text()
    template = template.replace("[EPISODE_NUMBER]-[EPISODE_NAME]", "{ep_name}")
    template = template.replace("[arxiv URL or paper URL]", "{paper_url}")
    return template


def find_episode(ep_num: str) -> Path | None:
    """Find audio file matching episode number."""
    audio_dir = SCRIPT_DIR / "audio"
    matches = list(audio_dir.glob(f"{ep_num}-*.m4a"))
    return matches[0] if matches else None


def check_file(path: Path, label: str) -> None:
    """Print file status."""
    status = "✅" if path.exists() else "❌"
    print(f"{status} {label}: {path.relative_to(SCRIPT_DIR)}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ./generate-prompt.py <episode_number>")
        print("Example: ./generate-prompt.py 01")
        print()
        print("Available episodes:")
        audio_dir = SCRIPT_DIR / "audio"
        if audio_dir.exists():
            for f in sorted(audio_dir.glob("*.m4a")):
                print(f"  {f.stem}")
        sys.exit(1)

    ep_num = sys.argv[1]
    audio_file = find_episode(ep_num)

    if not audio_file:
        print(f"❌ No audio file found for episode {ep_num}")
        sys.exit(1)

    ep_name = audio_file.stem
    paper_url = PAPER_URLS.get(ep_name, "https://arxiv.org/")

    print(f"📋 Episode: {ep_name}")
    print("━" * 40)
    print()
    print("Required files:")
    check_file(SCRIPT_DIR / "audio" / f"{ep_name}.m4a", "Audio")
    check_file(SCRIPT_DIR / "slides" / f"{ep_name}.pdf", "Slides")
    check_file(SCRIPT_DIR / "transcripts" / f"{ep_name}.json", "Transcript")
    print()
    print(f"📄 Paper URL: {paper_url}")
    print()
    print("━" * 40)
    print("📝 CLAUDE CODE PROMPT (copy below):")
    print("━" * 40)
    print()
    template = load_template()
    print(template.format(ep_name=ep_name, paper_url=paper_url))


if __name__ == "__main__":
    main()
