"""Tests for episode_pipeline.py and extract_paper_text.py."""

import pytest

from scripts.episode_pipeline import find_episode_dir, load_yaml
from scripts.extract_paper_text import format_pages


@pytest.mark.parametrize(("ep", "expected"), [("73", "73-raft"), ("7", "07-zero"), ("99", None)])
def test_find_episode_dir(tmp_path, ep, expected):
    for name in ("73-raft", "07-zero", "173-other"):
        (tmp_path / name).mkdir()
    found = find_episode_dir(ep, tmp_path)
    assert (found.name if found else None) == expected


def test_load_yaml_requires_mapping(tmp_path):
    path = tmp_path / "x.yaml"
    path.write_text("- a\n- b\n")
    with pytest.raises(ValueError, match="mapping"):
        load_yaml(path)


def test_format_pages_numbers_from_one():
    assert format_pages(["a", "b"]) == "=== page 1 ===\na\n\n=== page 2 ===\nb\n"
