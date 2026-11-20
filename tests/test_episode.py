"""Tests for odczyt.episode and odczyt.paper."""

import json
from pathlib import Path

import pytest

from odczyt.episode import (
    digest,
    find_episode_dir,
    find_paper,
    load_episode,
    load_yaml,
    merge,
    new_episode,
)
from odczyt.paper import format_pages


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


def test_merge_is_deep_and_override_wins():
    base = {"voices": {"narrator": "a", "skeptic": "b"}, "theme": "dark"}
    assert merge(base, {"voices": {"skeptic": "c"}}) == {
        "voices": {"narrator": "a", "skeptic": "c"},
        "theme": "dark",
    }


def test_digest_changes_with_file_content(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("1")
    first = digest(f, {"k": 1})
    f.write_text("2")
    assert digest(f, {"k": 1}) != first
    assert digest(tmp_path / "missing") == digest(tmp_path / "other-missing")


def make_repo(tmp_path: Path) -> tuple[Path, Path]:
    pdf = tmp_path / "whitepapers" / "distributed-computing" / "74-epaxos.pdf"
    pdf.parent.mkdir(parents=True)
    pdf.write_bytes(b"%PDF")
    status = tmp_path / "status.json"
    status.write_text(
        json.dumps(
            {"papers": [{"episode": "74", "name": "epaxos", "category": "distributed-computing"}]}
        )
    )
    return pdf, status


def test_find_paper_uses_status_then_glob(tmp_path):
    pdf, status = make_repo(tmp_path)
    assert find_paper(74, tmp_path, status) == pdf
    assert find_paper(74, tmp_path, tmp_path / "none.json") == pdf
    assert find_paper(75, tmp_path, status) is None


def test_new_episode_writes_config_and_loads_with_defaults(tmp_path):
    _, status = make_repo(tmp_path)
    episodes = tmp_path / "episodes"
    defaults = tmp_path / "pipeline.yaml"
    defaults.write_text("theme: dark\nvoices: {narrator: n, skeptic: s}\n")
    path = new_episode(74, repo=tmp_path, episodes_dir=episodes, status_file=status)
    assert path.name == "74-epaxos"
    ep = load_episode(74, episodes, defaults, tmp_path)
    assert ep.config["paper"] == "whitepapers/distributed-computing/74-epaxos.pdf"
    assert ep.config["theme"] == "dark"
    ep.update(title="EPaxos")
    assert load_yaml(path / "episode.yaml") == {**ep.raw}
    assert "theme" not in ep.raw
    with pytest.raises(FileExistsError):
        new_episode(74, repo=tmp_path, episodes_dir=episodes, status_file=status)


def test_new_episode_without_paper_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        new_episode(80, repo=tmp_path, episodes_dir=tmp_path / "e", status_file=tmp_path / "s")
