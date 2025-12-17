#!/usr/bin/env python3
"""Rename numeric thumbnails to match whitepaper names and compress to target size."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
THUMBNAILS_DIR = SCRIPT_DIR / "youtube" / "thumbnails"
WHITEPAPERS_DIR = SCRIPT_DIR / "whitepapers" / "distributed-computing"


def parse_size(size_str: str) -> int:
    """Parse human-readable size string to bytes (e.g., '1.9MB' -> 1992294)."""
    match = re.match(r"^(\d+(?:\.\d+)?)\s*(B|KB|MB|GB)?$", size_str.upper())
    if not match:
        raise ValueError(f"Invalid size format: {size_str}")

    value = float(match.group(1))
    unit = match.group(2) or "B"

    multipliers = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
    return int(value * multipliers[unit])


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable string."""
    if size_bytes >= 1024**3:
        return f"{size_bytes / 1024**3:.1f}GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / 1024**2:.1f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f}KB"
    return f"{size_bytes}B"


def compress_image(src: Path, quality: int, colors: int) -> tuple[int, int]:
    """Compress PNG image in-place. Returns (old_size, new_size)."""
    old_size = src.stat().st_size
    tmp_path = src.with_suffix(".tmp.png")

    cmd = [
        "convert",
        str(src),
        "-quality",
        str(quality),
        "-colors",
        str(colors),
        str(tmp_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        if tmp_path.exists():
            tmp_path.unlink()
        raise RuntimeError(f"Compression failed: {result.stderr}")

    new_size = tmp_path.stat().st_size

    if new_size < old_size:
        tmp_path.replace(src)
    else:
        tmp_path.unlink()
        new_size = old_size

    return old_size, new_size


def find_numeric_thumbnails() -> list[tuple[Path, int]]:
    """Find thumbnails with numeric-only names (e.g., 64.png)."""
    pattern = re.compile(r"^(\d+)\.png$")
    results = []

    for path in THUMBNAILS_DIR.glob("*.png"):
        match = pattern.match(path.name)
        if match:
            ep_num = int(match.group(1))
            results.append((path, ep_num))

    return sorted(results, key=lambda x: x[1])


def find_whitepaper_name(ep_num: int) -> str | None:
    """Find whitepaper name for episode number."""
    pattern = f"{ep_num}-*.pdf"
    matches = list(WHITEPAPERS_DIR.glob(pattern))

    if not matches:
        return None

    pdf_name = matches[0].stem
    name_part = pdf_name.split("-", 1)[1] if "-" in pdf_name else pdf_name
    return name_part


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rename numeric thumbnails to match whitepaper names and compress",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Rename and compress
  %(prog)s --dry-run                # Preview changes
  %(prog)s --skip-compress          # Rename only
  %(prog)s --threshold 1.5MB        # Custom size threshold
        """,
    )
    parser.add_argument(
        "--threshold",
        default="1.9MB",
        help="Compression size threshold (default: 1.9MB)",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=80,
        help="PNG quality 0-100 (default: 80)",
    )
    parser.add_argument(
        "--colors",
        type=int,
        default=256,
        help="Number of colors (default: 256)",
    )
    parser.add_argument(
        "--skip-compress",
        action="store_true",
        help="Skip compression step",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    args = parser.parse_args()

    try:
        threshold = parse_size(args.threshold)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    thumbnails = find_numeric_thumbnails()

    if not thumbnails:
        print("✅ No numeric thumbnails found to rename")
        return 0

    print(f"🔍 Found {len(thumbnails)} numeric thumbnails")
    print("━" * 60)

    if args.dry_run:
        print("🔄 DRY RUN - no changes will be made")
        print()

    renamed_count = 0
    compressed_count = 0
    total_saved = 0

    for path, ep_num in thumbnails:
        paper_name = find_whitepaper_name(ep_num)

        if not paper_name:
            print(f"⚠️  {path.name}: No whitepaper found for episode {ep_num}")
            continue

        new_name = f"{ep_num}-{paper_name}.png"
        new_path = path.parent / new_name

        if args.dry_run:
            print(f"📁 {path.name} → {new_name}")
            size = path.stat().st_size
            if size > threshold and not args.skip_compress:
                print(f"   {format_size(size)} → would compress")
            renamed_count += 1
        else:
            print(f"🔄 {path.name} → {new_name}")
            path.rename(new_path)
            renamed_count += 1

            if not args.skip_compress:
                size = new_path.stat().st_size
                if size > threshold:
                    try:
                        old_size, new_size = compress_image(
                            new_path, args.quality, args.colors
                        )
                        if new_size < old_size:
                            savings = old_size - new_size
                            total_saved += savings
                            pct = (1 - new_size / old_size) * 100
                            print(
                                f"   ✅ {format_size(old_size)} → {format_size(new_size)} ({pct:.1f}% smaller)"
                            )
                            compressed_count += 1
                        else:
                            print(f"   ⏭️  {format_size(old_size)} (already optimal)")
                    except RuntimeError as e:
                        print(f"   ❌ Compression failed: {e}")

    print()
    print("━" * 60)

    if args.dry_run:
        print(f"📊 Would rename {renamed_count} thumbnails")
    else:
        print(f"📊 Renamed {renamed_count} thumbnails")
        if not args.skip_compress:
            print(f"   Compressed {compressed_count} files, saved {format_size(total_saved)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
