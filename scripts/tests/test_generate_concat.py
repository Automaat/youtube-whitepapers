"""Tests for generate_concat.py"""

import pytest
from pathlib import Path
from scripts.generate_concat import (
    generate_concat,
    parse_durations_string,
    parse_durations_json,
)


def test_generate_concat_basic():
    """Test basic concat generation with template."""
    slide_durations = [
        ("slide-01", 120.0),
        ("slide-02", 90.0),
    ]
    result = generate_concat("55-olmo", slide_durations)

    assert "thumbnail.png" in result
    assert "slide-01.png" in result
    assert "slide-02.png" in result
    assert "last-slide.png" in result
    assert "duration 5" in result  # Intro
    assert "duration 0" in result  # Duplicate to avoid drop
    assert "duration 120.0" in result
    assert "duration 90.0" in result


def test_generate_concat_structure():
    """Test concat.txt has correct structure."""
    slide_durations = [("slide-01", 100.0)]
    result = generate_concat("55-olmo", slide_durations)
    lines = result.strip().split("\n")

    # Check structure
    assert lines[0].endswith("thumbnail.png'")
    assert lines[1] == "duration 5"
    assert lines[2].endswith("thumbnail.png'")  # Duplicate
    assert lines[3] == "duration 0"
    assert lines[4].endswith("slide-01.png'")
    assert lines[5] == "duration 100.0"
    assert lines[6].endswith("last-slide.png'")
    assert lines[7] == "duration 5"
    assert lines[8].endswith("last-slide.png'")


def test_parse_durations_string():
    """Test parsing durations from command line string."""
    input_str = "slide-01:180,slide-02:150.5,slide-03:120"
    result = parse_durations_string(input_str)

    assert result == [
        ("slide-01", 180.0),
        ("slide-02", 150.5),
        ("slide-03", 120.0),
    ]


def test_parse_durations_string_with_spaces():
    """Test parsing with whitespace."""
    input_str = "slide-01:180, slide-02:150, slide-03:120"
    result = parse_durations_string(input_str)

    assert len(result) == 3
    assert result[0] == ("slide-01", 180.0)


def test_parse_durations_json(tmp_path):
    """Test parsing durations from JSON file."""
    json_file = tmp_path / "timings.json"
    json_file.write_text(
        '[{"slide": "slide-01", "duration": 180}, '
        '{"slide": "slide-02", "duration": 150.5}]'
    )

    result = parse_durations_json(json_file)

    assert result == [
        ("slide-01", 180),
        ("slide-02", 150.5),
    ]


def test_generate_concat_absolute_paths():
    """Test that paths are absolute."""
    slide_durations = [("slide-01", 100.0)]
    result = generate_concat("55-olmo", slide_durations)

    # Should contain absolute paths
    assert "/youtube/pl/slides/55-olmo/" in result
    assert not result.startswith("file 'youtube/")


def test_generate_concat_multiple_slides():
    """Test concat with many slides."""
    slide_durations = [(f"slide-{i:02d}", float(i * 10)) for i in range(1, 12)]
    result = generate_concat("55-olmo", slide_durations)

    # Check all slides present
    for i in range(1, 12):
        assert f"slide-{i:02d}.png" in result
        assert f"duration {i * 10}.0" in result

    # Check template
    assert result.count("thumbnail.png") == 2
    assert result.count("last-slide.png") == 2
