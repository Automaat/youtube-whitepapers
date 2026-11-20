"""Episode files, defaults and bootstrap for the diagram-first pipeline."""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from odczyt.paths import DEFAULTS_FILE, EPISODES_DIR, REPO_DIR, STATUS_FILE


def find_episode_dir(ep: str | int, episodes_dir: Path = EPISODES_DIR) -> Path | None:
    """Return the episode directory matching an episode number."""
    matches = sorted(episodes_dir.glob(f"{int(ep):02d}-*"))
    return matches[0] if matches else None


def load_yaml(path: Path) -> dict:
    """Load a YAML mapping from a file."""
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def dump_yaml(path: Path, data: dict) -> None:
    """Write a YAML mapping, keeping key order and Polish characters."""
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8"
    )


def merge(base: dict, override: dict) -> dict:
    """Deep-merge two mappings; values from `override` win."""
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge(out[key], value)
        else:
            out[key] = value
    return out


def digest(*parts: Any) -> str:
    """Short stable hash of JSON-serializable values and file contents."""
    h = hashlib.sha256()
    for part in parts:
        if isinstance(part, Path):
            h.update(part.read_bytes() if part.exists() else b"<missing>")
        else:
            h.update(json.dumps(part, ensure_ascii=False, sort_keys=True).encode())
        h.update(b"\0")
    return h.hexdigest()[:16]


@dataclass
class Episode:
    """One episode directory with its configuration merged over the pipeline defaults."""

    dir: Path
    config: dict
    repo: Path = REPO_DIR
    raw: dict = field(default_factory=dict)

    @property
    def number(self) -> int:
        return int(self.config["number"])

    @property
    def slug(self) -> str:
        return str(self.config["slug"])

    @property
    def build(self) -> Path:
        path = self.dir / "build"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def public(self) -> Path:
        path = self.build / "public"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def scenes_dir(self) -> Path:
        """Remotion source folder with this episode's scene code."""
        return self.repo / "youtube" / "remotion" / "src" / "episodes" / self.slug

    def file(self, name: str) -> Path:
        return self.dir / name

    def rel(self, path: Path) -> str:
        return str(path.relative_to(self.repo))

    def storyboard(self) -> dict:
        return load_yaml(self.file("storyboard.yaml"))

    def script(self) -> dict:
        return load_yaml(self.file("script.yaml"))

    def update(self, **fields: Any) -> None:
        """Write fields to episode.yaml (not to the defaults) and reload."""
        self.raw = {**self.raw, **fields}
        dump_yaml(self.file("episode.yaml"), self.raw)
        self.config = merge(self.config, fields)


def load_defaults(path: Path = DEFAULTS_FILE) -> dict:
    return load_yaml(path) if path.exists() else {}


def load_episode(
    ep: str | int,
    episodes_dir: Path = EPISODES_DIR,
    defaults_file: Path = DEFAULTS_FILE,
    repo: Path = REPO_DIR,
) -> Episode:
    """Load an episode by number; raise FileNotFoundError when it does not exist."""
    episode_dir = find_episode_dir(ep, episodes_dir)
    if episode_dir is None:
        raise FileNotFoundError(f"No episode directory for {ep} in {episodes_dir}")
    raw = load_yaml(episode_dir / "episode.yaml")
    return Episode(episode_dir, merge(load_defaults(defaults_file), raw), repo, raw)


def find_paper(number: int, repo: Path = REPO_DIR, status_file: Path = STATUS_FILE) -> Path | None:
    """Locate the paper PDF of an episode via status.json, then by file name."""
    if status_file.exists():
        papers = json.loads(status_file.read_text(encoding="utf-8")).get("papers", [])
        for p in papers:
            if int(p["episode"]) == number:
                pdf = repo / "whitepapers" / p["category"] / f"{p['episode']}-{p['name']}.pdf"
                if pdf.exists():
                    return pdf
    matches = sorted((repo / "whitepapers").glob(f"*/{number:02d}-*.pdf"))
    return matches[0] if matches else None


def new_episode(
    number: int,
    paper: Path | None = None,
    repo: Path = REPO_DIR,
    episodes_dir: Path = EPISODES_DIR,
    status_file: Path = STATUS_FILE,
) -> Path:
    """Create youtube/pl/episodes/{slug}/episode.yaml for a paper; return the directory."""
    existing = find_episode_dir(number, episodes_dir)
    if existing is not None:
        raise FileExistsError(f"Episode {number} already exists: {existing}")
    pdf = paper.resolve() if paper else find_paper(number, repo, status_file)
    if pdf is None or not pdf.exists():
        raise FileNotFoundError(f"No paper PDF for episode {number}; pass --paper")
    stem = pdf.stem
    prefix = f"{number:02d}-"
    slug = stem if stem.startswith(prefix) else prefix + stem
    episode_dir = episodes_dir / slug
    episode_dir.mkdir(parents=True)
    dump_yaml(
        episode_dir / "episode.yaml",
        {"number": number, "slug": slug, "paper": str(pdf.relative_to(repo))},
    )
    return episode_dir
