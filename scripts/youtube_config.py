#!/usr/bin/env python3
"""YouTube upload configuration."""

import os
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent


@dataclass
class YouTubeSettings:
    """YouTube upload settings from environment variables."""

    credentials_dir: Path = field(default_factory=lambda: SCRIPT_DIR / ".youtube-credentials")
    client_secret_file: str = "client_secret.json"
    token_file: str = "token.json"

    playlist_llm: str | None = field(default_factory=lambda: os.environ.get("YOUTUBE_PLAYLIST_LLM"))
    playlist_distributed_computing: str | None = field(
        default_factory=lambda: os.environ.get("YOUTUBE_PLAYLIST_DISTRIBUTED_COMPUTING")
    )
    playlist_security: str | None = field(
        default_factory=lambda: os.environ.get("YOUTUBE_PLAYLIST_SECURITY")
    )

    chunk_size_mb: int = 10
    default_privacy: str = "private"

    @property
    def client_secret_path(self) -> Path:
        return self.credentials_dir / self.client_secret_file

    @property
    def token_path(self) -> Path:
        return self.credentials_dir / self.token_file


settings = YouTubeSettings()
