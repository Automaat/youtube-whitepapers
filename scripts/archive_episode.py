#!/usr/bin/env python3
"""Archive episode files after YouTube upload.

Moves audio, slides, transcript, video, metadata, and thumbnails to archive.
"""

import shutil
import sys
from pathlib import Path

from status_utils import archive_episode_status

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


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python archive_episode.py <episode_number>")
        print("Example: python archive_episode.py 54")
        print()
        print("Moves episode files to archive/ after YouTube upload:")
        print("  - audio/{ep}.m4a → archive/pl/audio/")
        print("  - slides/{ep}/ → archive/pl/slides/")
        print("  - slides/{ep}.pdf → archive/pl/slides/")
        print("  - transcripts/{ep}.json → archive/pl/transcripts/")
        print("  - output/{ep}.mp4 → archive/pl/video/")
        print("  - output/{ep}-metadata.txt → archive/pl/metadata/")
        print("  - thumbnails/{ep}*.png → archive/pl/thumbnails/")
        print()
        print("Available episodes:")
        if AUDIO_DIR.exists():
            for f in sorted(AUDIO_DIR.glob("*.m4a"))[:10]:
                print(f"  {f.stem}")
            total = len(list(AUDIO_DIR.glob("*.m4a")))
            if total > 10:
                print(f"  ... and {total - 10} more")
        return 1

    ep_num = sys.argv[1]
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


if __name__ == "__main__":
    sys.exit(main())
