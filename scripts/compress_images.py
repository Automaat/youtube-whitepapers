#!/usr/bin/env python3
"""Compress PNG files exceeding size threshold using ImageMagick."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run command and return result."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def parse_size(size_str: str) -> int:
    """Parse human-readable size string to bytes (e.g., '2MB' -> 2097152)."""
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

    # Create temp file for output
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

    result = run_cmd(cmd, check=False)
    if result.returncode != 0:
        if tmp_path.exists():
            tmp_path.unlink()
        raise RuntimeError(f"Compression failed: {result.stderr}")

    new_size = tmp_path.stat().st_size

    # Only replace if smaller
    if new_size < old_size:
        tmp_path.replace(src)
    else:
        tmp_path.unlink()
        new_size = old_size  # No change

    return old_size, new_size


def find_images(path: Path) -> list[Path]:
    """Find PNG files from path (directory or glob pattern)."""
    if path.is_dir():
        return sorted(path.glob("**/*.png"))
    elif "*" in str(path):
        # Glob pattern
        parent = path.parent
        pattern = path.name
        return sorted(parent.glob(pattern))
    elif path.is_file() and path.suffix.lower() == ".png":
        return [path]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compress PNG files exceeding size threshold",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s youtube/thumbnails/
  %(prog)s youtube/thumbnails/ --threshold 1MB
  %(prog)s youtube/thumbnails/*.png --dry-run
  %(prog)s youtube/thumbnails/ --quality 90 --colors 128
        """,
    )
    parser.add_argument("path", type=Path, help="Directory or glob pattern")
    parser.add_argument(
        "--threshold",
        default="2MB",
        help="Size threshold (default: 2MB). Examples: 500KB, 1MB, 2MB",
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
        "--dry-run",
        action="store_true",
        help="Show what would be compressed without making changes",
    )
    args = parser.parse_args()

    try:
        threshold = parse_size(args.threshold)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    # Find images
    images = find_images(args.path)

    if not images:
        print(f"❌ No PNG files found: {args.path}")
        return 1

    # Filter by threshold
    large_images = [(img, img.stat().st_size) for img in images if img.stat().st_size > threshold]

    if not large_images:
        print(f"✅ No images exceed {format_size(threshold)}")
        print(f"   Checked {len(images)} files")
        return 0

    print(f"🔍 Found {len(large_images)} images > {format_size(threshold)}")
    print("━" * 60)

    if args.dry_run:
        print("🔄 DRY RUN - no changes will be made")
        print()

    total_old = 0
    total_new = 0
    compressed_count = 0

    for img, size in large_images:
        rel_path = img.relative_to(SCRIPT_DIR) if img.is_relative_to(SCRIPT_DIR) else img

        if args.dry_run:
            print(f"   📁 {rel_path}")
            print(f"      Size: {format_size(size)} → would compress")
            total_old += size
            total_new += size  # Can't know actual size in dry run
        else:
            print(f"🔄 {rel_path}")
            try:
                old_size, new_size = compress_image(img, args.quality, args.colors)
                total_old += old_size
                total_new += new_size

                if new_size < old_size:
                    savings = (1 - new_size / old_size) * 100
                    print(
                        f"   ✅ {format_size(old_size)} → {format_size(new_size)} ({savings:.1f}% smaller)"
                    )
                    compressed_count += 1
                else:
                    print(f"   ⏭️  {format_size(old_size)} (already optimal)")
            except RuntimeError as e:
                print(f"   ❌ {e}")

    print()
    print("━" * 60)

    if args.dry_run:
        print(f"📊 Would check {len(large_images)} files")
        print(f"   Total size: {format_size(total_old)}")
    else:
        if total_old > 0:
            total_savings = (1 - total_new / total_old) * 100 if total_new < total_old else 0
            print(f"📊 Compressed {compressed_count}/{len(large_images)} files")
            print(
                f"   Total: {format_size(total_old)} → {format_size(total_new)} ({total_savings:.1f}% saved)"
            )
        else:
            print("📊 No files compressed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
