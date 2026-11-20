"""Tests for odczyt.tts."""

import pytest

from odczyt.tts import cache_key, resolve_api_key, strip_cues


@pytest.mark.parametrize(
    ("text", "clean", "cues"),
    [
        ("Ala ma kota.", "Ala ma kota.", {}),
        ("Gdy [[cue:timeout]] minie czas.", "Gdy minie czas.", {"timeout": 4}),
        ("[[cue:start]] Leader padł.", "Leader padł.", {"start": 0}),
        ("Koniec. [[cue:end]]", "Koniec.", {"end": 7}),
        ("A [[cue:a]] B [[cue:b]] C", "A B C", {"a": 2, "b": 4}),
        ("słowo,[[cue:x]]dalej", "słowo, dalej", {"x": 7}),
    ],
)
def test_strip_cues(text, clean, cues):
    got_clean, got_cues = strip_cues(text)
    assert got_clean == clean
    assert got_cues == cues
    for name, offset in cues.items():
        assert offset <= len(got_clean), name


def test_cue_offset_points_at_following_word():
    clean, cues = strip_cues("Zwiększa swój [[cue:term]] term i prosi o głosy.")
    assert clean[cues["term"] :].startswith("term i prosi")


@pytest.mark.parametrize(
    ("a", "b", "same"),
    [
        (("tekst", "v1", "eleven_v4"), ("tekst", "v1", "eleven_v4"), True),
        (("tekst", "v1", "eleven_v4"), ("tekst!", "v1", "eleven_v4"), False),
        (("tekst", "v1", "eleven_v4"), ("tekst", "v2", "eleven_v4"), False),
        (("tekst", "v1", "eleven_v4"), ("tekst", "v1", "eleven_v3"), False),
    ],
)
def test_cache_key_changes_with_inputs(a, b, same):
    assert (cache_key(*a) == cache_key(*b)) is same


def test_resolve_api_key_prefers_file_then_env(tmp_path, monkeypatch):
    key = tmp_path / "key"
    key.write_text("from-file\n")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "from-env")
    assert resolve_api_key(str(key), None) == "from-file"
    assert resolve_api_key(None, None) == "from-env"


def test_resolve_api_key_none_without_sources(monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    monkeypatch.delenv("BW_SESSION", raising=False)
    assert resolve_api_key(None, "item") is None
