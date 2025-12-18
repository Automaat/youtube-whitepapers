#!/usr/bin/env python3
"""Generate video from concat.txt and audio file using ffmpeg."""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
YOUTUBE_DIR = SCRIPT_DIR / "youtube"
ASSETS_DIR = YOUTUBE_DIR / "pl"
OUTPUT_DIR = YOUTUBE_DIR / "output"


def safe_relative(path: Path, base: Path) -> Path:
    """Return relative path if possible, otherwise absolute path."""
    try:
        return path.relative_to(base)
    except ValueError:
        return path


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run command and return result."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def get_duration(file_path: Path) -> float:
    """Get media duration in seconds using ffprobe."""
    result = run_cmd(
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
    return float(result.stdout.strip())


def extract_frame(video: Path, output: Path, timestamp: float) -> None:
    """Extract single frame from video at timestamp."""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-ss",
            str(timestamp),
            "-i",
            str(video),
            "-vframes",
            "1",
            str(output),
        ],
        check=True,
    )


def get_brightness(image: Path) -> float:
    """Get average brightness of image (0-1 scale)."""
    result = run_cmd(
        ["magick", str(image), "-colorspace", "Gray", "-format", "%[fx:mean]", "info:"]
    )
    return float(result.stdout.strip())


def check_black_frames(video: Path, duration: float) -> tuple[bool, bool]:
    """Check for black frames at start and end. Returns (start_ok, end_ok)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        start_ok = True
        for i in range(3):
            frame = tmppath / f"start_{i}.png"
            extract_frame(video, frame, float(i))
            if get_brightness(frame) < 0.05:
                start_ok = False
                break

        end_ok = True
        for i in range(3):
            frame = tmppath / f"end_{i}.png"
            extract_frame(video, frame, duration - 3 + i)
            if get_brightness(frame) < 0.05:
                end_ok = False
                break

    return start_ok, end_ok


def find_episode_files(ep_num: str) -> tuple[Path | None, Path | None]:
    """Find slides directory and audio file for episode number."""
    slides_dir = ASSETS_DIR / "slides"
    audio_dir = ASSETS_DIR / "audio"

    slides_matches = list(slides_dir.glob(f"{ep_num}-*/"))
    audio_matches = list(audio_dir.glob(f"{ep_num}-*.m4a"))

    slides = slides_matches[0] if slides_matches else None
    audio = audio_matches[0] if audio_matches else None

    return slides, audio


def generate_video(
    concat_file: Path, audio_file: Path, output_file: Path
) -> subprocess.CompletedProcess:
    """Run ffmpeg to generate video from concat.txt and audio."""
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-i",
        str(audio_file),
        "-af",
        "apad=pad_dur=5",
        "-c:v",
        "libx264",
        "-vf",
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30",
        "-pix_fmt",
        "yuv420p",
        "-vsync",
        "cfr",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(output_file),
    ]
    return run_cmd(cmd, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate video from concat.txt and audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 28
  %(prog)s 28 --concat path/to/concat.txt
  %(prog)s 28 --skip-verify
        """,
    )
    parser.add_argument("episode", help="Episode number (e.g., 28)")
    parser.add_argument("--concat", type=Path, help="Custom concat.txt path")
    parser.add_argument(
        "--skip-verify", action="store_true", help="Skip verification step"
    )
    args = parser.parse_args()

    ep_num = args.episode

    # Find episode files
    slides_dir, audio_file = find_episode_files(ep_num)

    if not slides_dir:
        print(f"❌ No slides directory found for episode {ep_num}")
        print(f"   Expected: youtube/pl/slides/{ep_num}-*/")
        return 1

    if not audio_file:
        print(f"❌ No audio file found for episode {ep_num}")
        print(f"   Expected: youtube/pl/audio/{ep_num}-*.m4a")
        return 1

    # Determine concat file path
    concat_file = args.concat if args.concat else slides_dir / "concat.txt"

    if not concat_file.exists():
        print(f"❌ concat.txt not found: {concat_file}")
        return 1

    ep_name = slides_dir.name
    output_file = OUTPUT_DIR / f"{ep_name}.mp4"

    print(f"🎬 Generating video: {ep_name}")
    print("━" * 50)
    print(f"   📁 Slides:  {safe_relative(slides_dir, SCRIPT_DIR)}")
    print(f"   🎵 Audio:   {safe_relative(audio_file, SCRIPT_DIR)}")
    print(f"   📋 Concat:  {safe_relative(concat_file, SCRIPT_DIR)}")
    print(f"   📺 Output:  {safe_relative(output_file, SCRIPT_DIR)}")

    # Get audio duration for verification
    audio_duration = get_duration(audio_file)
    expected_duration = audio_duration + 5.0
    print(f"   ⏱️  Audio duration: {audio_duration:.2f}s")
    print(f"   ⏱️  Expected video: {expected_duration:.2f}s")
    print()

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate video
    print("🔄 Running ffmpeg...")
    result = generate_video(concat_file, audio_file, output_file)

    if result.returncode != 0:
        print("❌ ffmpeg failed:")
        print(result.stderr)
        return 1

    print("   ✅ Video generated")

    if not output_file.exists():
        print("❌ Output file not created")
        return 1

    # Verification
    if args.skip_verify:
        print("⏭️  Skipping verification")
        print()
        print("━" * 50)
        print(f"✅ Video created: {safe_relative(output_file, SCRIPT_DIR)}")
        return 0

    print()
    print("🔍 Verifying output...")

    video_duration = get_duration(output_file)
    duration_diff = video_duration - expected_duration
    duration_ok = abs(duration_diff) <= 0.5

    print(f"   Video duration: {video_duration:.2f}s")
    if duration_ok:
        print("   ✅ Duration OK")
    else:
        print(f"   ❌ Duration mismatch: {duration_diff:+.2f}s")

    print("   Checking for black frames...")
    start_ok, end_ok = check_black_frames(output_file, video_duration)

    if start_ok:
        print("   ✅ Start frames OK")
    else:
        print("   ❌ Black frames detected at start")

    if end_ok:
        print("   ✅ End frames OK")
    else:
        print("   ❌ Black frames detected at end")

    all_ok = duration_ok and start_ok and end_ok

    print()
    print("━" * 50)
    if all_ok:
        print(f"✅ Video created and verified: {safe_relative(output_file, SCRIPT_DIR)}")
        return 0
    else:
        print(f"⚠️  Video created but verification failed: {safe_relative(output_file, SCRIPT_DIR)}")
        if not duration_ok:
            print("   → Check concat.txt timings")
        if not start_ok:
            print("   → Check thumbnail is first in concat.txt")
        if not end_ok:
            print("   → Check last-slide.png is at the end")
        return 1


if __name__ == "__main__":
    sys.exit(main())
