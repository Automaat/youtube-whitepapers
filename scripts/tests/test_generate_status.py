"""Tests for generate_status.py script."""

import json
from unittest.mock import patch

import pytest


@pytest.fixture
def project_with_whitepapers(temp_project):
    """Create temp project with whitepapers structure."""
    whitepapers_dir = temp_project / "whitepapers"

    llm_dir = whitepapers_dir / "llm"
    llm_dir.mkdir(parents=True)
    (llm_dir / "01-attention-is-all-you-need.pdf").write_bytes(b"pdf")
    (llm_dir / "01-attention-is-all-you-need-slides.pdf").write_bytes(b"pdf")
    (llm_dir / "02-gpt.pdf").write_bytes(b"pdf")

    dc_dir = whitepapers_dir / "distributed-computing"
    dc_dir.mkdir(parents=True)
    (dc_dir / "64-lamport-clocks.pdf").write_bytes(b"pdf")

    archive_dir = temp_project / "archive" / "pl"
    (archive_dir / "audio").mkdir(parents=True)
    (archive_dir / "slides").mkdir(parents=True)
    (archive_dir / "transcripts").mkdir(parents=True)
    (archive_dir / "video").mkdir(parents=True)
    (archive_dir / "thumbnails").mkdir(parents=True)

    return temp_project


class TestScanWhitepapers:
    """Tests for scan_whitepapers function."""

    def test_finds_all_papers(self, project_with_whitepapers):
        """Should find all PDF papers (not slides)."""
        from scripts.generate_status import scan_whitepapers

        with patch(
            "scripts.generate_status.WHITEPAPERS_DIR",
            project_with_whitepapers / "whitepapers",
        ):
            papers = scan_whitepapers()

        assert len(papers) == 3
        episodes = [p["episode"] for p in papers]
        assert "01" in episodes
        assert "02" in episodes
        assert "64" in episodes

    def test_extracts_category(self, project_with_whitepapers):
        """Should extract category from directory name."""
        from scripts.generate_status import scan_whitepapers

        with patch(
            "scripts.generate_status.WHITEPAPERS_DIR",
            project_with_whitepapers / "whitepapers",
        ):
            papers = scan_whitepapers()

        llm_paper = next(p for p in papers if p["episode"] == "01")
        assert llm_paper["category"] == "llm"

        dc_paper = next(p for p in papers if p["episode"] == "64")
        assert dc_paper["category"] == "distributed-computing"

    def test_extracts_paper_name(self, project_with_whitepapers):
        """Should extract paper name without episode number."""
        from scripts.generate_status import scan_whitepapers

        with patch(
            "scripts.generate_status.WHITEPAPERS_DIR",
            project_with_whitepapers / "whitepapers",
        ):
            papers = scan_whitepapers()

        paper = next(p for p in papers if p["episode"] == "01")
        assert paper["name"] == "attention-is-all-you-need"


class TestCheckExists:
    """Tests for check_exists function."""

    def test_returns_true_when_file_exists(self, temp_project):
        """Should return True when file matching pattern exists."""
        from scripts.generate_status import check_exists

        audio_dir = temp_project / "youtube" / "pl" / "audio"
        (audio_dir / "01-test.m4a").write_bytes(b"audio")

        result = check_exists([audio_dir], "01-*.m4a")

        assert result is True

    def test_returns_false_when_no_match(self, temp_project):
        """Should return False when no file matches."""
        from scripts.generate_status import check_exists

        audio_dir = temp_project / "youtube" / "pl" / "audio"

        result = check_exists([audio_dir], "99-*.m4a")

        assert result is False

    def test_searches_multiple_directories(self, temp_project):
        """Should search all provided directories."""
        from scripts.generate_status import check_exists

        dir1 = temp_project / "dir1"
        dir1.mkdir()
        dir2 = temp_project / "dir2"
        dir2.mkdir()
        (dir2 / "found.txt").write_text("content")

        result = check_exists([dir1, dir2], "found.txt")

        assert result is True


