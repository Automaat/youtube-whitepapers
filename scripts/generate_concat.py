#!/usr/bin/env python3
"""Generate concat.txt with proper intro/outro template.

Usage:
    python scripts/generate_concat.py 55 --durations slide-01:180,slide-02:150,slide-03:120
    python scripts/generate_concat.py 55 --json timings.json

Automatically adds:
- 5s thumbnail intro (with duplicate to avoid ffmpeg drop)
- 5s silent last-slide outro
"""

import argparse
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
SLIDES_BASE = SCRIPT_DIR / "youtube" / "pl" / "slides"


def generate_concat(episode: str, slide_durations: list[tuple[str, float]]) -> str:
    """Generate concat.txt content with proper template.

    Args:
        episode: Episode name (e.g., "55-olmo")
        slide_durations: List of (slide_name, duration) tuples

    Returns:
        Complete concat.txt content
    """
    slides_dir = SLIDES_BASE / episode

    lines = []

    # Template: 5s thumbnail intro (duplicate first entry to avoid ffmpeg drop)
    thumbnail_path = slides_dir / "thumbnail.png"
    lines.append(f"file '{thumbnail_path}'")
    lines.append("duration 5")
    lines.append(f"file '{thumbnail_path}'")
    lines.append("duration 0")

    # Content slides
    for slide_name, duration in slide_durations:
        slide_path = slides_dir / f"{slide_name}.png"
        lines.append(f"file '{slide_path}'")
        lines.append(f"duration {duration}")

    # Template: 5s silent outro
    last_slide_path = slides_dir / "last-slide.png"
    lines.append(f"file '{last_slide_path}'")
    lines.append("duration 5")
    lines.append(f"file '{last_slide_path}'")

    return "\n".join(lines) + "\n"


def parse_durations_string(durations_str: str) -> list[tuple[str, float]]:
    """Parse durations from command line string.

    Format: slide-01:180,slide-02:150,slide-03:120
    """
    result = []
    for item in durations_str.split(","):
        slide_name, duration = item.strip().split(":")
        result.append((slide_name, float(duration)))
    return result


def parse_durations_json(json_path: Path) -> list[tuple[str, float]]:
    """Parse durations from JSON file.

    Format: [{"slide": "slide-01", "duration": 180}, ...]
    """
    data = json.loads(json_path.read_text())
    return [(item["slide"], item["duration"]) for item in data]


def main():
    parser = argparse.ArgumentParser(description="Generate concat.txt with template")
    parser.add_argument("episode", help="Episode number (e.g., 55)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--durations", help="Comma-separated slide:duration pairs")
    group.add_argument("--json", type=Path, help="JSON file with slide timings")

    parser.add_argument("--output", type=Path, help="Output path (default: auto)")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")

    args = parser.parse_args()

    # Find episode name
    audio_dir = SCRIPT_DIR / "youtube" / "pl" / "audio"
    matches = list(audio_dir.glob(f"{args.episode}-*.m4a"))
    if not matches:
        print(f"❌ No audio file found for episode {args.episode}")
        return 1

    episode_name = matches[0].stem
    print(f"📋 Generating concat.txt for: {episode_name}")

    # Parse durations
    if args.durations:
        slide_durations = parse_durations_string(args.durations)
    else:
        slide_durations = parse_durations_json(args.json)

    print(f"   Slides: {len(slide_durations)}")

    # Generate concat content
    concat_content = generate_concat(episode_name, slide_durations)

    # Output
    if args.dry_run:
        print("\n" + concat_content)
        return 0

    output_path = args.output or (SLIDES_BASE / episode_name / "concat.txt")
    output_path.write_text(concat_content)
    print(f"✅ Written to: {output_path}")

    # Show summary
    total_duration = sum(d for _, d in slide_durations) + 10  # +10 for intro/outro
    print("\n📊 Summary:")
    print("   Thumbnail intro: 5s")
    for slide, duration in slide_durations:
        print(f"   {slide}: {duration}s")
    print("   Silent outro: 5s")
    print(f"   Total concat: {total_duration}s")

    return 0


if __name__ == "__main__":
    exit(main())
