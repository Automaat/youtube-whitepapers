"""Extract paper PDF text with page markers into the episode's paper.txt.

The page markers ("=== page N ===") let the script writer and the scenario
reviewer cite exact pages.
"""

import logging
from pathlib import Path

from pypdf import PdfReader

from odczyt.episode import Episode


def extract_pages(pdf: Path) -> list[str]:
    """Return the text of every page of a PDF.

    pypdf logging is raised to ERROR: Type1 font encoding warnings flood the
    output and do not affect the extracted text.
    """
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    reader = PdfReader(pdf)
    return [(page.extract_text() or "").strip() for page in reader.pages]


def format_pages(pages: list[str]) -> str:
    """Join page texts with 1-based page markers."""
    return "\n\n".join(f"=== page {i} ===\n{text}" for i, text in enumerate(pages, 1)) + "\n"


def write_paper_text(ep: Episode) -> int:
    """Write paper.txt for an episode; return the page count."""
    pdf = ep.repo / ep.config["paper"]
    if not pdf.exists():
        raise FileNotFoundError(f"Paper not found: {pdf}")
    pages = extract_pages(pdf)
    ep.file("paper.txt").write_text(format_pages(pages), encoding="utf-8")
    return len(pages)
