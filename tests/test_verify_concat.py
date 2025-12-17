"""Tests for verify_concat.py script."""

from pathlib import Path
from unittest.mock import patch

import pytest


class TestRunCmd:
    """Tests for run_cmd function."""

    def test_returns_stdout(self):
        """Should return command stdout."""
        from scripts.verify_concat import run_cmd

        result = run_cmd(["echo", "hello"])
        assert result == "hello"


class TestGetAudioDuration:
    """Tests for get_audio_duration function."""

    def test_parses_duration(self):
        """Should parse ffprobe output."""
        from scripts.verify_concat import get_audio_duration

        with patch("scripts.verify_concat.run_cmd", return_value="125.5"):
            duration = get_audio_duration(Path("/fake/audio.m4a"))

        assert duration == 125.5


class TestGetImageDimensions:
    """Tests for get_image_dimensions function."""

    def test_parses_dimensions(self):
        """Should parse identify output."""
        from scripts.verify_concat import get_image_dimensions

        with patch("scripts.verify_concat.run_cmd", return_value="1920x1080"):
            width, height = get_image_dimensions(Path("/fake/image.png"))

        assert width == 1920
        assert height == 1080


class TestParseConcat:
    """Tests for parse_concat function."""

    def test_parses_entries(self, tmp_path):
        """Should parse file/duration pairs."""
        from scripts.verify_concat import parse_concat

        concat = tmp_path / "concat.txt"
        concat.write_text(
            "file '/path/to/slide1.png'\n"
            "duration 10\n"
            "file '/path/to/slide2.png'\n"
            "duration 20\n"
        )

        entries = parse_concat(concat)

        assert len(entries) == 2
        assert entries[0].file_path == Path("/path/to/slide1.png")
        assert entries[0].duration == 10.0
        assert entries[1].file_path == Path("/path/to/slide2.png")
        assert entries[1].duration == 20.0

    def test_handles_decimal_duration(self, tmp_path):
        """Should parse decimal durations."""
        from scripts.verify_concat import parse_concat

        concat = tmp_path / "concat.txt"
        concat.write_text("file '/path/slide.png'\nduration 152.71\n")

        entries = parse_concat(concat)

        assert entries[0].duration == 152.71

    def test_handles_final_file_without_duration(self, tmp_path):
        """Should handle last file without duration."""
        from scripts.verify_concat import parse_concat

        concat = tmp_path / "concat.txt"
        concat.write_text(
            "file '/path/slide1.png'\nduration 10\n" "file '/path/last-slide.png'\n"
        )

        entries = parse_concat(concat)

        assert len(entries) == 2
        assert entries[1].duration == 0.0

    def test_handles_empty_lines(self, tmp_path):
        """Should skip empty lines."""
        from scripts.verify_concat import parse_concat

        concat = tmp_path / "concat.txt"
        concat.write_text(
            "\nfile '/path/slide.png'\n\nduration 10\n\n"
        )

        entries = parse_concat(concat)

        assert len(entries) == 1


class TestFindEpisodeAudio:
    """Tests for find_episode_audio function."""

    def test_returns_none_when_not_found(self, tmp_path):
        """Should return None when audio not found."""
        from scripts.verify_concat import find_episode_audio

        with patch("scripts.verify_concat.ASSETS_DIR", tmp_path):
            (tmp_path / "audio").mkdir()
            result = find_episode_audio("99")

        assert result is None

    def test_finds_matching_audio(self, tmp_path):
        """Should find audio file by episode number."""
        from scripts.verify_concat import find_episode_audio

        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()
        audio_file = audio_dir / "28-emergent-abilities.m4a"
        audio_file.write_bytes(b"audio")

        with patch("scripts.verify_concat.ASSETS_DIR", tmp_path):
            result = find_episode_audio("28")

        assert result == audio_file


class TestVerifyFilesExist:
    """Tests for verify_files_exist function."""

    def test_returns_empty_when_all_exist(self, tmp_path):
        """Should return empty list when all files exist."""
        from scripts.verify_concat import ConcatEntry, verify_files_exist

        slide = tmp_path / "slide.png"
        slide.write_bytes(b"png")

        entries = [ConcatEntry(slide, 10.0, 1)]
        errors = verify_files_exist(entries)

        assert errors == []

    def test_returns_error_for_missing_file(self, tmp_path):
        """Should return error for missing files."""
        from scripts.verify_concat import ConcatEntry, verify_files_exist

        entries = [ConcatEntry(tmp_path / "missing.png", 10.0, 1)]
        errors = verify_files_exist(entries)

        assert len(errors) == 1
        assert "File not found" in errors[0]


