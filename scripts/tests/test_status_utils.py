"""Tests for status_utils.py module."""

import json
from unittest.mock import patch

import pytest


@pytest.fixture
def status_file(tmp_path):
    """Create temp status file location."""
    return tmp_path / "whitepapers" / "status.json"


@pytest.fixture
def sample_status():
    """Sample status data."""
    return {
        "papers": [
            {
                "episode": "01",
                "name": "attention-is-all-you-need",
                "category": "llm",
                "notebook_created": True,
                "notebook_url": "https://notebooklm.google.com/notebook/abc123",
                "audio": True,
                "transcript": True,
            },
            {
                "episode": "02",
                "name": "gpt",
                "category": "llm",
                "audio": True,
            },
        ],
        "summary": {"total": 2, "audio": 2, "transcript": 1},
        "updated": "2025-01-01T00:00:00+00:00",
    }


class TestLoadStatus:
    """Tests for load_status function."""

    def test_returns_empty_when_no_file(self, status_file):
        """Should return empty structure when file doesn't exist."""
        from scripts.status_utils import load_status

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            result = load_status()

        assert result == {"papers": [], "summary": {}, "updated": ""}

    def test_loads_existing_file(self, status_file, sample_status):
        """Should load and parse existing status file."""
        from scripts.status_utils import load_status

        status_file.parent.mkdir(parents=True)
        status_file.write_text(json.dumps(sample_status))

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            result = load_status()

        assert result["papers"][0]["episode"] == "01"
        assert len(result["papers"]) == 2


class TestSaveStatus:
    """Tests for save_status function."""

    def test_creates_file_with_timestamp(self, status_file, sample_status):
        """Should create file and update timestamp."""
        from scripts.status_utils import save_status

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            save_status(sample_status)

        assert status_file.exists()
        saved = json.loads(status_file.read_text())
        assert "updated" in saved
        assert saved["updated"] != ""

    def test_creates_parent_directories(self, tmp_path):
        """Should create parent directories if missing."""
        from scripts.status_utils import save_status

        nested_file = tmp_path / "deep" / "nested" / "status.json"

        with patch("scripts.status_utils.STATUS_FILE", nested_file):
            save_status({"papers": [], "summary": {}, "updated": ""})

        assert nested_file.exists()


class TestFindPaperByEpisode:
    """Tests for find_paper_by_episode function."""

    def test_finds_matching_episode(self, sample_status):
        """Should find paper by episode number."""
        from scripts.status_utils import find_paper_by_episode

        result = find_paper_by_episode(sample_status["papers"], "01")

        assert result is not None
        assert result["name"] == "attention-is-all-you-need"

    def test_returns_none_for_missing(self, sample_status):
        """Should return None when episode not found."""
        from scripts.status_utils import find_paper_by_episode

        result = find_paper_by_episode(sample_status["papers"], "99")

        assert result is None

    def test_handles_integer_input(self, sample_status):
        """Should handle integer episode numbers."""
        from scripts.status_utils import find_paper_by_episode

        result = find_paper_by_episode(sample_status["papers"], 1)

        assert result is not None
        assert result["episode"] == "01"


class TestGetEpisodeFromName:
    """Tests for get_episode_from_name function."""

    def test_extracts_episode_number(self):
        """Should extract episode number from filename."""
        from scripts.status_utils import get_episode_from_name

        assert get_episode_from_name("01-attention-is-all-you-need") == "01"
        assert get_episode_from_name("15-glam") == "15"
        assert get_episode_from_name("100-flink") == "100"

    def test_returns_none_for_invalid(self):
        """Should return None for filenames without episode number."""
        from scripts.status_utils import get_episode_from_name

        assert get_episode_from_name("no-number") is None
        assert get_episode_from_name("") is None


