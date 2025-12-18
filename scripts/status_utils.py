#!/usr/bin/env python3
"""Utilities for managing whitepapers/status.json."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).parent.parent
STATUS_FILE = SCRIPT_DIR / "whitepapers" / "status.json"
WHITEPAPERS_DIR = SCRIPT_DIR / "whitepapers"

PIPELINE_FIELDS = ["audio", "slides", "transcript", "thumbnail", "video", "uploaded"]
PRESERVED_FIELDS = ["notebook_created"]


def load_status() -> dict[str, Any]:
    """Load existing status.json or return empty structure."""
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    return {"papers": [], "summary": {}, "updated": ""}


def save_status(status: dict[str, Any]) -> None:
    """Save status.json with updated timestamp."""
    status["updated"] = datetime.now(UTC).isoformat(timespec="seconds")
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def find_paper_by_episode(papers: list[dict], ep_num: str | int) -> dict | None:
    """Find paper entry by episode number."""
    ep_str = str(ep_num).zfill(2)
    for paper in papers:
        if paper.get("episode") == ep_str:
            return paper
    return None


def get_episode_from_name(name: str) -> str | None:
    """Extract episode number from filename like '01-attention-is-all-you-need'."""
    match = re.match(r"^(\d+)-", name)
    return match.group(1).zfill(2) if match else None


def detect_category(ep_name: str) -> str | None:
    """Detect category from whitepaper location."""
    for category_dir in WHITEPAPERS_DIR.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue
        if category_dir.name == "status.json":
            continue
        matches = list(category_dir.glob(f"*{ep_name}*.pdf"))
        if matches:
            return category_dir.name
    return None


def update_episode_status(ep_num: str | int, field: str, value: bool) -> None:
    """Update single field for an episode in status.json."""
    status = load_status()
    papers = status.get("papers", [])

    ep_str = str(ep_num).zfill(2)
    paper = find_paper_by_episode(papers, ep_str)

    if paper:
        paper[field] = value
    else:
        paper = {"episode": ep_str, "name": "", "category": "", field: value}
        papers.append(paper)
        papers.sort(key=lambda p: p.get("episode", ""))
        status["papers"] = papers

    update_summary(status)
    save_status(status)


def archive_episode_status(ep_num: str | int) -> None:
    """Mark episode as archived, keeping only episode/name/category/archived."""
    status = load_status()
    papers = status.get("papers", [])

    ep_str = str(ep_num).zfill(2)
    paper = find_paper_by_episode(papers, ep_str)

    if paper:
        # Keep only core fields
        archived_paper = {
            "episode": paper.get("episode", ep_str),
            "name": paper.get("name", ""),
            "category": paper.get("category", ""),
            "archived": True,
        }
        idx = papers.index(paper)
        papers[idx] = archived_paper
    else:
        paper = {"episode": ep_str, "name": "", "category": "", "archived": True}
        papers.append(paper)
        papers.sort(key=lambda p: p.get("episode", ""))
        status["papers"] = papers

    update_summary(status)
    save_status(status)


def update_summary(status: dict[str, Any]) -> None:
    """Recalculate summary counts from papers list."""
    papers = status.get("papers", [])
    fields = [
        "notebook_created",
        "audio",
        "slides",
        "transcript",
        "thumbnail",
        "video",
        "uploaded",
        "archived",
    ]

    summary = {"total": len(papers)}
    for field in fields:
        summary[field] = sum(1 for p in papers if p.get(field))

    status["summary"] = summary
