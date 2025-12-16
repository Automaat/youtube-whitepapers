"""Configuration management using pydantic-settings."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="NOTEBOOKLM_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Chrome/Browser settings
    chrome_profile_dir: Path = Field(
        default=Path.home() / ".notebooklm-chrome",
        description="Chrome profile directory for persistent sessions",
    )
    chrome_debug_port: int = Field(
        default=9222,
        description="Chrome remote debugging port",
    )
    headless: bool = Field(
        default=False,
        description="Run browser in headless mode",
    )

    # Timeouts (in seconds)
    page_load_timeout: int = Field(default=30)
    source_processing_timeout: int = Field(default=120)
    audio_generation_timeout: int = Field(default=900)  # 15 minutes
    slides_generation_timeout: int = Field(default=180)

    # Output directories
    output_dir: Path = Field(
        default=Path.cwd() / "output",
        description="Default output directory for downloads",
    )

    # URLs
    notebooklm_base_url: str = Field(
        default="https://notebooklm.google.com",
    )


settings = Settings()
