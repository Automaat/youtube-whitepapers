#!/usr/bin/env python3
"""Rename audio files to match whitepaper names."""

import re
import sys
from pathlib import Path

from status_utils import sort_by_episode, update_episode_status

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent

AUDIO_DIR = PROJECT_ROOT / "youtube" / "pl" / "audio"
WHITEPAPERS_DIR = PROJECT_ROOT / "whitepapers"


def build_paper_map() -> dict[int, str]:
    """Build mapping from episode number to paper name."""
    papers: dict[int, str] = {}

    for category_dir in WHITEPAPERS_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        for pdf in category_dir.glob("*.pdf"):
            if "slides" in pdf.name:
                continue

            name = pdf.stem
            match = re.match(r"^(\d+)-", name)
            if match:
                ep_num = int(match.group(1))
                papers[ep_num] = name

    return papers


def rename_audio_files() -> int:
    """Rename audio files to match whitepaper names."""
    papers = build_paper_map()

    if not papers:
        print("❌ No whitepapers found")
        return 1

    renamed = 0
    for audio_file in sort_by_episode(list(AUDIO_DIR.glob("*.m4a"))):
        match = re.match(r"^(\d+)", audio_file.name)
        if not match:
            continue

        ep_num = int(match.group(1))
        if ep_num not in papers:
            print(f"⚠️  No whitepaper for episode {ep_num}: {audio_file.name}")
            continue

        new_name = f"{papers[ep_num]}.m4a"
        if audio_file.name == new_name:
            continue

        new_path = audio_file.parent / new_name
        audio_file.rename(new_path)
        print(f"✅ {audio_file.name} -> {new_name}")
        update_episode_status(ep_num, "audio", True)
        renamed += 1

    if renamed == 0:
        print("✅ All audio files already match whitepaper names")
    else:
        print(f"\n🎉 Renamed {renamed} files")

    return 0


def main() -> int:
    return rename_audio_files()


if __name__ == "__main__":
    sys.exit(main())
