"""Fixtures for odczyt tests."""

import pytest

from odczyt.episode import Episode, dump_yaml


@pytest.fixture
def episode(tmp_path) -> Episode:
    """A minimal episode in a temporary repository."""
    episode_dir = tmp_path / "youtube" / "pl" / "episodes" / "73-raft"
    episode_dir.mkdir(parents=True)
    raw = {"number": 73, "slug": "73-raft", "paper": "whitepapers/x/73-raft.pdf"}
    dump_yaml(episode_dir / "episode.yaml", raw)
    config = {**raw, "target_minutes": 12, "voices": {"narrator": "n", "skeptic": "s"}}
    return Episode(episode_dir, config, tmp_path, dict(raw))
