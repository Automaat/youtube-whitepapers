"""Build the narration track, timeline.json and captions from synthesized segments.

Reads build/tts/manifest.json, places segments one after another with short
pauses, converts cue character offsets to seconds using the ElevenLabs alignment,
and writes everything Remotion needs into build/public/:

- narration.wav   loudness-normalized narration (-14 LUFS)
- timeline.json   scenes, cues, segments, chapters, thumbnail (Episode props)

It also writes build/captions.srt for YouTube CC and a copy of timeline.json next
to the episode files.
"""

import json
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

from odczyt.episode import Episode

SAMPLE_RATE = 44100
PAUSE_SAME_SPEAKER = 0.35
PAUSE_SPEAKER_CHANGE = 0.55
PAUSE_SCENE_CHANGE = 0.8
PAUSE_CHAPTER_CHANGE = 1.2
TAIL_SECONDS = 0.6
INTRO_SECONDS = 5.0
OUTRO_SECONDS = 5.0
FPS = 30
CAPTION_MAX_CHARS = 84


def pause_before(prev: dict | None, seg: dict, scene_chapter: dict[str, str | None]) -> float:
    """Silence inserted before a segment."""
    if prev is None:
        return 0.0
    if scene_chapter.get(prev["scene"]) != scene_chapter.get(seg["scene"]):
        return PAUSE_CHAPTER_CHANGE
    if prev["scene"] != seg["scene"]:
        return PAUSE_SCENE_CHANGE
    if prev["speaker"] != seg["speaker"]:
        return PAUSE_SPEAKER_CHANGE
    return PAUSE_SAME_SPEAKER


def cue_seconds(offset: int, alignment: dict, text: str, duration: float) -> float:
    """Seconds into a segment where the first non-space character at or after `offset` starts.

    Falls back to a proportional estimate when the alignment does not map 1:1 to the text.
    """
    chars = alignment.get("characters", [])
    starts = alignment.get("character_start_times_seconds", [])
    if len(chars) == len(text) and starts:
        idx = min(offset, len(starts) - 1)
        while idx < len(chars) - 1 and chars[idx].isspace():
            idx += 1
        return float(starts[idx])
    return duration * offset / max(1, len(text))


def word_times(alignment: dict) -> list[tuple[str, float, float]]:
    """Group character alignment into (word, start, end)."""
    words: list[tuple[str, float, float]] = []
    cur, start, end = "", 0.0, 0.0
    for ch, s, e in zip(
        alignment.get("characters", []),
        alignment.get("character_start_times_seconds", []),
        alignment.get("character_end_times_seconds", []),
        strict=False,
    ):
        if ch.isspace():
            if cur:
                words.append((cur, start, end))
            cur = ""
            continue
        if not cur:
            start = s
        cur += ch
        end = e
    if cur:
        words.append((cur, start, end))
    return words


def srt_time(t: float) -> str:
    """Format seconds as an SRT timestamp."""
    ms = round(t * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def captions(segments: list[dict]) -> str:
    """SRT text: each segment split into chunks of at most CAPTION_MAX_CHARS."""
    blocks: list[str] = []
    for seg in segments:
        chunk: list[tuple[str, float, float]] = []
        for w in [*seg["words"], None]:
            text = " ".join(x[0] for x in chunk)
            if w is None or (chunk and len(text) + 1 + len(w[0]) > CAPTION_MAX_CHARS):
                if chunk:
                    start = seg["start"] + chunk[0][1]
                    end = seg["start"] + chunk[-1][2]
                    blocks.append(
                        f"{len(blocks) + 1}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n"
                    )
                chunk = []
            if w is not None:
                chunk.append(w)
    return "\n".join(blocks)


def group_scenes(
    placed: list[dict], scene_chapter: dict[str, str | None], audio_seconds: float
) -> list[dict]:
    """Merge consecutive segments of one scene; scenes cover the audio without gaps."""
    scenes: list[dict] = []
    for seg in placed:
        if scenes and scenes[-1]["id"] == seg["scene"]:
            scenes[-1]["cues"].update(seg["cue_times"])
            continue
        if any(s["id"] == seg["scene"] for s in scenes):
            raise ValueError(f"Scene {seg['scene']} is not contiguous (segment {seg['id']})")
        scenes.append(
            {
                "id": seg["scene"],
                "chapter": scene_chapter.get(seg["scene"]),
                "start": seg["start"],
                "cues": dict(seg["cue_times"]),
            }
        )
    for i, scene in enumerate(scenes):
        if i == 0:
            scene["start"] = 0.0
        scene["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else audio_seconds
    return scenes


def decode(mp3: Path, wav: Path) -> None:
    """Decode an MP3 to mono 16-bit WAV at SAMPLE_RATE."""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(mp3),
            "-ac",
            "1",
            "-ar",
            str(SAMPLE_RATE),
            "-sample_fmt",
            "s16",
            str(wav),
        ],
        check=True,
    )


