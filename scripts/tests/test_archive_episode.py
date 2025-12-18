"""Tests for archive_episode.py script."""

from unittest.mock import patch

import pytest


@pytest.fixture
def full_episode_files(temp_project, sample_audio_files, sample_transcript, sample_thumbnail):
    """Create complete set of episode files for archiving."""
    ep_name = "01-attention-is-all-you-need"

    # Slides directory with files
    slides_dir = temp_project / "youtube" / "pl" / "slides" / ep_name
    slides_dir.mkdir(parents=True, exist_ok=True)
    (slides_dir / "slide-01.png").write_bytes(b"fake slide")
    (slides_dir / "slide-02.png").write_bytes(b"fake slide")
    (slides_dir / "thumbnail.png").write_bytes(b"fake thumb")
    (slides_dir / "last-slide.png").write_bytes(b"fake last")

    # Video output
    output_dir = temp_project / "youtube" / "output"
    (output_dir / f"{ep_name}.mp4").write_bytes(b"fake video")
    (output_dir / f"{ep_name}-metadata.txt").write_text("TYTUŁ: Test")

    # Optimized thumbnail variant
    thumbnails_dir = temp_project / "youtube" / "thumbnails"
    (thumbnails_dir / f"{ep_name}-optimized.png").write_bytes(b"fake optimized")

    # Create archive directory structure
    archive_dir = temp_project / "archive" / "pl"
    (archive_dir / "audio").mkdir(parents=True, exist_ok=True)
    (archive_dir / "slides").mkdir(parents=True, exist_ok=True)
    (archive_dir / "transcripts").mkdir(parents=True, exist_ok=True)
    (archive_dir / "video").mkdir(parents=True, exist_ok=True)
    (archive_dir / "metadata").mkdir(parents=True, exist_ok=True)
    (archive_dir / "thumbnails").mkdir(parents=True, exist_ok=True)

    return ep_name


class TestFindEpisode:
    """Tests for find_episode function."""

    def test_finds_matching_audio(self, temp_project, sample_audio_files):
        """Should find episode name from audio file."""
        from scripts.archive_episode import find_episode

        with patch("scripts.archive_episode.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"):
            result = find_episode("01")

        assert result == "01-attention-is-all-you-need"

    def test_returns_none_for_missing_episode(self, temp_project, sample_audio_files):
        """Should return None when no audio matches."""
        from scripts.archive_episode import find_episode

        with patch("scripts.archive_episode.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"):
            result = find_episode("99")

        assert result is None


class TestMoveFile:
    """Tests for move_file function."""

    def test_moves_existing_file(self, tmp_path):
        """Should move file to destination and return True."""
        from scripts.archive_episode import move_file

        src = tmp_path / "source" / "test.txt"
        src.parent.mkdir()
        src.write_text("content")
        dst_dir = tmp_path / "dest"

        result = move_file(src, dst_dir, "Test")

        assert result is True
        assert not src.exists()
        assert (dst_dir / "test.txt").exists()

    def test_returns_false_for_missing_file(self, tmp_path, capsys):
        """Should return False and warn when file doesn't exist."""
        from scripts.archive_episode import move_file

        src = tmp_path / "nonexistent.txt"
        dst_dir = tmp_path / "dest"

        result = move_file(src, dst_dir, "Test")

        assert result is False
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_replaces_existing_file(self, tmp_path, capsys):
        """Should replace existing file in archive."""
        from scripts.archive_episode import move_file

        src = tmp_path / "source" / "test.txt"
        src.parent.mkdir()
        src.write_text("new content")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        (dst_dir / "test.txt").write_text("old content")

        result = move_file(src, dst_dir, "Test")

        assert result is True
        assert not src.exists()
        assert (dst_dir / "test.txt").read_text() == "new content"
        captured = capsys.readouterr()
        assert "replaced" in captured.out


