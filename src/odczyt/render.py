"""Render review stills, the thumbnail and the final video with Remotion, and verify it.

Stills are taken 0.6 s after every cue and just before every scene ends, so the
stills review sees each state of each diagram.
"""

import json
import re
import subprocess
from pathlib import Path

from odczyt.episode import Episode
from odczyt.paths import REMOTION_DIR

CUE_OFFSET_SECONDS = 0.6
END_OFFSET_SECONDS = 0.3
THUMBNAIL_SIZE = "1280:720"
BLACK_THRESHOLD = 0.05
DURATION_TOLERANCE = 0.5
YAVG_RE = re.compile(r"lavfi\.signalstats\.YAVG=([\d.]+)")


def still_frames(timeline: dict, scenes: set[str] | None = None) -> list[tuple[int, str]]:
    """(frame, name) pairs: after each cue and at each scene's end."""
    fps = timeline["fps"]
    frames: list[tuple[int, str]] = []
    if scenes is None:
        frames.append((round(2 * fps), "00-intro-thumbnail"))
    for i, scene in enumerate(timeline["scenes"]):
        if scenes is not None and scene["id"] not in scenes:
            continue
        start = max(scene["start"], timeline["introSeconds"] if i == 0 else 0)
        last = scene["end"] - END_OFFSET_SECONDS
        for name, t in sorted(scene["cues"].items(), key=lambda kv: kv[1]):
            at = min(max(t + CUE_OFFSET_SECONDS, start), last)
            frames.append((round(at * fps), f"{i + 1:02d}-{scene['id']}--{name}"))
        frames.append((round(last * fps), f"{i + 1:02d}-{scene['id']}--end"))
    if scenes is None:
        frames.append((round((timeline["audioSeconds"] + 3) * fps), "99-outro"))
    return frames


def load_timeline(ep: Episode) -> dict:
    path = ep.public / "timeline.json"
    if not path.exists():
        raise FileNotFoundError("No timeline; run the timeline stage first")
    return json.loads(path.read_text(encoding="utf-8"))


def _node(*args: str) -> None:
    subprocess.run(["node", *args], cwd=REMOTION_DIR, check=True)


def render_stills(ep: Episode, scenes: set[str] | None = None) -> list[Path]:
    """Render review stills into build/stills/; a full run replaces old stills."""
    timeline = load_timeline(ep)
    out = ep.build / "stills"
    if scenes is None and out.exists():
        for old in out.glob("*.png"):
            old.unlink()
    frames = still_frames(timeline, scenes)
    print(f"🔄 rendering {len(frames)} stills → {ep.rel(out)}", flush=True)
    timeline_path = ep.public / "timeline.json"
    specs = [f"{f}:{name}" for f, name in frames]
    _node("scripts/stills.mjs", "Episode", str(timeline_path), str(ep.public), str(out), *specs)
    return [out / f"{name}.png" for _, name in frames]


def render_thumbnail(ep: Episode) -> Path:
    """Render the Thumbnail composition and scale it to YouTube's 1280x720."""
    full = ep.build / "thumbnail-full.png"
    _node(
        "scripts/stills.mjs",
        "Thumbnail",
        str(ep.public / "timeline.json"),
        str(ep.public),
        str(ep.build),
        "0:thumbnail-full",
    )
    out = ep.build / "thumbnail.png"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(full),
            "-vf",
            f"scale={THUMBNAIL_SIZE}",
            str(out),
        ],
        check=True,
    )
    return out


def render_video(ep: Episode) -> Path:
    """Render build/{slug}.mp4."""
    video = ep.build / f"{ep.slug}.mp4"
    print(f"🔄 rendering {ep.rel(video)}", flush=True)
    _node("scripts/render.mjs", str(ep.public / "timeline.json"), str(ep.public), str(video))
    return video


def media_duration(path: Path) -> float:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(out.stdout.strip())


def frame_brightness(video: Path, at: float) -> float:
    """Mean luma (0 to 1) of the frame at `at` seconds, from ffmpeg signalstats."""
    out = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            f"{at:.3f}",
            "-i",
            str(video),
            "-vframes",
            "1",
            "-vf",
            "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    match = YAVG_RE.search(out.stdout + out.stderr)
    if match is None:
        raise RuntimeError(f"No signalstats output for {video} at {at}s")
    return max(0.0, (float(match.group(1)) - 16) / 219)


def verify_video(video: Path, audio: Path, outro_seconds: float) -> list[str]:
    """Problems with the rendered video: duration and black frames at start and end."""
    problems = []
    duration = media_duration(video)
    expected = media_duration(audio) + outro_seconds
    if abs(duration - expected) > DURATION_TOLERANCE:
        problems.append(f"duration {duration:.2f}s, expected {expected:.2f}s")
    for at in (0.5, 1.5, 2.5, duration - 2.5, duration - 1.5, duration - 0.5):
        brightness = frame_brightness(video, at)
        if brightness < BLACK_THRESHOLD:
            problems.append(f"black frame at {at:.1f}s (brightness {brightness:.3f})")
    return problems
