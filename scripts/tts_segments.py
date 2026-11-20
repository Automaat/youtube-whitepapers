#!/usr/bin/env python3
"""Synthesize every script segment with ElevenLabs, with character timestamps.

One request per segment, voice chosen by speaker (episode.yaml `voices`). Results
are cached in build/tts/ by a hash of text, voice, model and settings, so only
changed segments cost credits on re-runs.

Usage:
    python scripts/tts_segments.py 73 --api-key-file PATH
    python scripts/tts_segments.py 73 --only s001,s002 --api-key-file PATH
    python scripts/tts_segments.py 73 --dry-run      # count characters, no requests

The key can also come from ELEVENLABS_API_KEY.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from episode_pipeline import build_dir, find_episode_dir, load_episode, load_yaml

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128"
CUE_RE = re.compile(r"\s*\[\[cue:([a-z0-9_]+)\]\]\s*")
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
}


def strip_cues(text: str) -> tuple[str, dict[str, int]]:
    """Remove [[cue:x]] markers; return clean text and cue → char offset in it."""
    text = text.strip()
    cues: dict[str, int] = {}
    clean = ""
    pos = 0
    for m in CUE_RE.finditer(text):
        clean += text[pos : m.start()]
        between_words = bool(clean) and m.end() < len(text)
        if between_words:
            clean += " "
        cues[m.group(1)] = len(clean)
        pos = m.end()
    clean += text[pos:]
    return clean.rstrip(), cues


def cache_key(text: str, voice: str, model: str) -> str:
    """Stable hash of everything that changes the audio."""
    payload = json.dumps([text, voice, model, VOICE_SETTINGS], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def synthesize(api_key: str, voice: str, model: str, text: str, context: dict[str, str]) -> dict:
    """Call ElevenLabs with-timestamps; return the JSON response."""
    body = {
        "text": text,
        "model_id": model,
        "language_code": "pl",
        "voice_settings": VOICE_SETTINGS,
        **context,
    }
    req = urllib.request.Request(
        API.format(voice=voice),
        data=json.dumps(body).encode(),
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:500]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"ElevenLabs {e.code}: {detail}") from e
    raise RuntimeError("unreachable")


def read_api_key(path: str | None) -> str | None:
    if path:
        return Path(path).read_text(encoding="utf-8").strip()
    return os.environ.get("ELEVENLABS_API_KEY")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode")
    parser.add_argument("--api-key-file")
    parser.add_argument("--only", help="Comma-separated segment ids to (re)synthesize")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    episode_dir = find_episode_dir(args.episode)
    if episode_dir is None:
        print(f"❌ No episode directory for {args.episode}")
        return 1
    episode = load_episode(episode_dir)
    segments = load_yaml(episode_dir / "script.yaml")["segments"]
    model = episode.get("tts_model", "eleven_v4")
    only = set(args.only.split(",")) if args.only else None
    tts_dir = build_dir(episode_dir) / "tts"
    tts_dir.mkdir(exist_ok=True)

    total = sum(len(strip_cues(s["text"])[0]) for s in segments)
    print(f"📋 {len(segments)} segments, {total} characters, model {model}")
    if args.dry_run:
        return 0
    api_key = read_api_key(args.api_key_file)
    if not api_key:
        print("❌ No API key (use --api-key-file or ELEVENLABS_API_KEY)")
        return 1

    manifest = []
    missing: list[str] = []
    spent = 0
    for i, seg in enumerate(segments):
        text, cues = strip_cues(seg["text"])
        voice = episode["voices"][seg["speaker"]]
        key = cache_key(text, voice, model)
        mp3 = tts_dir / f"{seg['id']}-{key}.mp3"
        align = mp3.with_suffix(".json")
        if not (mp3.exists() and align.exists()) and (only is None or seg["id"] in only):
            context = {}
            if i > 0:
                context["previous_text"] = strip_cues(segments[i - 1]["text"])[0][-300:]
            if i + 1 < len(segments):
                context["next_text"] = strip_cues(segments[i + 1]["text"])[0][:300]
            print(f"🔄 {seg['id']} ({seg['speaker']}, {len(text)} chars)")
            data = synthesize(api_key, voice, model, text, context)
            mp3.write_bytes(base64.b64decode(data["audio_base64"]))
            align.write_text(json.dumps(data["alignment"], ensure_ascii=False), encoding="utf-8")
            spent += len(text)
        if not mp3.exists():
            missing.append(seg["id"])
            continue
        manifest.append(
            {
                "id": seg["id"],
                "speaker": seg["speaker"],
                "scene": seg["scene"],
                "text": text,
                "cues": cues,
                "audio": mp3.name,
                "alignment": align.name,
            }
        )
    if missing:
        print(f"❌ Missing audio (excluded by --only): {', '.join(missing)}")
        return 1
    (tts_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"✅ {len(manifest)} segments ready, {spent} characters synthesized now")
    return 0


if __name__ == "__main__":
    sys.exit(main())
