"""Tests for build_timeline.py."""

import pytest

from scripts.build_timeline import (
    PAUSE_CHAPTER_CHANGE,
    PAUSE_SAME_SPEAKER,
    PAUSE_SCENE_CHANGE,
    PAUSE_SPEAKER_CHANGE,
    captions,
    cue_seconds,
    group_scenes,
    pause_before,
    srt_time,
    word_times,
)

CHAPTERS = {"intro": None, "hook": "c1", "glossary": "c1", "election": "c2"}


def align(text: str, step: float = 0.1) -> dict:
    return {
        "characters": list(text),
        "character_start_times_seconds": [i * step for i in range(len(text))],
        "character_end_times_seconds": [(i + 1) * step for i in range(len(text))],
    }


@pytest.mark.parametrize(
    ("prev", "seg", "expected"),
    [
        (None, {"scene": "intro", "speaker": "narrator"}, 0.0),
        (
            {"scene": "hook", "speaker": "narrator"},
            {"scene": "hook", "speaker": "narrator"},
            PAUSE_SAME_SPEAKER,
        ),
        (
            {"scene": "hook", "speaker": "narrator"},
            {"scene": "hook", "speaker": "skeptic"},
            PAUSE_SPEAKER_CHANGE,
        ),
        (
            {"scene": "hook", "speaker": "narrator"},
            {"scene": "glossary", "speaker": "narrator"},
            PAUSE_SCENE_CHANGE,
        ),
        (
            {"scene": "glossary", "speaker": "narrator"},
            {"scene": "election", "speaker": "narrator"},
            PAUSE_CHAPTER_CHANGE,
        ),
    ],
)
def test_pause_before(prev, seg, expected):
    assert pause_before(prev, seg, CHAPTERS) == expected


@pytest.mark.parametrize(
    ("text", "offset", "expected"),
    [
        ("Ala ma kota", 0, 0.0),
        ("Ala ma kota", 4, 0.4),
        ("Ala ma kota", 3, 0.4),
        ("Ala ma kota", 99, 1.0),
    ],
)
def test_cue_seconds_uses_alignment_and_skips_spaces(text, offset, expected):
    assert cue_seconds(offset, align(text), text, 5.0) == pytest.approx(expected)


def test_cue_seconds_falls_back_to_proportional_when_alignment_differs():
    assert cue_seconds(5, align("inny, dłuższy tekst"), "abcdefghij", 10.0) == pytest.approx(5.0)


def test_word_times_groups_characters():
    assert word_times(align("Ala ma")) == [
        ("Ala", 0.0, pytest.approx(0.3)),
        ("ma", pytest.approx(0.4), pytest.approx(0.6)),
    ]


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [(0, "00:00:00,000"), (61.5, "00:01:01,500"), (3725.042, "01:02:05,042")],
)
def test_srt_time(seconds, expected):
    assert srt_time(seconds) == expected


def test_captions_split_long_segments_and_offset_by_segment_start():
    words = [(f"słowo{i:02d}", i * 0.5, i * 0.5 + 0.4) for i in range(20)]
    srt = captions([{"start": 10.0, "words": words}])
    blocks = srt.strip().split("\n\n")
    assert len(blocks) > 1
    assert blocks[0].splitlines()[1].startswith("00:00:10,000 --> ")
    assert all(len(b.splitlines()[2]) <= 84 for b in blocks)


def seg(sid: str, scene: str, start: float, end: float, cues: dict | None = None) -> dict:
    return {"id": sid, "scene": scene, "start": start, "end": end, "cue_times": cues or {}}


def test_group_scenes_merges_and_covers_audio():
    placed = [
        seg("s1", "intro", 0.0, 4.0, {"greeting": 0.1}),
        seg("s2", "hook", 4.8, 9.0, {"crash": 6.0}),
        seg("s3", "hook", 9.4, 12.0, {"vote": 10.0}),
        seg("s4", "glossary", 12.8, 20.0),
    ]
    scenes = group_scenes(placed, CHAPTERS, 20.6)
    assert [(s["id"], s["start"], s["end"]) for s in scenes] == [
        ("intro", 0.0, 4.8),
        ("hook", 4.8, 12.8),
        ("glossary", 12.8, 20.6),
    ]
    assert scenes[1]["cues"] == {"crash": 6.0, "vote": 10.0}
    assert scenes[1]["chapter"] == "c1"


def test_group_scenes_rejects_non_contiguous_scene():
    placed = [seg("s1", "hook", 0, 1), seg("s2", "glossary", 1, 2), seg("s3", "hook", 2, 3)]
    with pytest.raises(ValueError, match="not contiguous"):
        group_scenes(placed, CHAPTERS, 3.0)
