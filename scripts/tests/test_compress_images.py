"""Tests for compress_images.py script."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestParseSize:
    """Tests for parse_size function."""

    def test_parses_bytes(self):
        """Should parse plain bytes."""
        from scripts.compress_images import parse_size

        assert parse_size("1024") == 1024
        assert parse_size("1024B") == 1024

    def test_parses_kilobytes(self):
        """Should parse KB values."""
        from scripts.compress_images import parse_size

        assert parse_size("1KB") == 1024
        assert parse_size("2KB") == 2048
        assert parse_size("1.5KB") == 1536

    def test_parses_megabytes(self):
        """Should parse MB values."""
        from scripts.compress_images import parse_size

        assert parse_size("1MB") == 1024**2
        assert parse_size("2MB") == 2 * 1024**2
        assert parse_size("0.5MB") == 512 * 1024

    def test_parses_gigabytes(self):
        """Should parse GB values."""
        from scripts.compress_images import parse_size

        assert parse_size("1GB") == 1024**3

    def test_case_insensitive(self):
        """Should handle case insensitivity."""
        from scripts.compress_images import parse_size

        assert parse_size("1mb") == parse_size("1MB")
        assert parse_size("1kb") == parse_size("1KB")

    def test_raises_on_invalid_format(self):
        """Should raise ValueError on invalid format."""
        from scripts.compress_images import parse_size

        with pytest.raises(ValueError):
            parse_size("invalid")
        with pytest.raises(ValueError):
            parse_size("MB")
        with pytest.raises(ValueError):
            parse_size("1TB")


class TestFormatSize:
    """Tests for format_size function."""

    def test_formats_bytes(self):
        """Should format bytes."""
        from scripts.compress_images import format_size

        assert format_size(512) == "512B"

    def test_formats_kilobytes(self):
        """Should format KB."""
        from scripts.compress_images import format_size

        assert format_size(1024) == "1.0KB"
        assert format_size(1536) == "1.5KB"

    def test_formats_megabytes(self):
        """Should format MB."""
        from scripts.compress_images import format_size

        assert format_size(1024**2) == "1.0MB"
        assert format_size(2 * 1024**2) == "2.0MB"

    def test_formats_gigabytes(self):
        """Should format GB."""
        from scripts.compress_images import format_size

        assert format_size(1024**3) == "1.0GB"


class TestCompressImage:
    """Tests for compress_image function."""

    def test_returns_size_tuple(self, tmp_path):
        """Should return (old_size, new_size) tuple."""
        from scripts.compress_images import compress_image

        img = tmp_path / "test.png"
        img.write_bytes(b"x" * 1000)

        mock_result = MagicMock()
        mock_result.returncode = 0

        def create_smaller_file(_cmd, **_kwargs):
            tmp_file = tmp_path / "test.tmp.png"
            tmp_file.write_bytes(b"x" * 500)
            return mock_result

        with patch("scripts.compress_images.run_cmd", side_effect=create_smaller_file):
            old_size, new_size = compress_image(img, quality=80, colors=256)

        assert old_size == 1000
        assert new_size == 500

    def test_keeps_original_if_larger(self, tmp_path):
        """Should keep original if compressed is larger."""
        from scripts.compress_images import compress_image

        img = tmp_path / "test.png"
        img.write_bytes(b"x" * 1000)

        mock_result = MagicMock()
        mock_result.returncode = 0

        def create_larger_file(_cmd, **_kwargs):
            tmp_file = tmp_path / "test.tmp.png"
            tmp_file.write_bytes(b"x" * 1500)
            return mock_result

        with patch("scripts.compress_images.run_cmd", side_effect=create_larger_file):
            old_size, new_size = compress_image(img, quality=80, colors=256)

        assert old_size == 1000
        assert new_size == 1000  # Kept original size

    def test_raises_on_compression_error(self, tmp_path):
        """Should raise RuntimeError on compression failure."""
        from scripts.compress_images import compress_image

        img = tmp_path / "test.png"
        img.write_bytes(b"x" * 1000)

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "error message"

        with (
            patch("scripts.compress_images.run_cmd", return_value=mock_result),
            pytest.raises(RuntimeError, match="Compression failed"),
        ):
            compress_image(img, quality=80, colors=256)


class TestFindImages:
    """Tests for find_images function."""

    def test_finds_in_directory(self, tmp_path):
        """Should find all PNGs in directory."""
        from scripts.compress_images import find_images

        (tmp_path / "a.png").write_bytes(b"png")
        (tmp_path / "b.png").write_bytes(b"png")
        (tmp_path / "c.jpg").write_bytes(b"jpg")

        images = find_images(tmp_path)

        assert len(images) == 2
        assert all(img.suffix == ".png" for img in images)

    def test_finds_recursive(self, tmp_path):
        """Should find PNGs recursively."""
        from scripts.compress_images import find_images

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "root.png").write_bytes(b"png")
        (subdir / "nested.png").write_bytes(b"png")

        images = find_images(tmp_path)

        assert len(images) == 2

    def test_handles_glob_pattern(self, tmp_path):
        """Should handle glob patterns."""
        from scripts.compress_images import find_images

        (tmp_path / "a.png").write_bytes(b"png")
        (tmp_path / "b.png").write_bytes(b"png")
        (tmp_path / "c.jpg").write_bytes(b"jpg")

        images = find_images(tmp_path / "*.png")

        assert len(images) == 2

    def test_handles_single_file(self, tmp_path):
        """Should handle single file path."""
        from scripts.compress_images import find_images

        img = tmp_path / "test.png"
        img.write_bytes(b"png")

        images = find_images(img)

        assert len(images) == 1
        assert images[0] == img

    def test_returns_empty_for_nonexistent(self, tmp_path):
        """Should return empty list for nonexistent path."""
        from scripts.compress_images import find_images

        images = find_images(tmp_path / "nonexistent")

        assert images == []


class TestMain:
    """Tests for main function."""

    def test_shows_usage_when_no_args(self):
        """Should show usage when missing arguments."""
        from scripts.compress_images import main

        with patch("sys.argv", ["compress_images.py"]), pytest.raises(SystemExit):
            main()

    def test_returns_1_on_invalid_threshold(self, tmp_path, capsys):
        """Should return 1 for invalid threshold format."""
        from scripts.compress_images import main

        with patch("sys.argv", ["compress_images.py", str(tmp_path), "--threshold", "invalid"]):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Invalid size format" in captured.out

    def test_returns_1_when_no_files_found(self, tmp_path, capsys):
        """Should return 1 when no PNG files found."""
        from scripts.compress_images import main

        with patch("sys.argv", ["compress_images.py", str(tmp_path / "nonexistent")]):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No PNG files found" in captured.out

    def test_returns_0_when_no_large_files(self, tmp_path, capsys):
        """Should return 0 when no files exceed threshold."""
        from scripts.compress_images import main

        img = tmp_path / "small.png"
        img.write_bytes(b"x" * 100)

        with patch("sys.argv", ["compress_images.py", str(tmp_path), "--threshold", "1MB"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "No images exceed" in captured.out

    def test_dry_run_makes_no_changes(self, tmp_path, capsys):
        """Should not modify files in dry run mode."""
        from scripts.compress_images import main

        img = tmp_path / "large.png"
        img.write_bytes(b"x" * 3 * 1024 * 1024)
        original_size = img.stat().st_size

        with patch("sys.argv", ["compress_images.py", str(tmp_path), "--threshold", "1MB", "--dry-run"]):
            result = main()

        assert result == 0
        assert img.stat().st_size == original_size
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out

    def test_compresses_large_files(self, tmp_path, capsys):
        """Should compress files exceeding threshold."""
        from scripts.compress_images import main

        img = tmp_path / "large.png"
        img.write_bytes(b"x" * 3 * 1024 * 1024)

        mock_result = MagicMock()
        mock_result.returncode = 0

        def create_smaller_file(cmd, **_kwargs):
            tmp_file = Path(cmd[-1])
            tmp_file.write_bytes(b"x" * 1024 * 1024)
            return mock_result

        with (
            patch("sys.argv", ["compress_images.py", str(tmp_path), "--threshold", "1MB"]),
            patch("scripts.compress_images.run_cmd", side_effect=create_smaller_file),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "smaller" in captured.out

    def test_custom_quality_and_colors(self, tmp_path, capsys):
        """Should pass custom quality and colors to compression."""
        from scripts.compress_images import main

        img = tmp_path / "large.png"
        img.write_bytes(b"x" * 3 * 1024 * 1024)

        mock_result = MagicMock()
        mock_result.returncode = 0

        captured_cmd = []

        def capture_cmd(cmd, **_kwargs):
            captured_cmd.extend(cmd)
            tmp_file = Path(cmd[-1])
            tmp_file.write_bytes(b"x" * 1024 * 1024)
            return mock_result

        with (
            patch(
                "sys.argv",
                [
                    "compress_images.py",
                    str(tmp_path),
                    "--threshold",
                    "1MB",
                    "--quality",
                    "90",
                    "--colors",
                    "128",
                ],
            ),
            patch("scripts.compress_images.run_cmd", side_effect=capture_cmd),
        ):
            main()

        assert "-quality" in captured_cmd
        assert "90" in captured_cmd
        assert "-colors" in captured_cmd
        assert "128" in captured_cmd

    def test_shows_summary(self, tmp_path, capsys):
        """Should show compression summary."""
        from scripts.compress_images import main

        img = tmp_path / "large.png"
        img.write_bytes(b"x" * 3 * 1024 * 1024)

        mock_result = MagicMock()
        mock_result.returncode = 0

        def create_smaller_file(cmd, **_kwargs):
            tmp_file = Path(cmd[-1])
            tmp_file.write_bytes(b"x" * 1024 * 1024)
            return mock_result

        with (
            patch("sys.argv", ["compress_images.py", str(tmp_path), "--threshold", "1MB"]),
            patch("scripts.compress_images.run_cmd", side_effect=create_smaller_file),
        ):
            main()

        captured = capsys.readouterr()
        assert "Compressed" in captured.out
        assert "saved" in captured.out
