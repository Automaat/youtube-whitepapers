"""Recover the hand-made dog thumbnail of an episode that was produced before.

Old thumbnails were committed to youtube/thumbnails/ and later removed by the
archive script, so the last committed version is the first source. Uploaded
episodes also have their thumbnail on YouTube.
"""

import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

YOUTUBE_ID_RE = re.compile(r"(?:v=|youtu\.be/)([\w-]{11})")
YOUTUBE_THUMB = "https://i.ytimg.com/vi/{id}/maxresdefault.jpg"


def from_git(repo: Path, image: Path) -> bool:
    """Write the last committed (added or modified) version of `image`; True on success."""
    rel = str(image.relative_to(repo))
    log = subprocess.run(
        ["git", "log", "--all", "-1", "--format=%H", "--diff-filter=AM", "--", rel],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    commit = log.stdout.strip()
    if log.returncode != 0 or not commit:
        return False
    blob = subprocess.run(
        ["git", "show", f"{commit}:{rel}"], cwd=repo, capture_output=True, check=False
    )
    if blob.returncode != 0 or not blob.stdout:
        return False
    image.parent.mkdir(parents=True, exist_ok=True)
    image.write_bytes(blob.stdout)
    return True


def youtube_url(status_file: Path, number: int) -> str | None:
    if not status_file.exists():
        return None
    papers = json.loads(status_file.read_text(encoding="utf-8")).get("papers", [])
    return next((p.get("youtube_url") for p in papers if int(p["episode"]) == number), None)


def from_youtube(url: str, image: Path) -> bool:
    """Save the uploaded video's max-resolution thumbnail as PNG; True on success."""
    match = YOUTUBE_ID_RE.search(url)
    if match is None:
        return False
    jpg = image.with_suffix(".jpg")
    try:
        with urllib.request.urlopen(YOUTUBE_THUMB.format(id=match.group(1)), timeout=30) as resp:
            jpg.write_bytes(resp.read())
    except (urllib.error.URLError, TimeoutError):
        return False
    converted = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(jpg), str(image)], check=False
    )
    jpg.unlink(missing_ok=True)
    return converted.returncode == 0 and image.exists()
