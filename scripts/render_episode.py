#!/usr/bin/env python3
"""Render review stills or the final video of a diagram-first episode with Remotion.

Stills are taken 0.6 s after every cue and just before every scene ends, so the
stills review sees each state of each diagram.

Usage:
    python scripts/render_episode.py stills 73
    python scripts/render_episode.py stills 73 --scenes hook,election
    python scripts/render_episode.py render 73     # build/{slug}.mp4 + verification
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from episode_pipeline import REMOTION_DIR, build_dir, find_episode_dir
from verify_video import verify_video

CUE_OFFSET_SECONDS = 0.6
END_OFFSET_SECONDS = 0.3


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=["stills", "render"])
    parser.add_argument("episode")
    parser.add_argument("--scenes", help="Comma-separated scene ids (stills only)")
    args = parser.parse_args()

    episode_dir = find_episode_dir(args.episode)
    if episode_dir is None:
        print(f"❌ No episode directory for {args.episode}")
        return 1
    build = build_dir(episode_dir)
    public = build / "public"
    timeline_path = public / "timeline.json"
    if not timeline_path.exists():
        print("❌ No timeline; run build_timeline.py first")
        return 1
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))

    if args.mode == "stills":
        scenes = set(args.scenes.split(",")) if args.scenes else None
        out = build / "stills"
        if scenes is None:
            for old in out.glob("*.png"):
                old.unlink()
        specs = [f"{f}:{name}" for f, name in still_frames(timeline, scenes)]
        print(f"🔄 rendering {len(specs)} stills → {out}")
        cmd = ["node", "scripts/stills.mjs", str(timeline_path), str(public), str(out), *specs]
        return subprocess.run(cmd, cwd=REMOTION_DIR, check=False).returncode

    video = build / f"{timeline['slug']}.mp4"
    print(f"🔄 rendering {video}")
    cmd = ["node", "scripts/render.mjs", str(timeline_path), str(public), str(video)]
    if subprocess.run(cmd, cwd=REMOTION_DIR, check=False).returncode != 0:
        print("❌ Render failed")
        return 1
    return 0 if verify_video(video, Path(public / "narration.wav")) else 1


if __name__ == "__main__":
    sys.exit(main())
