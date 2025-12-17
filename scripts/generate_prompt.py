#!/usr/bin/env python3
"""Generate Claude Code prompt for video creation."""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
YOUTUBE_DIR = SCRIPT_DIR / "youtube"
ASSETS_DIR = YOUTUBE_DIR / "pl"
TEMPLATE_FILE = YOUTUBE_DIR / "prompts" / "generate-video-command.md"


def load_template() -> str:
    """Load prompt template from markdown file."""
    template = TEMPLATE_FILE.read_text()
    template = template.replace("[EPISODE_NUMBER]-[EPISODE_NAME]", "{ep_name}")
    return template


def find_episode(ep_num: str) -> Path | None:
    """Find audio file matching episode number."""
    audio_dir = ASSETS_DIR / "audio"
    matches = list(audio_dir.glob(f"{ep_num}-*.m4a"))
    return matches[0] if matches else None


def check_file(path: Path, label: str) -> None:
    """Print file status."""
    status = "✅" if path.exists() else "❌"
    print(f"{status} {label}: {path.relative_to(SCRIPT_DIR)}")


def main() -> None:
    """Generate and print Claude Code prompt for video creation."""
    if len(sys.argv) < 2:
        print("Usage: ./generate-prompt.py <episode_number>")
        print("Example: ./generate-prompt.py 01")
        print()
        print("Available episodes:")
        audio_dir = ASSETS_DIR / "audio"
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

    print(f"📋 Episode: {ep_name}")
    print("━" * 40)
    print()
    print("Required files:")
    check_file(ASSETS_DIR / "audio" / f"{ep_name}.m4a", "Audio")
    check_file(ASSETS_DIR / "slides" / f"{ep_name}.pdf", "Slides")
    check_file(ASSETS_DIR / "transcripts" / f"{ep_name}.json", "Transcript")
    print()
    print("━" * 40)
    print("📝 CLAUDE CODE PROMPT (copy below):")
    print("━" * 40)
    print()
    template = load_template()
    print(template.format(ep_name=ep_name))


if __name__ == "__main__":
    main()
