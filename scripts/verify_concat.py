#!/usr/bin/env python3
"""Verify concat.txt for correct duration, file existence, and image dimensions."""

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
YOUTUBE_DIR = SCRIPT_DIR / "youtube"
ASSETS_DIR = YOUTUBE_DIR / "pl"


@dataclass
class ConcatEntry:
    """Single entry from concat.txt."""

    file_path: Path
    duration: float
    line_number: int


def run_cmd(cmd: list[str]) -> str:
    """Run command and return stdout."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_audio_duration(file_path: Path) -> float:
    """Get audio duration in seconds using ffprobe."""
    output = run_cmd(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(file_path),
        ]
    )
    return float(output)


def get_image_dimensions(file_path: Path) -> tuple[int, int]:
    """Get image dimensions using ImageMagick."""
    output = run_cmd(["identify", "-format", "%wx%h", str(file_path)])
    width, height = output.split("x")
    return int(width), int(height)


def parse_concat(concat_path: Path) -> list[ConcatEntry]:
    """Parse concat.txt and return list of entries."""
    entries = []
    lines = concat_path.read_text().strip().split("\n")

    file_pattern = re.compile(r"^file\s+'(.+)'$")
    duration_pattern = re.compile(r"^duration\s+([\d.]+)$")

    current_file = None
    current_line = 0

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        file_match = file_pattern.match(line)
        if file_match:
            current_file = Path(file_match.group(1))
            current_line = i
            continue

        duration_match = duration_pattern.match(line)
        if duration_match and current_file:
            duration = float(duration_match.group(1))
            entries.append(ConcatEntry(current_file, duration, current_line))
            current_file = None

    # Handle last file without duration (final slide)
    if current_file:
        entries.append(ConcatEntry(current_file, 0.0, current_line))

    return entries


def find_episode_audio(ep_num: str) -> Path | None:
    """Find audio file for episode number."""
    audio_dir = ASSETS_DIR / "audio"
    matches = list(audio_dir.glob(f"{ep_num}-*.m4a"))
    return matches[0] if matches else None


def verify_files_exist(entries: list[ConcatEntry]) -> list[str]:
    """Verify all referenced files exist. Returns list of errors."""
    errors = []
    for entry in entries:
        if not entry.file_path.exists():
            errors.append(f"Line {entry.line_number}: File not found: {entry.file_path}")
    return errors


def verify_dimensions(entries: list[ConcatEntry]) -> list[str]:
    """Verify all images have consistent dimensions. Returns list of errors."""
    errors = []
    dimensions: dict[tuple[int, int], list[str]] = {}

    for entry in entries:
        if not entry.file_path.exists():
            continue
        try:
            dims = get_image_dimensions(entry.file_path)
            dimensions.setdefault(dims, []).append(entry.file_path.name)
        except (ValueError, subprocess.CalledProcessError):
            errors.append(f"Line {entry.line_number}: Cannot read dimensions: {entry.file_path}")

    if len(dimensions) > 1:
        errors.append("Inconsistent image dimensions detected:")
        for dims, files in sorted(dimensions.items(), key=lambda x: -len(x[1])):
            errors.append(f"  {dims[0]}x{dims[1]}: {len(files)} files ({', '.join(files[:3])}...)")

    return errors


def verify_duration(
    entries: list[ConcatEntry], audio_path: Path, tolerance: float = 0.5
) -> tuple[bool, list[str]]:
    """Verify total duration matches audio + 5s outro. Returns (ok, messages)."""
    messages = []

    total_duration = sum(e.duration for e in entries)
    audio_duration = get_audio_duration(audio_path)
    expected_duration = audio_duration + 5.0

    messages.append(f"Audio duration:    {audio_duration:.2f}s")
    messages.append(f"Concat duration:   {total_duration:.2f}s")
    messages.append(f"Expected:          {expected_duration:.2f}s (audio + 5s)")

    diff = total_duration - expected_duration
    ok = abs(diff) <= tolerance

    if ok:
        messages.append(f"✅ Duration OK (diff: {diff:+.2f}s)")
    else:
        messages.append(f"❌ Duration mismatch: {diff:+.2f}s")

    return ok, messages


def verify_structure(entries: list[ConcatEntry]) -> list[str]:
    """Verify concat structure (thumbnail first, last-slide at end)."""
    errors = []

    if not entries:
        errors.append("Empty concat.txt")
        return errors

    # Check first entry is thumbnail
    first_file = entries[0].file_path.name
    if "thumbnail" not in first_file.lower():
        errors.append(f"⚠️  First file should be thumbnail, got: {first_file}")

    # Check last entry is last-slide
    last_file = entries[-1].file_path.name
    if "last-slide" not in last_file.lower():
        errors.append(f"⚠️  Last file should be last-slide.png, got: {last_file}")

    # Check for very short durations (< 3s)
    for entry in entries:
        if 0 < entry.duration < 3:
            errors.append(
                f"⚠️  Very short duration ({entry.duration}s) for {entry.file_path.name}"
            )

    # Check for very long durations (> 180s / 3 min)
    for entry in entries:
        if entry.duration > 180:
            errors.append(
                f"⚠️  Very long duration ({entry.duration:.0f}s) for {entry.file_path.name}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify concat.txt for video generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 28
  %(prog)s 28 --concat path/to/concat.txt
  %(prog)s 28 --check-dims
        """,
    )
    parser.add_argument("episode", help="Episode number (e.g., 28)")
    parser.add_argument("--concat", type=Path, help="Custom concat.txt path")
    parser.add_argument(
        "--check-dims", action="store_true", help="Check image dimensions consistency"
    )
    args = parser.parse_args()

    ep_num = args.episode

    # Find concat file
    if args.concat:
        concat_path = args.concat
    else:
        slides_dir = ASSETS_DIR / "slides"
        matches = list(slides_dir.glob(f"{ep_num}-*/"))
        if not matches:
            print(f"❌ No slides directory found for episode {ep_num}")
            return 1
        concat_path = matches[0] / "concat.txt"

    if not concat_path.exists():
        print(f"❌ concat.txt not found: {concat_path}")
        return 1

    # Find audio file
    audio_path = find_episode_audio(ep_num)
    if not audio_path:
        print(f"❌ No audio file found for episode {ep_num}")
        return 1

    print(f"🔍 Verifying: {concat_path}")
    print(f"   Audio: {audio_path.name}")
    print()

    entries = parse_concat(concat_path)
    print(f"📋 Found {len(entries)} entries in concat.txt")
    print()

    all_errors: list[str] = []

    # Check files exist
    print("📁 Checking files exist...")
    file_errors = verify_files_exist(entries)
    if file_errors:
        all_errors.extend(file_errors)
        for err in file_errors:
            print(f"   {err}")
    else:
        print("   ✅ All files exist")
    print()

    # Check dimensions (optional)
    if args.check_dims:
        print("📐 Checking image dimensions...")
        dim_errors = verify_dimensions(entries)
        if dim_errors:
            all_errors.extend(dim_errors)
            for err in dim_errors:
                print(f"   {err}")
        else:
            first_dims = get_image_dimensions(entries[0].file_path) if entries else (0, 0)
            print(f"   ✅ All images: {first_dims[0]}x{first_dims[1]}")
        print()

    # Check structure
    print("🏗️  Checking structure...")
    struct_errors = verify_structure(entries)
    if struct_errors:
        for err in struct_errors:
            print(f"   {err}")
    else:
        print("   ✅ Structure OK")
    print()

    # Check duration
    print("⏱️  Checking duration...")
    duration_ok, duration_msgs = verify_duration(entries, audio_path)
    for msg in duration_msgs:
        print(f"   {msg}")
    print()

    # Summary
    print("━" * 50)
    if not all_errors and duration_ok:
        print("✅ concat.txt verification passed")
        return 0
    else:
        print("❌ concat.txt verification FAILED")
        if not duration_ok:
            print("   → Adjust slide durations to match audio + 5s")
        return 1


if __name__ == "__main__":
    sys.exit(main())
