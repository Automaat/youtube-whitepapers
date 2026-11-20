"""Synthesize every script segment with ElevenLabs, with character timestamps.

One request per segment, voice chosen by speaker (`voices` in the episode config).
Results are cached in build/tts/ by a hash of text, voice, model and settings, so
only changed segments cost credits on re-runs.
"""

import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

from odczyt.episode import Episode

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128"
CUE_RE = re.compile(r"\s*\[\[cue:([a-z0-9_]+)\]\]\s*")
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
}
CONTEXT_CHARS = 300
SUBSCRIPTION_API = "https://api.elevenlabs.io/v1/user/subscription"


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


def remaining_credits(api_key: str) -> int | None:
    """Credits left in the current billing period, or None if the key cannot read it."""
    req = urllib.request.Request(SUBSCRIPTION_API, headers={"xi-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            sub = json.load(resp)
    except (urllib.error.URLError, TimeoutError):
        return None
    return int(sub["character_limit"]) - int(sub["character_count"])


def resolve_api_key(key_file: str | None, bitwarden_item: str | None) -> str | None:
    """API key from a file, ELEVENLABS_API_KEY, or an unlocked Bitwarden vault (BW_SESSION)."""
    if key_file:
        return Path(key_file).expanduser().read_text(encoding="utf-8").strip()
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    if bitwarden_item and os.environ.get("BW_SESSION") and shutil.which("bw"):
        proc = subprocess.run(
            ["bw", "get", "password", bitwarden_item], capture_output=True, text=True
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    return None


def segment_plan(ep: Episode) -> list[dict]:
    """Clean text, cues, voice and cache file names of every segment."""
    model = ep.config.get("tts_model", "eleven_v4")
    tts_dir = ep.build / "tts"
    tts_dir.mkdir(exist_ok=True)
    plan = []
    for seg in ep.script()["segments"]:
        text, cues = strip_cues(seg["text"])
        voice = ep.config["voices"][seg["speaker"]]
        mp3 = tts_dir / f"{seg['id']}-{cache_key(text, voice, model)}.mp3"
        plan.append({**seg, "clean": text, "cues": cues, "voice": voice, "mp3": mp3})
    return plan


def missing_characters(ep: Episode) -> int:
    """Characters that still need synthesis (not in the cache)."""
    return sum(
        len(p["clean"])
        for p in segment_plan(ep)
        if not (p["mp3"].exists() and p["mp3"].with_suffix(".json").exists())
    )


def synthesize_episode(ep: Episode, api_key: str | None, only: set[str] | None = None) -> int:
    """Synthesize uncached segments and write build/tts/manifest.json; return chars spent."""
    model = ep.config.get("tts_model", "eleven_v4")
    plan = segment_plan(ep)
    manifest = []
    missing: list[str] = []
    spent = 0
    for i, seg in enumerate(plan):
        mp3: Path = seg["mp3"]
        align = mp3.with_suffix(".json")
        cached = mp3.exists() and align.exists()
        if not cached and (only is None or seg["id"] in only):
            if not api_key:
                raise RuntimeError(
                    "ElevenLabs key needed: --api-key-file, ELEVENLABS_API_KEY or "
                    "BW_SESSION (bw unlock) for the Bitwarden item"
                )
            context = {}
            if i > 0:
                context["previous_text"] = plan[i - 1]["clean"][-CONTEXT_CHARS:]
            if i + 1 < len(plan):
                context["next_text"] = plan[i + 1]["clean"][:CONTEXT_CHARS]
            print(f"🔄 {seg['id']} ({seg['speaker']}, {len(seg['clean'])} chars)", flush=True)
            data = synthesize(api_key, seg["voice"], model, seg["clean"], context)
            mp3.write_bytes(base64.b64decode(data["audio_base64"]))
            align.write_text(json.dumps(data["alignment"], ensure_ascii=False), encoding="utf-8")
            spent += len(seg["clean"])
        if not mp3.exists():
            missing.append(seg["id"])
            continue
        manifest.append(
            {
                "id": seg["id"],
                "speaker": seg["speaker"],
                "scene": seg["scene"],
                "text": seg["clean"],
                "cues": seg["cues"],
                "audio": mp3.name,
                "alignment": align.name,
            }
        )
    if missing:
        raise RuntimeError(f"Missing audio (excluded by --only): {', '.join(missing)}")
    (ep.build / "tts" / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return spent
