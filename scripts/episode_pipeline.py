"""Shared paths and file helpers for the diagram-first episode pipeline."""

from pathlib import Path

import yaml

REPO_DIR = Path(__file__).resolve().parent.parent
EPISODES_DIR = REPO_DIR / "youtube" / "pl" / "episodes"
PROMPTS_DIR = REPO_DIR / "youtube" / "prompts" / "pipeline"
REMOTION_DIR = REPO_DIR / "youtube" / "remotion"


def find_episode_dir(ep: str, episodes_dir: Path = EPISODES_DIR) -> Path | None:
    """Return the episode directory matching an episode number."""
    matches = sorted(episodes_dir.glob(f"{int(ep):02d}-*"))
    return matches[0] if matches else None


def build_dir(episode_dir: Path) -> Path:
    """Return the git-ignored build directory of an episode, creating it."""
    path = episode_dir / "build"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_yaml(path: Path) -> dict:
    """Load a YAML mapping from a file."""
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def load_episode(episode_dir: Path) -> dict:
    """Load episode.yaml (paper path, title, voices, theme)."""
    return load_yaml(episode_dir / "episode.yaml")