class TestUpdateEpisodeStatus:
    """Tests for update_episode_status function."""

    def test_updates_existing_paper(self, status_file, sample_status):
        """Should update field on existing paper."""
        from scripts.status_utils import update_episode_status

        status_file.parent.mkdir(parents=True)
        status_file.write_text(json.dumps(sample_status))

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            update_episode_status("01", "video", True)

        saved = json.loads(status_file.read_text())
        paper = next(p for p in saved["papers"] if p["episode"] == "01")
        assert paper["video"] is True

    def test_creates_new_paper_entry(self, status_file):
        """Should create new paper entry if not found."""
        from scripts.status_utils import update_episode_status

        status_file.parent.mkdir(parents=True)
        status_file.write_text(json.dumps({"papers": [], "summary": {}, "updated": ""}))

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            update_episode_status("05", "audio", True)

        saved = json.loads(status_file.read_text())
        assert len(saved["papers"]) == 1
        assert saved["papers"][0]["episode"] == "05"
        assert saved["papers"][0]["audio"] is True

    def test_updates_summary(self, status_file, sample_status):
        """Should recalculate summary after update."""
        from scripts.status_utils import update_episode_status

        status_file.parent.mkdir(parents=True)
        status_file.write_text(json.dumps(sample_status))

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            update_episode_status("02", "transcript", True)

        saved = json.loads(status_file.read_text())
        assert saved["summary"]["transcript"] == 2


class TestArchiveEpisodeStatus:
    """Tests for archive_episode_status function."""

    def test_sets_archived_clears_pipeline(self, status_file, sample_status):
        """Should set archived and remove pipeline fields."""
        from scripts.status_utils import archive_episode_status

        status_file.parent.mkdir(parents=True)
        status_file.write_text(json.dumps(sample_status))

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            archive_episode_status("01")

        saved = json.loads(status_file.read_text())
        paper = next(p for p in saved["papers"] if p["episode"] == "01")

        assert paper["archived"] is True
        assert "audio" not in paper
        assert "transcript" not in paper
        # PRESERVED_FIELDS are kept after archiving
        assert paper["notebook_created"] is True
        assert paper["notebook_url"] == "https://notebooklm.google.com/notebook/abc123"

    def test_creates_new_archived_entry(self, status_file):
        """Should create archived entry if paper not found."""
        from scripts.status_utils import archive_episode_status

        status_file.parent.mkdir(parents=True)
        status_file.write_text(json.dumps({"papers": [], "summary": {}, "updated": ""}))

        with patch("scripts.status_utils.STATUS_FILE", status_file):
            archive_episode_status("99")

        saved = json.loads(status_file.read_text())
        assert len(saved["papers"]) == 1
        assert saved["papers"][0]["archived"] is True


class TestUpdateSummary:
    """Tests for update_summary function."""

    def test_counts_all_fields(self, sample_status):
        """Should count papers with each field set to True."""
        from scripts.status_utils import update_summary

        update_summary(sample_status)

        assert sample_status["summary"]["total"] == 2
        assert sample_status["summary"]["audio"] == 2
        assert sample_status["summary"]["transcript"] == 1
        assert sample_status["summary"]["notebook_created"] == 1


class TestGetEpisodeNumber:
    """Tests for get_episode_number function."""

    def test_extracts_number(self):
        """Should extract episode number as int."""
        from scripts.status_utils import get_episode_number

        assert get_episode_number("01-attention") == 1
        assert get_episode_number("99-raft") == 99
        assert get_episode_number("101-bitcoin") == 101

    def test_returns_high_value_for_invalid(self):
        """Should return 999999 for non-matching names."""
        from scripts.status_utils import get_episode_number

        assert get_episode_number("no-number") == 999999
        assert get_episode_number("") == 999999


class TestSortByEpisode:
    """Tests for sort_by_episode function."""

    def test_sorts_numerically(self, tmp_path):
        """Should sort paths by episode number, not lexicographically."""
        from scripts.status_utils import sort_by_episode

        paths = [
            tmp_path / "101-bitcoin.m4a",
            tmp_path / "91-cocroachdb.m4a",
            tmp_path / "9-gpt.m4a",
        ]

        result = sort_by_episode(paths)

        assert result[0].stem == "9-gpt"
        assert result[1].stem == "91-cocroachdb"
        assert result[2].stem == "101-bitcoin"

    def test_handles_non_matching_names(self, tmp_path):
        """Should put non-matching names at end."""
        from scripts.status_utils import sort_by_episode

        paths = [
            tmp_path / "no-number.m4a",
            tmp_path / "01-first.m4a",
        ]

        result = sort_by_episode(paths)

        assert result[0].stem == "01-first"
        assert result[1].stem == "no-number"