class TestCheckSlidesExist:
    """Tests for check_slides_exist function."""

    def test_returns_true_for_slides_dir_with_pngs(self, temp_project):
        """Should return True when slides directory has PNG files."""
        from scripts.generate_status import check_slides_exist

        slides_dir = temp_project / "youtube" / "pl" / "slides"
        ep_slides = slides_dir / "01-test"
        ep_slides.mkdir(parents=True)
        (ep_slides / "slide-01.png").write_bytes(b"png")

        result = check_slides_exist([slides_dir], "01-test")

        assert result is True

    def test_returns_false_for_empty_dir(self, temp_project):
        """Should return False for empty slides directory."""
        from scripts.generate_status import check_slides_exist

        slides_dir = temp_project / "youtube" / "pl" / "slides"
        ep_slides = slides_dir / "01-test"
        ep_slides.mkdir(parents=True)

        result = check_slides_exist([slides_dir], "01-test")

        assert result is False

    def test_returns_false_for_missing_dir(self, temp_project):
        """Should return False when slides directory doesn't exist."""
        from scripts.generate_status import check_slides_exist

        slides_dir = temp_project / "youtube" / "pl" / "slides"

        result = check_slides_exist([slides_dir], "99-nonexistent")

        assert result is False

    def test_returns_true_for_pdf_file(self, temp_project):
        """Should return True when PDF file exists in slides directory."""
        from scripts.generate_status import check_slides_exist

        slides_dir = temp_project / "youtube" / "pl" / "slides"
        slides_dir.mkdir(parents=True, exist_ok=True)
        (slides_dir / "55-olmo.pdf").write_bytes(b"pdf")

        result = check_slides_exist([slides_dir], "55-olmo")

        assert result is True


class TestCheckArchived:
    """Tests for check_archived function."""

    def test_returns_true_when_archive_audio_exists(self, project_with_whitepapers):
        """Should return True when audio in archive."""
        from scripts.generate_status import check_archived

        archive_audio = project_with_whitepapers / "archive" / "pl" / "audio"
        (archive_audio / "01-test.m4a").write_bytes(b"audio")

        with patch(
            "scripts.generate_status.ARCHIVE_DIR",
            project_with_whitepapers / "archive" / "pl",
        ):
            result = check_archived("01-test")

        assert result is True

    def test_returns_true_when_archive_video_exists(self, project_with_whitepapers):
        """Should return True when video in archive."""
        from scripts.generate_status import check_archived

        archive_video = project_with_whitepapers / "archive" / "pl" / "video"
        (archive_video / "01-test.mp4").write_bytes(b"video")

        with patch(
            "scripts.generate_status.ARCHIVE_DIR",
            project_with_whitepapers / "archive" / "pl",
        ):
            result = check_archived("01-test")

        assert result is True

    def test_returns_false_when_not_archived(self, project_with_whitepapers):
        """Should return False when no archive files."""
        from scripts.generate_status import check_archived

        with patch(
            "scripts.generate_status.ARCHIVE_DIR",
            project_with_whitepapers / "archive" / "pl",
        ):
            result = check_archived("99-nonexistent")

        assert result is False


