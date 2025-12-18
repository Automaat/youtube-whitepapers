#!/usr/bin/env python3
"""Rename slides directories and PDFs to match whitepaper names."""

import re
import sys
from pathlib import Path

from status_utils import update_episode_status

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent

SLIDES_DIR = PROJECT_ROOT / "youtube" / "pl" / "slides"
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


def rename_slides() -> int:
    """Rename slides directories and PDFs to match whitepaper names."""
    papers = build_paper_map()

    if not papers:
        print("❌ No whitepapers found")
        return 1

    renamed = 0

    # Rename directories
    for item in sorted(SLIDES_DIR.iterdir()):
        if not item.is_dir():
            continue

        match = re.match(r"^(\d+)", item.name)
        if not match:
            continue

        ep_num = int(match.group(1))
        if ep_num not in papers:
            print(f"⚠️  No whitepaper for episode {ep_num}: {item.name}/")
            continue

        new_name = papers[ep_num]
        if item.name == new_name:
            continue

        new_path = item.parent / new_name
        item.rename(new_path)
        print(f"✅ {item.name}/ -> {new_name}/")
        update_episode_status(ep_num, "slides", True)
        renamed += 1

    # Rename PDFs
    for pdf in sorted(SLIDES_DIR.glob("*.pdf")):
        match = re.match(r"^(\d+)", pdf.name)
        if not match:
            continue

        ep_num = int(match.group(1))
        if ep_num not in papers:
            print(f"⚠️  No whitepaper for episode {ep_num}: {pdf.name}")
            continue

        new_name = f"{papers[ep_num]}.pdf"
        if pdf.name == new_name:
            continue

        new_path = pdf.parent / new_name
        pdf.rename(new_path)
        print(f"✅ {pdf.name} -> {new_name}")
        update_episode_status(ep_num, "slides", True)
        renamed += 1

    if renamed == 0:
        print("✅ All slides already match whitepaper names")
    else:
        print(f"\n🎉 Renamed {renamed} items")

    return 0


def main() -> int:
    return rename_slides()


if __name__ == "__main__":
    sys.exit(main())
