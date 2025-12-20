#!/usr/bin/env python3
"""Generate whitepapers/status.json by scanning all directories."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from status_utils import (
    PRESERVED_FIELDS,
    SCRIPT_DIR,
    WHITEPAPERS_DIR,
    load_status,
    save_status,
    update_summary,
)

YOUTUBE_DIR = SCRIPT_DIR / "youtube"
ASSETS_DIR = YOUTUBE_DIR / "pl"
ARCHIVE_DIR = SCRIPT_DIR / "archive" / "pl"

AUDIO_DIRS = [ASSETS_DIR / "audio", ARCHIVE_DIR / "audio"]
SLIDES_DIRS = [ASSETS_DIR / "slides", ARCHIVE_DIR / "slides"]
TRANSCRIPTS_DIRS = [ASSETS_DIR / "transcripts", ARCHIVE_DIR / "transcripts"]
THUMBNAILS_DIRS = [YOUTUBE_DIR / "thumbnails", ARCHIVE_DIR / "thumbnails"]
VIDEO_DIRS = [YOUTUBE_DIR / "output", ARCHIVE_DIR / "video"]
SLIDES_PROMPTS_DIR = YOUTUBE_DIR / "prompts" / "slides"


def scan_whitepapers() -> list[dict]:
    """Scan whitepapers directory for all papers."""
    papers = []

    for category_dir in sorted(WHITEPAPERS_DIR.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue
        if category_dir.name == "status.json":
            continue

        category = category_dir.name

        for pdf in sorted(category_dir.glob("*.pdf")):
            if "-slides" in pdf.name:
                continue

            name = pdf.stem
            match = re.match(r"^(\d+)-(.+)$", name)
            if not match:
                continue

            ep_num = match.group(1).zfill(2)
            paper_name = match.group(2)

            papers.append(
                {
                    "episode": ep_num,
                    "name": paper_name,
                    "category": category,
                }
            )

    return papers


def check_exists(dirs: list[Path], pattern: str) -> bool:
    """Check if file matching pattern exists in any of the directories."""
    for d in dirs:
        if not d.exists():
            continue
        if list(d.glob(pattern)):
            return True
    return False


def check_slides_exist(dirs: list[Path], ep_name: str) -> bool:
    """Check if slides exist for episode (PDF or extracted PNGs)."""
    for d in dirs:
        if not d.exists():
            continue
        # Check for PDF file directly in slides dir
        if (d / f"{ep_name}.pdf").exists():
            return True
        # Check for extracted PNGs in episode subdirectory
        slides_dir = d / ep_name
        if slides_dir.is_dir() and list(slides_dir.glob("*.png")):
            return True
    return False


def check_archived(ep_name: str) -> bool:
    """Check if episode is archived (has files in archive directory)."""
    archive_audio = ARCHIVE_DIR / "audio" / f"{ep_name}.m4a"
    archive_video = ARCHIVE_DIR / "video" / f"{ep_name}.mp4"
    return archive_audio.exists() or archive_video.exists()


def check_slides_prompt(ep_name: str) -> bool:
    """Check if slides prompt exists for episode."""
    return (SLIDES_PROMPTS_DIR / f"{ep_name}.md").exists()


def generate_status() -> dict:
    """Generate complete status by scanning directories."""
    existing = load_status()
    existing_papers = {p.get("episode"): p for p in existing.get("papers", [])}

    papers = scan_whitepapers()

    for paper in papers:
        ep_num = paper["episode"]
        ep_name = f"{ep_num}-{paper['name']}"

        old_paper = existing_papers.get(ep_num, {})

        # Skip status updates for archived episodes - preserve all existing fields
        if old_paper.get("archived"):
            paper.update(
                {k: v for k, v in old_paper.items() if k not in ("episode", "name", "category")}
            )
            continue

        for field in PRESERVED_FIELDS:
            if field in old_paper:
                paper[field] = old_paper[field]

        if old_paper.get("uploaded"):
            paper["uploaded"] = True

        paper["audio"] = check_exists(AUDIO_DIRS, f"{ep_name}.m4a")
        paper["slides_prompt"] = check_slides_prompt(ep_name)
        paper["slides"] = check_slides_exist(SLIDES_DIRS, ep_name)
        paper["transcript"] = check_exists(TRANSCRIPTS_DIRS, f"{ep_name}.json")
        paper["thumbnail"] = check_exists(THUMBNAILS_DIRS, f"{ep_name}.png") or check_exists(
            THUMBNAILS_DIRS, f"{ep_name}-optimized.png"
        )
        paper["video"] = check_exists(VIDEO_DIRS, f"{ep_name}.mp4")

        if check_archived(ep_name):
            paper["archived"] = True

    status = {"papers": papers, "summary": {}, "updated": ""}
    update_summary(status)
    return status


def get_ready_for_video(papers: list[dict]) -> list[dict]:
    """Get episodes ready for video generation (have all assets except video)."""
    return [
        p
        for p in papers
        if not p.get("archived")
        and p.get("audio")
        and p.get("slides")
        and p.get("transcript")
        and p.get("thumbnail")
        and not p.get("video")
    ]


def get_ready_for_slides(papers: list[dict]) -> list[dict]:
    """Get episodes ready for slide prompt generation (have audio+transcript, no slides)."""
    return [
        p
        for p in papers
        if not p.get("archived")
        and p.get("audio")
        and p.get("transcript")
        and not p.get("slides_prompt")
        and not p.get("slides_scheduled")
        and not p.get("slides")
    ]


def get_ready_for_upload(papers: list[dict]) -> list[dict]:
    """Get episodes ready for upload (have video, not uploaded)."""
    return [
        p
        for p in papers
        if not p.get("archived")
        and p.get("video")
        and not p.get("uploaded")
    ]


def get_ready_for_archive(papers: list[dict]) -> list[dict]:
    """Get episodes ready for archive (uploaded, not archived)."""
    return [
        p
        for p in papers
        if p.get("uploaded")
        and not p.get("archived")
    ]


def main() -> int:
    print("📊 Generating status.json")
    print("━" * 40)

    status = generate_status()
    papers = status["papers"]
    summary = status["summary"]

    print(f"   Total papers: {summary['total']}")
    print(f"   📓 Notebook created: {summary.get('notebook_created', 0)}")
    print(f"   🎙️  Audio: {summary.get('audio', 0)}")
    print(f"   🖼️  Thumbnail: {summary.get('thumbnail', 0)}")
    print(f"   📝 Transcript: {summary.get('transcript', 0)}")
    print(f"   📑 Slides: {summary.get('slides', 0)}")
    print(f"   🎬 Video: {summary.get('video', 0)}")
    print(f"   📤 Uploaded: {summary.get('uploaded', 0)}")
    print(f"   📦 Archived: {summary.get('archived', 0)}")

    save_status(status)

    print()
    print("━" * 40)
    print(f"✅ Saved to whitepapers/status.json ({len(papers)} papers)")

    # Ready for video generation
    ready_video = get_ready_for_video(papers)
    if ready_video:
        print()
        print("🎬 Ready for video generation:")
        for p in ready_video:
            print(f"   {p['episode']}-{p['name']}")

    # Ready for slide prompts
    ready_slides = get_ready_for_slides(papers)
    if ready_slides:
        print()
        print("📑 Ready for slide prompts (have audio, need slides):")
        for p in ready_slides:
            print(f"   {p['episode']}-{p['name']}")

    # Ready for upload
    ready_upload = get_ready_for_upload(papers)
    if ready_upload:
        print()
        print("📤 Ready for upload:")
        for p in ready_upload:
            print(f"   {p['episode']}-{p['name']}")

    # Ready for archive
    ready_archive = get_ready_for_archive(papers)
    if ready_archive:
        print()
        print("📦 Ready for archive:")
        for p in ready_archive:
            print(f"   {p['episode']}-{p['name']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
