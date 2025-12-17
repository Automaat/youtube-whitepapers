"""Pytest fixtures for youtube-whitepapers tests."""

import json
import sys
from pathlib import Path

import pytest

# Add scripts to path for imports
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def temp_project(tmp_path):
    """Create temporary project structure mimicking real layout."""
    # Create directory structure
    youtube_dir = tmp_path / "youtube"
    pl_dir = youtube_dir / "pl"
    (pl_dir / "audio").mkdir(parents=True)
    (pl_dir / "slides").mkdir(parents=True)
    (pl_dir / "transcripts").mkdir(parents=True)
    (youtube_dir / "output").mkdir(parents=True)
    (youtube_dir / "thumbnails").mkdir(parents=True)
    (youtube_dir / "prompts").mkdir(parents=True)

    return tmp_path


@pytest.fixture
def sample_audio_files(temp_project):
    """Create sample audio files in project."""
    audio_dir = temp_project / "youtube" / "pl" / "audio"
    files = [
        "01-attention-is-all-you-need.m4a",
        "02-gpt.m4a",
        "15-glam.m4a",
    ]
    created = []
    for name in files:
        path = audio_dir / name
        path.write_bytes(b"fake audio content")
        created.append(path)
    return created


@pytest.fixture
def sample_pdf_files(temp_project):
    """Create sample PDF files in project."""
    slides_dir = temp_project / "youtube" / "pl" / "slides"
    files = ["01-attention-is-all-you-need.pdf", "02-gpt.pdf"]
    created = []
    for name in files:
        path = slides_dir / name
        path.write_bytes(b"%PDF-1.4 fake pdf")
        created.append(path)
    return created


@pytest.fixture
def sample_transcript(temp_project):
    """Create sample transcript JSON."""
    transcript_dir = temp_project / "youtube" / "pl" / "transcripts"
    transcript = {
        "text": "This is a test transcript about attention mechanisms.",
        "segments": [
            {"start": 0.0, "end": 5.0, "text": "Welcome to this episode."},
            {"start": 5.0, "end": 15.0, "text": "Today we discuss transformers."},
            {"start": 15.0, "end": 30.0, "text": "The attention mechanism is key."},
        ],
        "language": "pl",
    }
    path = transcript_dir / "01-attention-is-all-you-need.json"
    path.write_text(json.dumps(transcript, indent=2))
    return path


@pytest.fixture
def sample_template(temp_project):
    """Create sample prompt template."""
    prompts_dir = temp_project / "youtube" / "prompts"
    template = """# Video Generation Prompt

Generate video for episode: [EPISODE_NUMBER]-[EPISODE_NAME]

Read the slides and transcript carefully.
"""
    path = prompts_dir / "generate-video-command.md"
    path.write_text(template)
    return path


@pytest.fixture
def sample_thumbnail(temp_project):
    """Create sample thumbnail PNG (1x1 pixel red)."""
    thumbnails_dir = temp_project / "youtube" / "thumbnails"
    # Minimal valid PNG (1x1 red pixel)
    png_data = bytes(
        [
            0x89,
            0x50,
            0x4E,
            0x47,
            0x0D,
            0x0A,
            0x1A,
            0x0A,  # PNG signature
            0x00,
            0x00,
            0x00,
            0x0D,
            0x49,
            0x48,
            0x44,
            0x52,  # IHDR chunk
            0x00,
            0x00,
            0x00,
            0x01,
            0x00,
            0x00,
            0x00,
            0x01,  # 1x1
            0x08,
            0x02,
            0x00,
            0x00,
            0x00,
            0x90,
            0x77,
            0x53,
            0xDE,  # 8-bit RGB
            0x00,
            0x00,
            0x00,
            0x0C,
            0x49,
            0x44,
            0x41,
            0x54,  # IDAT chunk
            0x08,
            0xD7,
            0x63,
            0xF8,
            0xCF,
            0xC0,
            0x00,
            0x00,
            0x00,
            0x03,
            0x00,
            0x01,
            0x00,
            0x18,
            0xDD,
            0x8D,
            0xB4,
            0x00,
            0x00,
            0x00,
            0x00,
            0x49,
            0x45,
            0x4E,
            0x44,  # IEND chunk
            0xAE,
            0x42,
            0x60,
            0x82,
        ]
    )
    path = thumbnails_dir / "01-attention-is-all-you-need.png"
    path.write_bytes(png_data)
    return path


@pytest.fixture
def sample_last_slide(temp_project):
    """Create sample last-slide.png."""
    slides_dir = temp_project / "youtube" / "pl" / "slides"
    # Same minimal PNG
    png_data = bytes(
        [
            0x89,
            0x50,
            0x4E,
            0x47,
            0x0D,
            0x0A,
            0x1A,
            0x0A,
            0x00,
            0x00,
            0x00,
            0x0D,
            0x49,
            0x48,
            0x44,
            0x52,
            0x00,
            0x00,
            0x00,
            0x01,
            0x00,
            0x00,
            0x00,
            0x01,
            0x08,
            0x02,
            0x00,
            0x00,
            0x00,
            0x90,
            0x77,
            0x53,
            0xDE,
            0x00,
            0x00,
            0x00,
            0x0C,
            0x49,
            0x44,
            0x41,
            0x54,
            0x08,
            0xD7,
            0x63,
            0xF8,
            0xCF,
            0xC0,
            0x00,
            0x00,
            0x00,
            0x03,
            0x00,
            0x01,
            0x00,
            0x18,
            0xDD,
            0x8D,
            0xB4,
            0x00,
            0x00,
            0x00,
            0x00,
            0x49,
            0x45,
            0x4E,
            0x44,
            0xAE,
            0x42,
            0x60,
            0x82,
        ]
    )
    path = slides_dir / "last-slide.png"
    path.write_bytes(png_data)
    return path
