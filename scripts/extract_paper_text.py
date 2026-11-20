#!/usr/bin/env python3
"""Extract paper PDF text with page markers into the episode's paper.txt.

The page markers ("=== page N ===") let the script writer and the scenario
reviewer cite exact pages.

Usage: python scripts/extract_paper_text.py 73
"""

import logging
import sys
from pathlib import Path

from pypdf import PdfReader

from episode_pipeline import REPO_DIR, find_episode_dir, load_episode


def extract_pages(pdf: Path) -> list[str]:
    """Return the text of every page of a PDF."""
    # Type1 font encoding warnings flood stdout; text output is unaffected.
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    reader = PdfReader(pdf)
    return [(page.extract_text() or "").strip() for page in reader.pages]


def format_pages(pages: list[str]) -> str:
    """Join page texts with 1-based page markers."""
    return "\n\n".join(f"=== page {i} ===\n{text}" for i, text in enumerate(pages, 1)) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: extract_paper_text.py EPISODE_NUM")
        return 1
    episode_dir = find_episode_dir(sys.argv[1])
    if episode_dir is None:
        print(f"❌ No episode directory for {sys.argv[1]}")
        return 1
    pdf = REPO_DIR / load_episode(episode_dir)["paper"]
    if not pdf.exists():
        print(f"❌ Paper not found: {pdf}")
        return 1
    pages = extract_pages(pdf)
    out = episode_dir / "paper.txt"
    out.write_text(format_pages(pages), encoding="utf-8")
    print(f"✅ {len(pages)} pages → {out.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
