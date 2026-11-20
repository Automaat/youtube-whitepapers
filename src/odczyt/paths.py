"""Repository paths used by the pipeline."""

from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[2]
YOUTUBE_DIR = REPO_DIR / "youtube"
EPISODES_DIR = YOUTUBE_DIR / "pl" / "episodes"
PROMPTS_DIR = YOUTUBE_DIR / "prompts" / "pipeline"
REMOTION_DIR = YOUTUBE_DIR / "remotion"
OUTPUT_DIR = YOUTUBE_DIR / "output"
THUMBNAILS_DIR = YOUTUBE_DIR / "thumbnails"
DEFAULTS_FILE = YOUTUBE_DIR / "pipeline.yaml"
STATUS_FILE = REPO_DIR / "whitepapers" / "status.json"
