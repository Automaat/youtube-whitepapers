#!/usr/bin/env python3
"""Parallel transcription script for NotebookLM podcasts using Whisper."""

import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from status_utils import update_episode_status

SCRIPT_DIR = Path(__file__).parent.parent
AUDIO_DIR = SCRIPT_DIR / "youtube/pl/audio"
OUTPUT_DIR = SCRIPT_DIR / "youtube/pl/transcripts"
MODEL = "small"
LANGUAGE = "pl"
AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav"}


def transcribe_file(audio_path: Path) -> tuple[Path, bool, str]:
    """Transcribe single audio file with whisper.

    Returns tuple of (path, success, message).
    """
    output_file = OUTPUT_DIR / f"{audio_path.stem}.json"

    if output_file.exists():
        return audio_path, True, "skipped (exists)"

    try:
        subprocess.run(
            [
                "whisper",
                str(audio_path),
                "--model",
                MODEL,
                "--language",
                LANGUAGE,
                "--output_format",
                "json",
                "--output_dir",
                str(OUTPUT_DIR),
            ],
            check=True,
            capture_output=True,
        )
        return audio_path, True, "done"
    except subprocess.CalledProcessError as e:
        return audio_path, False, f"failed: {e.stderr.decode()[:100]}"


def find_audio_files() -> list[Path]:
    """Find all audio files in audio directory."""
    files = []
    for ext in AUDIO_EXTENSIONS:
        files.extend(AUDIO_DIR.glob(f"*{ext}"))
    return sorted(files)


def main() -> int:
    """Run parallel transcription."""
    parallel_jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("🎙️ Transcription Script")
    print("=" * 24)
    print(f"Audio dir: {AUDIO_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Model: {MODEL}")
    print(f"Language: {LANGUAGE}")
    print(f"Parallel jobs: {parallel_jobs}")
    print()

    audio_files = find_audio_files()
    print(f"Found {len(audio_files)} audio files")
    print()

    if not audio_files:
        print("No audio files to process")
        return 0

    failed = []

    with ThreadPoolExecutor(max_workers=parallel_jobs) as executor:
        futures = {executor.submit(transcribe_file, f): f for f in audio_files}

        for future in as_completed(futures):
            path, success, msg = future.result()
            name = path.stem

            if msg == "skipped (exists)":
                print(f"⏭️  Skip: {name}")
            elif success:
                print(f"✅ Done: {name}")
                match = re.match(r"^(\d+)-", name)
                if match:
                    update_episode_status(match.group(1), "transcript", True)
            else:
                print(f"❌ Failed: {name} - {msg}")
                failed.append(path)

    print()
    if failed:
        print(f"⚠️  {len(failed)} transcription(s) failed")
        return 1

    print("🎉 All transcriptions complete!")
    print(f"Output files in: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