class TestVerifyDimensions:
    """Tests for verify_dimensions function."""

    def test_returns_empty_when_consistent(self, tmp_path):
        """Should return empty when all dimensions match."""
        from scripts.verify_concat import ConcatEntry, verify_dimensions

        slide1 = tmp_path / "slide1.png"
        slide2 = tmp_path / "slide2.png"
        slide1.write_bytes(b"png")
        slide2.write_bytes(b"png")

        entries = [
            ConcatEntry(slide1, 10.0, 1),
            ConcatEntry(slide2, 20.0, 3),
        ]

        with patch("scripts.verify_concat.get_image_dimensions", return_value=(1920, 1080)):
            errors = verify_dimensions(entries)

        assert errors == []

    def test_returns_error_for_inconsistent_dims(self, tmp_path):
        """Should return error when dimensions differ."""
        from scripts.verify_concat import ConcatEntry, verify_dimensions

        slide1 = tmp_path / "slide1.png"
        slide2 = tmp_path / "slide2.png"
        slide1.write_bytes(b"png")
        slide2.write_bytes(b"png")

        entries = [
            ConcatEntry(slide1, 10.0, 1),
            ConcatEntry(slide2, 20.0, 3),
        ]

        dims = {str(slide1): (1920, 1080), str(slide2): (2867, 1600)}

        def mock_dims(path):
            return dims[str(path)]

        with patch("scripts.verify_concat.get_image_dimensions", side_effect=mock_dims):
            errors = verify_dimensions(entries)

        assert len(errors) > 0
        assert "Inconsistent" in errors[0]


class TestVerifyDuration:
    """Tests for verify_duration function."""

    def test_passes_when_duration_matches(self, tmp_path):
        """Should pass when duration matches expected."""
        from scripts.verify_concat import ConcatEntry, verify_duration

        entries = [
            ConcatEntry(tmp_path / "slide.png", 100.0, 1),
            ConcatEntry(tmp_path / "outro.png", 5.0, 3),
        ]

        with patch("scripts.verify_concat.get_audio_duration", return_value=100.0):
            ok, messages = verify_duration(entries, tmp_path / "audio.m4a")

        assert ok is True
        assert any("Duration OK" in m for m in messages)

    def test_fails_when_duration_mismatch(self, tmp_path):
        """Should fail when duration differs too much."""
        from scripts.verify_concat import ConcatEntry, verify_duration

        entries = [
            ConcatEntry(tmp_path / "slide.png", 90.0, 1),  # Too short
        ]

        with patch("scripts.verify_concat.get_audio_duration", return_value=100.0):
            ok, messages = verify_duration(entries, tmp_path / "audio.m4a")

        assert ok is False
        assert any("mismatch" in m for m in messages)

    def test_uses_tolerance(self, tmp_path):
        """Should use tolerance for comparison."""
        from scripts.verify_concat import ConcatEntry, verify_duration

        entries = [
            ConcatEntry(tmp_path / "slide.png", 100.0, 1),
            ConcatEntry(tmp_path / "outro.png", 5.3, 3),  # Slightly over
        ]

        with patch("scripts.verify_concat.get_audio_duration", return_value=100.0):
            ok, _messages = verify_duration(entries, tmp_path / "audio.m4a", tolerance=0.5)

        assert ok is True


class TestVerifyStructure:
    """Tests for verify_structure function."""

    def test_returns_empty_for_correct_structure(self, tmp_path):
        """Should return empty for correct structure."""
        from scripts.verify_concat import ConcatEntry, verify_structure

        entries = [
            ConcatEntry(tmp_path / "thumbnail.png", 5.0, 1),
            ConcatEntry(tmp_path / "slide-01.png", 60.0, 3),
            ConcatEntry(tmp_path / "last-slide.png", 5.0, 5),
        ]

        errors = verify_structure(entries)

        assert errors == []

    def test_warns_missing_thumbnail(self, tmp_path):
        """Should warn when thumbnail not first."""
        from scripts.verify_concat import ConcatEntry, verify_structure

        entries = [
            ConcatEntry(tmp_path / "slide-01.png", 60.0, 1),
            ConcatEntry(tmp_path / "last-slide.png", 5.0, 3),
        ]

        errors = verify_structure(entries)

        assert any("thumbnail" in e.lower() for e in errors)

    def test_warns_missing_last_slide(self, tmp_path):
        """Should warn when last-slide not last."""
        from scripts.verify_concat import ConcatEntry, verify_structure

        entries = [
            ConcatEntry(tmp_path / "thumbnail.png", 5.0, 1),
            ConcatEntry(tmp_path / "slide-01.png", 60.0, 3),
        ]

        errors = verify_structure(entries)

        assert any("last-slide" in e.lower() for e in errors)

    def test_warns_very_short_duration(self, tmp_path):
        """Should warn for durations < 3s."""
        from scripts.verify_concat import ConcatEntry, verify_structure

        entries = [
            ConcatEntry(tmp_path / "thumbnail.png", 5.0, 1),
            ConcatEntry(tmp_path / "slide-01.png", 2.0, 3),  # Too short
            ConcatEntry(tmp_path / "last-slide.png", 5.0, 5),
        ]

        errors = verify_structure(entries)

        assert any("short" in e.lower() for e in errors)

    def test_warns_very_long_duration(self, tmp_path):
        """Should warn for durations > 180s."""
        from scripts.verify_concat import ConcatEntry, verify_structure

        entries = [
            ConcatEntry(tmp_path / "thumbnail.png", 5.0, 1),
            ConcatEntry(tmp_path / "slide-01.png", 200.0, 3),  # Too long
            ConcatEntry(tmp_path / "last-slide.png", 5.0, 5),
        ]

        errors = verify_structure(entries)

        assert any("long" in e.lower() for e in errors)