def place_segments(
    manifest: list[dict], tts_dir: Path, scene_chapter: dict[str, str | None], out_wav: Path
) -> tuple[list[dict], float]:
    """Concatenate segment audio with pauses into a normalized WAV; return placed segments and end time."""
    placed: list[dict] = []
    cursor = 0.0
    pcm = bytearray()
    with tempfile.TemporaryDirectory() as tmp:
        prev = None
        for seg in manifest:
            gap = pause_before(prev, seg, scene_chapter)
            pcm += b"\x00\x00" * round(gap * SAMPLE_RATE)
            cursor += gap
            wav = Path(tmp) / f"{seg['id']}.wav"
            decode(tts_dir / seg["audio"], wav)
            with wave.open(str(wav)) as w:
                data = w.readframes(w.getnframes())
            duration = len(data) / 2 / SAMPLE_RATE
            alignment = json.loads((tts_dir / seg["alignment"]).read_text(encoding="utf-8"))
            placed.append(
                {
                    **seg,
                    "start": round(cursor, 3),
                    "end": round(cursor + duration, 3),
                    "cue_times": {
                        k: round(cursor + cue_seconds(v, alignment, seg["text"], duration), 3)
                        for k, v in seg["cues"].items()
                    },
                    "words": word_times(alignment),
                }
            )
            pcm += data
            cursor += duration
            prev = seg
        pcm += b"\x00\x00" * round(TAIL_SECONDS * SAMPLE_RATE)
        raw = Path(tmp) / "raw.wav"
        with wave.open(str(raw), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SAMPLE_RATE)
            w.writeframes(bytes(pcm))
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(raw),
                "-af",
                "loudnorm=I=-14:TP=-1.5:LRA=11",
                "-ar",
                str(SAMPLE_RATE),
                "-ac",
                "2",
                str(out_wav),
            ],
            check=True,
        )
    return placed, round(cursor + TAIL_SECONDS, 3)


def missing_cues(storyboard: dict, scenes: list[dict]) -> list[str]:
    """Storyboard cues that never appear in the script."""
    by_id = {s["id"]: s["cues"] for s in scenes}
    return [
        f"{s['id']}:{c['name']}"
        for s in storyboard["scenes"]
        for c in s.get("cues", [])
        if c["name"] not in by_id.get(s["id"], {})
    ]


def build_timeline(ep: Episode) -> dict:
    """Write narration.wav, timeline.json and captions.srt; return the timeline."""
    storyboard = ep.storyboard()
    tts_dir = ep.build / "tts"
    manifest = json.loads((tts_dir / "manifest.json").read_text(encoding="utf-8"))
    public = ep.public

    scene_chapter = {s["id"]: s.get("chapter") for s in storyboard["scenes"]}
    placed, audio_seconds = place_segments(
        manifest, tts_dir, scene_chapter, public / "narration.wav"
    )
    scenes = group_scenes(placed, scene_chapter, audio_seconds)
    missing = missing_cues(storyboard, scenes)
    if missing:
        print(f"⚠️  Storyboard cues missing in script: {', '.join(missing)}")

    image = None
    override = ep.config.get("thumbnail_image")
    if override:
        shutil.copy(ep.repo / override, public / "thumbnail.png")
        image = "thumbnail.png"

    timeline = {
        "slug": ep.slug,
        "number": ep.number,
        "title": ep.config["title"],
        "subtitle": ep.config["subtitle"],
        "authors": ep.config["authors"],
        "theme": ep.config.get("theme", "dark"),
        "fps": FPS,
        "audio": "narration.wav",
        "audioSeconds": audio_seconds,
        "introSeconds": INTRO_SECONDS,
        "outroSeconds": OUTRO_SECONDS,
        "thumbnail": image,
        "thumbnailArt": storyboard.get("thumbnail"),
        "chapters": [{"id": c["id"], "title": c["title"]} for c in storyboard["chapters"]],
        "scenes": scenes,
        "segments": [{k: s[k] for k in ("id", "speaker", "scene", "start", "end")} for s in placed],
    }
    text = json.dumps(timeline, ensure_ascii=False, indent=2)
    (public / "timeline.json").write_text(text, encoding="utf-8")
    ep.file("timeline.json").write_text(text, encoding="utf-8")
    (ep.build / "captions.srt").write_text(captions(placed), encoding="utf-8")
    print(f"✅ narration {audio_seconds:.1f}s, {len(scenes)} scenes, {len(placed)} segments")
    return timeline