class TestMoveDirectory:
    """Tests for move_directory function."""

    def test_moves_directory_with_contents(self, tmp_path, capsys):
        """Should move entire directory and report file count."""
        from scripts.archive_episode import move_directory

        src = tmp_path / "source" / "episode"
        src.mkdir(parents=True)
        (src / "file1.png").write_bytes(b"data")
        (src / "file2.png").write_bytes(b"data")
        dst_dir = tmp_path / "dest"

        result = move_directory(src, dst_dir, "Slides")

        assert result is True
        assert not src.exists()
        assert (dst_dir / "episode").exists()
        assert (dst_dir / "episode" / "file1.png").exists()
        captured = capsys.readouterr()
        assert "2 files" in captured.out

    def test_returns_false_for_missing_directory(self, tmp_path, capsys):
        """Should return False when directory doesn't exist."""
        from scripts.archive_episode import move_directory

        src = tmp_path / "nonexistent"
        dst_dir = tmp_path / "dest"

        result = move_directory(src, dst_dir, "Slides")

        assert result is False
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_replaces_existing_directory(self, tmp_path, capsys):
        """Should replace existing directory in archive."""
        from scripts.archive_episode import move_directory

        src = tmp_path / "source" / "episode"
        src.mkdir(parents=True)
        (src / "new.png").write_bytes(b"new")

        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        existing = dst_dir / "episode"
        existing.mkdir()
        (existing / "old.png").write_bytes(b"old")

        result = move_directory(src, dst_dir, "Slides")

        assert result is True
        assert not src.exists()
        assert (dst_dir / "episode" / "new.png").exists()
        assert not (dst_dir / "episode" / "old.png").exists()
        captured = capsys.readouterr()
        assert "replaced" in captured.out