class TestMain:
    """Tests for main function."""

    def test_returns_1_when_no_args(self):
        """Should return error when missing arguments."""
        from scripts.verify_concat import main

        with patch("sys.argv", ["verify_concat.py"]), pytest.raises(SystemExit):
            main()

    def test_returns_1_when_slides_not_found(self, capsys):
        """Should return 1 when slides directory not found."""
        from scripts.verify_concat import main

        with (
            patch("sys.argv", ["verify_concat.py", "99"]),
            patch("scripts.verify_concat.ASSETS_DIR", Path("/nonexistent")),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No slides directory found" in captured.out

    def test_returns_1_when_concat_not_found(self, tmp_path, capsys):
        """Should return 1 when concat.txt not found."""
        from scripts.verify_concat import main

        slides_dir = tmp_path / "slides" / "28-test"
        slides_dir.mkdir(parents=True)

        with (
            patch("sys.argv", ["verify_concat.py", "28"]),
            patch("scripts.verify_concat.ASSETS_DIR", tmp_path),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "concat.txt not found" in captured.out

    def test_returns_1_when_audio_not_found(self, tmp_path, capsys):
        """Should return 1 when audio not found."""
        from scripts.verify_concat import main

        slides_dir = tmp_path / "slides" / "28-test"
        slides_dir.mkdir(parents=True)
        concat = slides_dir / "concat.txt"
        concat.write_text("file 'slide.png'\nduration 10\n")

        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()

        with (
            patch("sys.argv", ["verify_concat.py", "28"]),
            patch("scripts.verify_concat.ASSETS_DIR", tmp_path),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No audio file found" in captured.out

    def test_returns_0_when_valid(self, tmp_path, capsys):
        """Should return 0 when concat is valid."""
        from scripts.verify_concat import main

        slides_dir = tmp_path / "slides" / "28-test"
        slides_dir.mkdir(parents=True)

        thumbnail = slides_dir / "thumbnail.png"
        slide = slides_dir / "slide-01.png"
        last_slide = slides_dir / "last-slide.png"
        thumbnail.write_bytes(b"png")
        slide.write_bytes(b"png")
        last_slide.write_bytes(b"png")

        concat = slides_dir / "concat.txt"
        concat.write_text(
            f"file '{thumbnail}'\nduration 5\n"
            f"file '{slide}'\nduration 95\n"
            f"file '{last_slide}'\nduration 5\n"
        )

        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()
        audio = audio_dir / "28-test.m4a"
        audio.write_bytes(b"audio")

        with (
            patch("sys.argv", ["verify_concat.py", "28"]),
            patch("scripts.verify_concat.ASSETS_DIR", tmp_path),
            patch("scripts.verify_concat.get_audio_duration", return_value=100.0),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "verification passed" in captured.out

    def test_returns_1_when_duration_mismatch(self, tmp_path, capsys):
        """Should return 1 when duration doesn't match."""
        from scripts.verify_concat import main

        slides_dir = tmp_path / "slides" / "28-test"
        slides_dir.mkdir(parents=True)

        thumbnail = slides_dir / "thumbnail.png"
        last_slide = slides_dir / "last-slide.png"
        thumbnail.write_bytes(b"png")
        last_slide.write_bytes(b"png")

        concat = slides_dir / "concat.txt"
        concat.write_text(
            f"file '{thumbnail}'\nduration 5\n"
            f"file '{last_slide}'\nduration 5\n"  # Only 10s total, not 105
        )

        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()
        audio = audio_dir / "28-test.m4a"
        audio.write_bytes(b"audio")

        with (
            patch("sys.argv", ["verify_concat.py", "28"]),
            patch("scripts.verify_concat.ASSETS_DIR", tmp_path),
            patch("scripts.verify_concat.get_audio_duration", return_value=100.0),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "FAILED" in captured.out
