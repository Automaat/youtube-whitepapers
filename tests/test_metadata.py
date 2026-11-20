"""Tests for odczyt.metadata."""

import pytest

from odczyt.metadata import chapter_marks, clock, format_metadata

TIMELINE = {
    "chapters": [{"id": "c1", "title": "Problem"}, {"id": "c2", "title": "Wybór"}],
    "scenes": [
        {"id": "intro", "chapter": None, "start": 0.0},
        {"id": "hook", "chapter": "c1", "start": 22.4},
        {"id": "x", "chapter": "c1", "start": 80.0},
        {"id": "y", "chapter": "c2", "start": 3725.0},
    ],
}

DATA = {
    "title": "Konsensus (Raft) - Ongaro 2014",
    "intro": "🎙️ Opis.",
    "topics": ["Jeden", "Dwa"],
    "publication": "USENIX ATC 2014",
    "tags": ["#Raft", "Systemy Rozproszone"],
}


@pytest.mark.parametrize(("sec", "text"), [(0, "0:00"), (22.9, "0:22"), (3725, "1:02:05")])
def test_clock(sec, text):
    assert clock(sec) == text


def test_chapter_marks_start_at_zero_and_skip_short():
    assert chapter_marks(TIMELINE) == [(0.0, "Wstęp"), (22.4, "Problem"), (3725.0, "Wybór")]
    early = {
        **TIMELINE,
        "scenes": [{**s, "start": min(s["start"], 5.0)} for s in TIMELINE["scenes"]],
    }
    assert chapter_marks(early) == [(0.0, "Wstęp")]


def test_format_metadata_matches_upload_parser(episode):
    episode.config.update(paper_url="https://raft.github.io/raft.pdf", authors="D. Ongaro")
    text = format_metadata(episode, DATA, TIMELINE)
    assert text.startswith("TYTUŁ:\nKonsensus (Raft) - Ongaro 2014 | Deep Dive\n\nOPIS:\n🎙️ Opis.")
    assert "0:22 Problem\n1:02:05 Wybór" in text
    assert text.endswith("TAGI:\n#Raft #SystemyRozproszone\n")


def test_format_metadata_rejects_long_title(episode):
    episode.config.update(paper_url="u", authors="a")
    with pytest.raises(ValueError, match="Title"):
        format_metadata(episode, {**DATA, "title": "x" * 95}, TIMELINE)