class TestMain:
    """Tests for main function integration."""

    def test_shows_usage_when_no_args(self, temp_project, sample_audio_files, capsys):
        """Should show usage and return 1 when no episode provided."""
        from scripts.archive_episode import main

        with (
            patch("scripts.archive_episode.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("sys.argv", ["archive_episode.py"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out
        assert "Available episodes:" in captured.out

    def test_returns_1_when_episode_not_found(self, temp_project, capsys):
        """Should return 1 when audio file doesn't exist."""
        from scripts.archive_episode import main

        with (
            patch("scripts.archive_episode.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("sys.argv", ["archive_episode.py", "99"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No audio file found" in captured.out

    def test_archives_all_files_successfully(self, temp_project, full_episode_files, capsys):
        """Should move all episode files to archive."""
        from scripts.archive_episode import main

        ep_name = full_episode_files
        archive_dir = temp_project / "archive" / "pl"

        with (
            patch("scripts.archive_episode.SCRIPT_DIR", temp_project),
            patch("scripts.archive_episode.YOUTUBE_DIR", temp_project / "youtube"),
            patch("scripts.archive_episode.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.archive_episode.ARCHIVE_DIR", archive_dir),
            patch("scripts.archive_episode.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.archive_episode.SLIDES_DIR", temp_project / "youtube" / "pl" / "slides"),
            patch(
                "scripts.archive_episode.TRANSCRIPTS_DIR",
                temp_project / "youtube" / "pl" / "transcripts",
            ),
            patch("scripts.archive_episode.OUTPUT_DIR", temp_project / "youtube" / "output"),
            patch(
                "scripts.archive_episode.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"
            ),
            patch("scripts.archive_episode.ARCHIVE_AUDIO", archive_dir / "audio"),
            patch("scripts.archive_episode.ARCHIVE_SLIDES", archive_dir / "slides"),
            patch("scripts.archive_episode.ARCHIVE_TRANSCRIPTS", archive_dir / "transcripts"),
            patch("scripts.archive_episode.ARCHIVE_VIDEO", archive_dir / "video"),
            patch("scripts.archive_episode.ARCHIVE_METADATA", archive_dir / "metadata"),
            patch("scripts.archive_episode.ARCHIVE_THUMBNAILS", archive_dir / "thumbnails"),
            patch("sys.argv", ["archive_episode.py", "01"]),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Archiving episode:" in captured.out
        assert "successfully" in captured.out

        # Verify files moved
        assert (archive_dir / "audio" / f"{ep_name}.m4a").exists()
        assert (archive_dir / "slides" / ep_name).exists()
        assert (archive_dir / "transcripts" / f"{ep_name}.json").exists()
        assert (archive_dir / "video" / f"{ep_name}.mp4").exists()
        assert (archive_dir / "metadata" / f"{ep_name}-metadata.txt").exists()
        assert (archive_dir / "thumbnails" / f"{ep_name}.png").exists()
        assert (archive_dir / "thumbnails" / f"{ep_name}-optimized.png").exists()

    def test_continues_with_missing_optional_files(self, temp_project, sample_audio_files, capsys):
        """Should warn but continue when some files missing."""
        from scripts.archive_episode import main

        archive_dir = temp_project / "archive" / "pl"

        with (
            patch("scripts.archive_episode.SCRIPT_DIR", temp_project),
            patch("scripts.archive_episode.YOUTUBE_DIR", temp_project / "youtube"),
            patch("scripts.archive_episode.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.archive_episode.ARCHIVE_DIR", archive_dir),
            patch("scripts.archive_episode.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.archive_episode.SLIDES_DIR", temp_project / "youtube" / "pl" / "slides"),
            patch(
                "scripts.archive_episode.TRANSCRIPTS_DIR",
                temp_project / "youtube" / "pl" / "transcripts",
            ),
            patch("scripts.archive_episode.OUTPUT_DIR", temp_project / "youtube" / "output"),
            patch(
                "scripts.archive_episode.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"
            ),
            patch("scripts.archive_episode.ARCHIVE_AUDIO", archive_dir / "audio"),
            patch("scripts.archive_episode.ARCHIVE_SLIDES", archive_dir / "slides"),
            patch("scripts.archive_episode.ARCHIVE_TRANSCRIPTS", archive_dir / "transcripts"),
            patch("scripts.archive_episode.ARCHIVE_VIDEO", archive_dir / "video"),
            patch("scripts.archive_episode.ARCHIVE_METADATA", archive_dir / "metadata"),
            patch("scripts.archive_episode.ARCHIVE_THUMBNAILS", archive_dir / "thumbnails"),
            patch("sys.argv", ["archive_episode.py", "01"]),
        ):
            result = main()

        # Should succeed with partial archive (audio exists)
        assert result == 0
        captured = capsys.readouterr()
        assert "not found" in captured.out  # Warnings for missing files
        assert (archive_dir / "audio" / "01-attention-is-all-you-need.m4a").exists()

    def test_replaces_existing_archived_files(self, temp_project, capsys):
        """Should replace files that already exist in archive."""
        from scripts.archive_episode import main

        # Create audio file and existing archive
        audio_dir = temp_project / "youtube" / "pl" / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        (audio_dir / "01-test.m4a").write_bytes(b"new audio")

        archive_dir = temp_project / "archive" / "pl"
        archive_audio = archive_dir / "audio"
        archive_audio.mkdir(parents=True, exist_ok=True)
        (archive_audio / "01-test.m4a").write_bytes(b"old audio")

        with (
            patch("scripts.archive_episode.SCRIPT_DIR", temp_project),
            patch("scripts.archive_episode.YOUTUBE_DIR", temp_project / "youtube"),
            patch("scripts.archive_episode.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.archive_episode.ARCHIVE_DIR", archive_dir),
            patch("scripts.archive_episode.AUDIO_DIR", audio_dir),
            patch("scripts.archive_episode.SLIDES_DIR", temp_project / "youtube" / "pl" / "slides"),
            patch(
                "scripts.archive_episode.TRANSCRIPTS_DIR",
                temp_project / "youtube" / "pl" / "transcripts",
            ),
            patch("scripts.archive_episode.OUTPUT_DIR", temp_project / "youtube" / "output"),
            patch(
                "scripts.archive_episode.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"
            ),
            patch("scripts.archive_episode.ARCHIVE_AUDIO", archive_audio),
            patch("scripts.archive_episode.ARCHIVE_SLIDES", archive_dir / "slides"),
            patch("scripts.archive_episode.ARCHIVE_TRANSCRIPTS", archive_dir / "transcripts"),
            patch("scripts.archive_episode.ARCHIVE_VIDEO", archive_dir / "video"),
            patch("scripts.archive_episode.ARCHIVE_METADATA", archive_dir / "metadata"),
            patch("scripts.archive_episode.ARCHIVE_THUMBNAILS", archive_dir / "thumbnails"),
            patch("sys.argv", ["archive_episode.py", "01"]),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "replaced" in captured.out
        assert (archive_audio / "01-test.m4a").read_bytes() == b"new audio"