class TestGenerateStatus:
    """Tests for generate_status function."""

    def test_scans_all_papers(self, project_with_whitepapers):
        """Should include all papers from whitepapers directory."""
        from scripts.generate_status import generate_status

        status_file = project_with_whitepapers / "whitepapers" / "status.json"

        with (
            patch(
                "scripts.generate_status.WHITEPAPERS_DIR",
                project_with_whitepapers / "whitepapers",
            ),
            patch("scripts.generate_status.SCRIPT_DIR", project_with_whitepapers),
            patch("scripts.generate_status.YOUTUBE_DIR", project_with_whitepapers / "youtube"),
            patch(
                "scripts.generate_status.ASSETS_DIR", project_with_whitepapers / "youtube" / "pl"
            ),
            patch(
                "scripts.generate_status.ARCHIVE_DIR", project_with_whitepapers / "archive" / "pl"
            ),
            patch(
                "scripts.generate_status.AUDIO_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "audio"],
            ),
            patch(
                "scripts.generate_status.SLIDES_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "slides"],
            ),
            patch(
                "scripts.generate_status.TRANSCRIPTS_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "transcripts"],
            ),
            patch(
                "scripts.generate_status.THUMBNAILS_DIRS",
                [project_with_whitepapers / "youtube" / "thumbnails"],
            ),
            patch(
                "scripts.generate_status.VIDEO_DIRS",
                [project_with_whitepapers / "youtube" / "output"],
            ),
            patch("scripts.status_utils.STATUS_FILE", status_file),
            patch("status_utils.STATUS_FILE", status_file),
            patch("scripts.status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
            patch("status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
        ):
            status = generate_status()

        assert len(status["papers"]) == 3
        assert status["summary"]["total"] == 3

    def test_detects_audio_files(self, project_with_whitepapers):
        """Should detect audio files in youtube/pl/audio."""
        from scripts.generate_status import generate_status

        audio_dir = project_with_whitepapers / "youtube" / "pl" / "audio"
        (audio_dir / "01-attention-is-all-you-need.m4a").write_bytes(b"audio")

        status_file = project_with_whitepapers / "whitepapers" / "status.json"

        with (
            patch(
                "scripts.generate_status.WHITEPAPERS_DIR",
                project_with_whitepapers / "whitepapers",
            ),
            patch("scripts.generate_status.SCRIPT_DIR", project_with_whitepapers),
            patch("scripts.generate_status.YOUTUBE_DIR", project_with_whitepapers / "youtube"),
            patch(
                "scripts.generate_status.ASSETS_DIR", project_with_whitepapers / "youtube" / "pl"
            ),
            patch(
                "scripts.generate_status.ARCHIVE_DIR", project_with_whitepapers / "archive" / "pl"
            ),
            patch(
                "scripts.generate_status.AUDIO_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "audio"],
            ),
            patch(
                "scripts.generate_status.SLIDES_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "slides"],
            ),
            patch(
                "scripts.generate_status.TRANSCRIPTS_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "transcripts"],
            ),
            patch(
                "scripts.generate_status.THUMBNAILS_DIRS",
                [project_with_whitepapers / "youtube" / "thumbnails"],
            ),
            patch(
                "scripts.generate_status.VIDEO_DIRS",
                [project_with_whitepapers / "youtube" / "output"],
            ),
            patch("scripts.status_utils.STATUS_FILE", status_file),
            patch("status_utils.STATUS_FILE", status_file),
            patch("scripts.status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
            patch("status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
        ):
            status = generate_status()

        paper = next(p for p in status["papers"] if p["episode"] == "01")
        assert paper.get("audio") is True

    def test_preserves_manual_fields(self, project_with_whitepapers):
        """Should preserve notebook_created from existing status."""
        from scripts.generate_status import generate_status

        status_file = project_with_whitepapers / "whitepapers" / "status.json"
        status_file.parent.mkdir(parents=True, exist_ok=True)
        existing = {
            "papers": [
                {
                    "episode": "01",
                    "name": "attention-is-all-you-need",
                    "category": "llm",
                    "notebook_created": True,
                }
            ],
            "summary": {},
            "updated": "",
        }
        status_file.write_text(json.dumps(existing))

        with (
            patch(
                "scripts.generate_status.WHITEPAPERS_DIR",
                project_with_whitepapers / "whitepapers",
            ),
            patch("scripts.generate_status.SCRIPT_DIR", project_with_whitepapers),
            patch("scripts.generate_status.YOUTUBE_DIR", project_with_whitepapers / "youtube"),
            patch(
                "scripts.generate_status.ASSETS_DIR", project_with_whitepapers / "youtube" / "pl"
            ),
            patch(
                "scripts.generate_status.ARCHIVE_DIR", project_with_whitepapers / "archive" / "pl"
            ),
            patch(
                "scripts.generate_status.AUDIO_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "audio"],
            ),
            patch(
                "scripts.generate_status.SLIDES_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "slides"],
            ),
            patch(
                "scripts.generate_status.TRANSCRIPTS_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "transcripts"],
            ),
            patch(
                "scripts.generate_status.THUMBNAILS_DIRS",
                [project_with_whitepapers / "youtube" / "thumbnails"],
            ),
            patch(
                "scripts.generate_status.VIDEO_DIRS",
                [project_with_whitepapers / "youtube" / "output"],
            ),
            patch("scripts.status_utils.STATUS_FILE", status_file),
            patch("status_utils.STATUS_FILE", status_file),
            patch("scripts.status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
            patch("status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
        ):
            status = generate_status()

        paper = next(p for p in status["papers"] if p["episode"] == "01")
        assert paper.get("notebook_created") is True

    def test_preserves_uploaded_field(self, project_with_whitepapers):
        """Should preserve uploaded from existing status."""
        from scripts.generate_status import generate_status

        status_file = project_with_whitepapers / "whitepapers" / "status.json"
        status_file.parent.mkdir(parents=True, exist_ok=True)
        existing = {
            "papers": [
                {
                    "episode": "01",
                    "name": "attention-is-all-you-need",
                    "category": "llm",
                    "uploaded": True,
                }
            ],
            "summary": {},
            "updated": "",
        }
        status_file.write_text(json.dumps(existing))

        with (
            patch(
                "scripts.generate_status.WHITEPAPERS_DIR",
                project_with_whitepapers / "whitepapers",
            ),
            patch("scripts.generate_status.SCRIPT_DIR", project_with_whitepapers),
            patch("scripts.generate_status.YOUTUBE_DIR", project_with_whitepapers / "youtube"),
            patch(
                "scripts.generate_status.ASSETS_DIR", project_with_whitepapers / "youtube" / "pl"
            ),
            patch(
                "scripts.generate_status.ARCHIVE_DIR", project_with_whitepapers / "archive" / "pl"
            ),
            patch(
                "scripts.generate_status.AUDIO_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "audio"],
            ),
            patch(
                "scripts.generate_status.SLIDES_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "slides"],
            ),
            patch(
                "scripts.generate_status.TRANSCRIPTS_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "transcripts"],
            ),
            patch(
                "scripts.generate_status.THUMBNAILS_DIRS",
                [project_with_whitepapers / "youtube" / "thumbnails"],
            ),
            patch(
                "scripts.generate_status.VIDEO_DIRS",
                [project_with_whitepapers / "youtube" / "output"],
            ),
            patch("scripts.status_utils.STATUS_FILE", status_file),
            patch("status_utils.STATUS_FILE", status_file),
            patch("scripts.status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
            patch("status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
        ):
            status = generate_status()

        paper = next(p for p in status["papers"] if p["episode"] == "01")
        assert paper.get("uploaded") is True


class TestMain:
    """Tests for main function."""

    def test_prints_summary(self, project_with_whitepapers, capsys):
        """Should print summary of status."""
        from scripts.generate_status import main

        status_file = project_with_whitepapers / "whitepapers" / "status.json"

        with (
            patch(
                "scripts.generate_status.WHITEPAPERS_DIR",
                project_with_whitepapers / "whitepapers",
            ),
            patch("scripts.generate_status.SCRIPT_DIR", project_with_whitepapers),
            patch("scripts.generate_status.YOUTUBE_DIR", project_with_whitepapers / "youtube"),
            patch(
                "scripts.generate_status.ASSETS_DIR", project_with_whitepapers / "youtube" / "pl"
            ),
            patch(
                "scripts.generate_status.ARCHIVE_DIR", project_with_whitepapers / "archive" / "pl"
            ),
            patch(
                "scripts.generate_status.AUDIO_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "audio"],
            ),
            patch(
                "scripts.generate_status.SLIDES_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "slides"],
            ),
            patch(
                "scripts.generate_status.TRANSCRIPTS_DIRS",
                [project_with_whitepapers / "youtube" / "pl" / "transcripts"],
            ),
            patch(
                "scripts.generate_status.THUMBNAILS_DIRS",
                [project_with_whitepapers / "youtube" / "thumbnails"],
            ),
            patch(
                "scripts.generate_status.VIDEO_DIRS",
                [project_with_whitepapers / "youtube" / "output"],
            ),
            patch("scripts.status_utils.STATUS_FILE", status_file),
            patch("status_utils.STATUS_FILE", status_file),
            patch("scripts.status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
            patch("status_utils.WHITEPAPERS_DIR", project_with_whitepapers / "whitepapers"),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Generating status.json" in captured.out
        assert "Total papers:" in captured.out
        assert "Saved to" in captured.out
