#!/usr/bin/env python3
"""Archive episode files after YouTube upload.

Moves audio, slides, transcript, video, metadata, and thumbnails to archive.
"""

import shutil
import sys
from pathlib import Path

from status_utils import archive_episode_status, load_status

SCRIPT_DIR = Path(__file__).parent.parent
YOUTUBE_DIR = SCRIPT_DIR / "youtube"
ASSETS_DIR = YOUTUBE_DIR / "pl"
ARCHIVE_DIR = SCRIPT_DIR / "archive" / "pl"

# Source directories
AUDIO_DIR = ASSETS_DIR / "audio"
SLIDES_DIR = ASSETS_DIR / "slides"
TRANSCRIPTS_DIR = ASSETS_DIR / "transcripts"
OUTPUT_DIR = YOUTUBE_DIR / "output"
THUMBNAILS_DIR = YOUTUBE_DIR / "thumbnails"

# Archive destinations
ARCHIVE_AUDIO = ARCHIVE_DIR / "audio"
ARCHIVE_SLIDES = ARCHIVE_DIR / "slides"
ARCHIVE_TRANSCRIPTS = ARCHIVE_DIR / "transcripts"
ARCHIVE_VIDEO = ARCHIVE_DIR / "video"
ARCHIVE_METADATA = ARCHIVE_DIR / "metadata"
ARCHIVE_THUMBNAILS = ARCHIVE_DIR / "thumbnails"


def find_episode(ep_num: str) -> str | None:
    """Find episode name from audio file matching episode number."""
    matches = list(AUDIO_DIR.glob(f"{ep_num}-*.m4a"))
    return matches[0].stem if matches else None


def get_ready_to_archive() -> list[str]:
    """Get list of episode numbers that are uploaded but not archived."""
    status = load_status()
    papers = status.get("papers", [])
    ready = []

    for paper in papers:
        uploaded = paper.get("uploaded", False)
        archived = paper.get("archived", False)

        if uploaded and not archived:
            ready.append(paper["episode"])

    return ready


def move_file(src: Path, dst_dir: Path, label: str) -> bool:
    """Move single file to destination directory. Returns True if moved."""
    if not src.exists():
        print(f"   ⚠️  {label}: not found ({src.name})")
        return False

    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name

    try:
        if dst.exists():
            dst.unlink()
            shutil.move(str(src), str(dst))
            print(f"   ✅ {label}: {src.name} (replaced)")
        else:
            shutil.move(str(src), str(dst))
            print(f"   ✅ {label}: {src.name}")
        return True
    except OSError as e:
        print(f"   ❌ {label}: {e}")
        return False


def move_directory(src: Path, dst_dir: Path, label: str) -> bool:
    """Move entire directory to destination. Returns True if moved."""
    if not src.exists():
        print(f"   ⚠️  {label}: not found ({src.name})")
        return False

    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name

    try:
        replaced = False
        if dst.exists():
            shutil.rmtree(dst)
            replaced = True
        shutil.move(str(src), str(dst))
        file_count = len(list(dst.glob("*")))
        suffix = " (replaced)" if replaced else ""
        print(f"   ✅ {label}: {src.name}/ ({file_count} files){suffix}")
        return True
    except OSError as e:
        print(f"   ❌ {label}: {e}")
        return False


def archive_single_episode(ep_num: str) -> int:
    """Archive a single episode. Returns 0 on success, 1 on failure."""
    ep_name = find_episode(ep_num)

    if not ep_name:
        print(f"❌ No audio file found for episode {ep_num}")
        return 1

    print(f"📦 Archiving episode: {ep_name}")
    print("━" * 50)

    moved = 0
    total = 0

    # Audio
    total += 1
    if move_file(AUDIO_DIR / f"{ep_name}.m4a", ARCHIVE_AUDIO, "Audio"):
        moved += 1

    # Slides directory
    total += 1
    if move_directory(SLIDES_DIR / ep_name, ARCHIVE_SLIDES, "Slides"):
        moved += 1

    # Slides PDF
    total += 1
    if move_file(SLIDES_DIR / f"{ep_name}.pdf", ARCHIVE_SLIDES, "Slides PDF"):
        moved += 1

    # Transcript
    total += 1
    if move_file(TRANSCRIPTS_DIR / f"{ep_name}.json", ARCHIVE_TRANSCRIPTS, "Transcript"):
        moved += 1

    # Video
    total += 1
    if move_file(OUTPUT_DIR / f"{ep_name}.mp4", ARCHIVE_VIDEO, "Video"):
        moved += 1

    # Metadata
    total += 1
    if move_file(OUTPUT_DIR / f"{ep_name}-metadata.txt", ARCHIVE_METADATA, "Metadata"):
        moved += 1

    # Thumbnails (all variants)
    thumbnail_files = list(THUMBNAILS_DIR.glob(f"{ep_name}*.png"))
    for thumb in thumbnail_files:
        total += 1
        if move_file(thumb, ARCHIVE_THUMBNAILS, "Thumbnail"):
            moved += 1

    # Summary
    print()
    print("━" * 50)
    if moved == total:
        print(f"✅ Archived {moved}/{total} items successfully")
        archive_episode_status(ep_num)
    elif moved > 0:
        print(f"⚠️  Archived {moved}/{total} items (some skipped)")
        archive_episode_status(ep_num)
    else:
        print("❌ No items archived")

    return 0 if moved > 0 else 1


def main() -> int:
    # No argument: archive all ready episodes
    if len(sys.argv) < 2:
        ready = get_ready_to_archive()

        if not ready:
            print("✅ No episodes ready to archive")
            print()
            print("Episodes are ready to archive when:")
            print("  - uploaded: true")
            print("  - archived: false")
            return 0

        print(f"📦 Found {len(ready)} episode(s) ready to archive:")
        for ep in ready:
            print(f"   • Episode {ep}")
        print()

        success = 0
        failed = 0

        for ep in ready:
            result = archive_single_episode(ep)
            if result == 0:
                success += 1
            else:
                failed += 1
            if ep != ready[-1]:  # Not last episode
                print()

        # Final summary
        print()
        print("=" * 50)
        print(f"📊 Summary: {success} archived, {failed} failed")
        return 0 if failed == 0 else 1

    # Single episode specified
    ep_num = sys.argv[1]
    return archive_single_episode(ep_num)


if __name__ == "__main__":
    sys.exit(main())
