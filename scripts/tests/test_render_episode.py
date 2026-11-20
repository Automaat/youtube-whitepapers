"""Tests for render_episode.py."""

from scripts.render_episode import still_frames

TIMELINE = {
    "fps": 30,
    "introSeconds": 5.0,
    "audioSeconds": 30.0,
    "scenes": [
        {"id": "intro", "start": 0.0, "end": 8.0, "cues": {"greeting": 0.2}},
        {"id": "hook", "start": 8.0, "end": 30.0, "cues": {"crash": 20.0, "start": 8.1}},
    ],
}


def test_still_frames_full_episode():
    frames = still_frames(TIMELINE)
    names = [n for _, n in frames]
    assert names == [
        "00-intro-thumbnail",
        "01-intro--greeting",
        "01-intro--end",
        "02-hook--start",
        "02-hook--crash",
        "02-hook--end",
        "99-outro",
    ]
    by_name = {n: f for f, n in frames}
    assert by_name["01-intro--greeting"] == 150
    assert by_name["02-hook--crash"] == 618
    assert by_name["02-hook--end"] == 891
    assert by_name["99-outro"] == 990


def test_still_frames_selected_scenes_only():
    names = [n for _, n in still_frames(TIMELINE, {"hook"})]
    assert names == ["02-hook--start", "02-hook--crash", "02-hook--end"]
