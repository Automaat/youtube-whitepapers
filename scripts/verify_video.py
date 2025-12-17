#!/usr/bin/env python3
"""Verify video has no black frames at start/end and correct duration."""

import subprocess
import sys
import tempfile
from pathlib import Path


def run_cmd(cmd: list[str]) -> str:
    """Run command and return stdout."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_duration(file_path: Path) -> float:
    """Get media duration in seconds."""
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


def extract_frames(video: Path, output_dir: Path, start: bool, count: int = 3) -> list[Path]:
    """Extract frames from start or end of video."""
    frames = []
    for i in range(count):
        frame_path = output_dir / f"{'start' if start else 'end'}_{i:02d}.png"
        timestamp = str(i) if start else str(get_duration(video) - count + i)

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-ss",
                timestamp,
                "-i",
                str(video),
                "-vframes",
                "1",
                str(frame_path),
            ],
            check=True,
        )
        frames.append(frame_path)
    return frames


def get_brightness(image: Path) -> float:
    """Get average brightness of image (0-1 scale)."""
    output = run_cmd(
        ["magick", str(image), "-colorspace", "Gray", "-format", "%[fx:mean]", "info:"]
    )
    return float(output)


def verify_video(video_path: Path, audio_path: Path) -> bool:
    """Verify video duration and no black frames."""
    print(f"🔍 Verifying: {video_path.name}")

    video_duration = get_duration(video_path)
    audio_duration = get_duration(audio_path)
    expected_duration = audio_duration + 5.0

    print(f"   Audio duration: {audio_duration:.2f}s")
    print(f"   Video duration: {video_duration:.2f}s")
    print(f"   Expected: {expected_duration:.2f}s (audio + 5s)")

    duration_ok = abs(video_duration - expected_duration) <= 0.5
    if duration_ok:
        print("   ✅ Duration OK")
    else:
        print(f"   ❌ Duration mismatch: {video_duration - expected_duration:+.2f}s")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        print("   Checking start frames...")
        start_frames = extract_frames(video_path, tmppath, start=True)
        start_ok = True
        for frame in start_frames:
            brightness = get_brightness(frame)
            is_black = brightness < 0.05
            status = "❌ BLACK" if is_black else "✅"
            print(f"      {frame.name}: brightness={brightness:.3f} {status}")
            if is_black:
                start_ok = False

        print("   Checking end frames...")
        end_frames = extract_frames(video_path, tmppath, start=False)
        end_ok = True
        for frame in end_frames:
            brightness = get_brightness(frame)
            is_black = brightness < 0.05
            status = "❌ BLACK" if is_black else "✅"
            print(f"      {frame.name}: brightness={brightness:.3f} {status}")
            if is_black:
                end_ok = False

    all_ok = duration_ok and start_ok and end_ok

    if all_ok:
        print("✅ Video verification passed")
    else:
        print("❌ Video verification FAILED")
        if not duration_ok:
            print("   → Fix concat timings for correct duration")
        if not start_ok:
            print("   → Check thumbnail is correctly set as first slide")
        if not end_ok:
            print("   → Check last-slide.png is correctly set as outro")

    return all_ok


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: verify-video.py <video.mp4> <audio.m4a>")
        print(
            "Example: verify-video.py youtube/output/01-llm-attention.mp4 youtube/pl/audio/01-llm-attention.m4a"
        )
        return 1

    video = Path(sys.argv[1])
    audio = Path(sys.argv[2])

    if not video.exists():
        print(f"❌ Video not found: {video}")
        return 1
    if not audio.exists():
        print(f"❌ Audio not found: {audio}")
        return 1

    success = verify_video(video, audio)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
