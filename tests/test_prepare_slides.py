"""Tests for prepare_slides.py script."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestRunCmd:
    """Tests for run_cmd function."""

    def test_runs_command_and_returns_result(self):
        """Should run command and return CompletedProcess."""
        from scripts.prepare_slides import run_cmd

        result = run_cmd(["echo", "hello"])

        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_raises_on_failure_when_check_true(self):
        """Should raise CalledProcessError when command fails and check=True."""
        from scripts.prepare_slides import run_cmd

        with pytest.raises(subprocess.CalledProcessError):
            run_cmd(["false"], check=True)

    def test_returns_failure_when_check_false(self):
        """Should return non-zero returncode when check=False."""
        from scripts.prepare_slides import run_cmd

        result = run_cmd(["false"], check=False)
        assert result.returncode != 0


class TestGetImageDimensions:
    """Tests for get_image_dimensions function."""

    def test_parses_dimensions_correctly(self):
        """Should parse width and height from identify output."""
        from scripts.prepare_slides import get_image_dimensions

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "1920x1080"

        with patch("scripts.prepare_slides.run_cmd", return_value=mock_result):
            width, height = get_image_dimensions(Path("/fake/image.png"))

        assert width == 1920
        assert height == 1080

    def test_handles_different_dimensions(self):
        """Should handle various dimension formats."""
        from scripts.prepare_slides import get_image_dimensions

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "2867x1600"

        with patch("scripts.prepare_slides.run_cmd", return_value=mock_result):
            width, height = get_image_dimensions(Path("/fake/image.png"))

        assert width == 2867
        assert height == 1600

    def test_raises_on_identify_failure(self):
        """Should raise ValueError when identify fails."""
        from scripts.prepare_slides import get_image_dimensions

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "identify: unable to open image"

        with (
            patch("scripts.prepare_slides.run_cmd", return_value=mock_result),
            pytest.raises(ValueError, match="Cannot get dimensions"),
        ):
            get_image_dimensions(Path("/fake/image.png"))


class TestScaleImage:
    """Tests for scale_image function."""

    def test_calls_convert_with_correct_args(self):
        """Should call ImageMagick convert with proper scaling arguments."""
        from scripts.prepare_slides import scale_image

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("scripts.prepare_slides.run_cmd", return_value=mock_result) as mock_run:
            scale_image(Path("/src.png"), Path("/dst.png"), 1920, 1080)

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "convert"
        assert "/src.png" in cmd
        assert "1920x1080" in cmd
        assert "-colorspace" in cmd
        assert "sRGB" in cmd

    def test_exits_on_convert_failure(self):
        """Should exit with code 1 when convert fails."""
        from scripts.prepare_slides import scale_image

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "convert: unable to write"

        with (
            patch("scripts.prepare_slides.run_cmd", return_value=mock_result),
            pytest.raises(SystemExit) as exc_info,
        ):
            scale_image(Path("/src.png"), Path("/dst.png"), 1920, 1080)

        assert exc_info.value.code == 1


class TestEnsureRgb:
    """Tests for ensure_rgb function."""

    def test_calls_mogrify_with_colorspace(self):
        """Should call mogrify with sRGB colorspace."""
        from scripts.prepare_slides import ensure_rgb

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("scripts.prepare_slides.run_cmd", return_value=mock_result) as mock_run:
            ensure_rgb(Path("/test.png"))

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "mogrify"
        assert "-colorspace" in cmd
        assert "sRGB" in cmd


class TestFindEpisode:
    """Tests for find_episode function."""

    def test_finds_matching_pdf(self, temp_project, sample_pdf_files):
        """Should find PDF file matching episode number."""
        from scripts.prepare_slides import find_episode

        with patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"):
            result = find_episode("01")

        assert result is not None
        assert result.suffix == ".pdf"
        assert "01-attention" in result.stem

    def test_returns_none_for_missing_pdf(self, temp_project, sample_pdf_files):
        """Should return None when no PDF matches."""
        from scripts.prepare_slides import find_episode

        with patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"):
            result = find_episode("99")

        assert result is None


class TestMain:
    """Tests for main function."""

    def test_shows_usage_when_no_args(self, temp_project, sample_pdf_files, capsys):
        """Should show usage and return 1 when no episode provided."""
        from scripts.prepare_slides import main

        with (
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("sys.argv", ["prepare_slides.py"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_lists_available_pdfs(self, temp_project, sample_pdf_files, capsys):
        """Should list available PDF files when no args."""
        from scripts.prepare_slides import main

        with (
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("sys.argv", ["prepare_slides.py"]),
        ):
            main()

        captured = capsys.readouterr()
        assert "Available episodes:" in captured.out
        assert "01-attention-is-all-you-need" in captured.out

    def test_returns_1_when_pdf_not_found(self, temp_project, capsys):
        """Should return 1 when PDF file doesn't exist."""
        from scripts.prepare_slides import main

        with (
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("sys.argv", ["prepare_slides.py", "99"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No PDF file found" in captured.out

    def test_returns_1_when_thumbnail_missing(
        self, temp_project, sample_pdf_files, sample_last_slide, capsys
    ):
        """Should return 1 when thumbnail is missing."""
        from scripts.prepare_slides import main

        with (
            patch("scripts.prepare_slides.SCRIPT_DIR", temp_project),
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.prepare_slides.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"),
            patch("scripts.prepare_slides.LAST_SLIDE", sample_last_slide),
            patch("sys.argv", ["prepare_slides.py", "01"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Thumbnail not found" in captured.out

    def test_returns_1_when_last_slide_missing(
        self, temp_project, sample_pdf_files, sample_thumbnail, capsys
    ):
        """Should return 1 when last-slide.png is missing."""
        from scripts.prepare_slides import main

        missing_last = temp_project / "missing" / "last-slide.png"

        with (
            patch("scripts.prepare_slides.SCRIPT_DIR", temp_project),
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.prepare_slides.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"),
            patch("scripts.prepare_slides.LAST_SLIDE", missing_last),
            patch("sys.argv", ["prepare_slides.py", "01"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Last slide not found" in captured.out

    def test_creates_output_directory(
        self, temp_project, sample_pdf_files, sample_thumbnail, sample_last_slide
    ):
        """Should create output directory for slides."""
        from scripts.prepare_slides import main

        # Mock external commands
        mock_pdftoppm = MagicMock()
        mock_pdftoppm.returncode = 0

        def mock_run_cmd(cmd, check=True):
            result = MagicMock()
            result.returncode = 0
            if cmd[0] == "identify":
                result.stdout = "100x100"
            elif cmd[0] == "pdftoppm":
                # Create fake slide files
                output_dir = (
                    temp_project / "youtube" / "pl" / "slides" / "01-attention-is-all-you-need"
                )
                output_dir.mkdir(exist_ok=True)
                (output_dir / "slide-01.png").write_bytes(b"fake png")
            return result

        with (
            patch("scripts.prepare_slides.SCRIPT_DIR", temp_project),
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.prepare_slides.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"),
            patch("scripts.prepare_slides.LAST_SLIDE", sample_last_slide),
            patch("scripts.prepare_slides.run_cmd", side_effect=mock_run_cmd),
            patch("sys.argv", ["prepare_slides.py", "01"]),
        ):
            main()

        output_dir = temp_project / "youtube" / "pl" / "slides" / "01-attention-is-all-you-need"
        assert output_dir.exists()

    def test_returns_1_when_pdftoppm_fails(
        self, temp_project, sample_pdf_files, sample_thumbnail, sample_last_slide, capsys
    ):
        """Should return 1 when pdftoppm extraction fails."""
        from scripts.prepare_slides import main

        def mock_run_cmd(cmd, check=True):
            result = MagicMock()
            if cmd[0] == "pdftoppm":
                result.returncode = 1
                result.stderr = "pdftoppm: error"
            else:
                result.returncode = 0
                result.stdout = "100x100"
            return result

        with (
            patch("scripts.prepare_slides.SCRIPT_DIR", temp_project),
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.prepare_slides.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"),
            patch("scripts.prepare_slides.LAST_SLIDE", sample_last_slide),
            patch("scripts.prepare_slides.run_cmd", side_effect=mock_run_cmd),
            patch("sys.argv", ["prepare_slides.py", "01"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "pdftoppm failed" in captured.out


class TestFullWorkflow:
    """Integration tests for complete workflow."""

    def test_successful_preparation(
        self, temp_project, sample_pdf_files, sample_thumbnail, sample_last_slide, capsys
    ):
        """Should complete full preparation workflow successfully."""
        from scripts.prepare_slides import main

        output_dir = temp_project / "youtube" / "pl" / "slides" / "01-attention-is-all-you-need"

        def mock_run_cmd(cmd, check=True):
            result = MagicMock()
            result.returncode = 0
            result.stdout = "100x100"
            result.stderr = ""

            if cmd[0] == "pdftoppm":
                # Create fake extracted slides
                output_dir.mkdir(exist_ok=True)
                for i in range(1, 4):
                    (output_dir / f"slide-{i:02d}.png").write_bytes(b"fake png")

            return result

        with (
            patch("scripts.prepare_slides.SCRIPT_DIR", temp_project),
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.prepare_slides.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"),
            patch("scripts.prepare_slides.LAST_SLIDE", sample_last_slide),
            patch("scripts.prepare_slides.run_cmd", side_effect=mock_run_cmd),
            patch("sys.argv", ["prepare_slides.py", "01"]),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Slides prepared successfully" in captured.out
        assert "Extracted 3 slides" in captured.out

    def test_copies_thumbnail_when_dimensions_match(
        self, temp_project, sample_pdf_files, sample_thumbnail, sample_last_slide, capsys
    ):
        """Should copy thumbnail directly when dimensions already match."""
        from scripts.prepare_slides import main

        output_dir = temp_project / "youtube" / "pl" / "slides" / "01-attention-is-all-you-need"

        def mock_run_cmd(cmd, check=True):
            result = MagicMock()
            result.returncode = 0
            result.stdout = "100x100"  # All same dimensions
            result.stderr = ""

            if cmd[0] == "pdftoppm":
                output_dir.mkdir(exist_ok=True)
                (output_dir / "slide-01.png").write_bytes(b"fake png")

            return result

        with (
            patch("scripts.prepare_slides.SCRIPT_DIR", temp_project),
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.prepare_slides.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"),
            patch("scripts.prepare_slides.LAST_SLIDE", sample_last_slide),
            patch("scripts.prepare_slides.run_cmd", side_effect=mock_run_cmd),
            patch("sys.argv", ["prepare_slides.py", "01"]),
        ):
            main()

        captured = capsys.readouterr()
        assert "dimensions already match" in captured.out

    def test_scales_thumbnail_when_dimensions_differ(
        self, temp_project, sample_pdf_files, sample_thumbnail, sample_last_slide, capsys
    ):
        """Should scale thumbnail when dimensions don't match slides."""
        from scripts.prepare_slides import main

        output_dir = temp_project / "youtube" / "pl" / "slides" / "01-attention-is-all-you-need"
        call_count = [0]

        def mock_run_cmd(cmd, check=True):
            result = MagicMock()
            result.returncode = 0
            result.stderr = ""

            if cmd[0] == "pdftoppm":
                output_dir.mkdir(exist_ok=True)
                (output_dir / "slide-01.png").write_bytes(b"fake png")
                result.stdout = ""
            elif cmd[0] == "identify":
                call_count[0] += 1
                # First call for slide, second for thumbnail, third for last-slide, etc.
                if call_count[0] == 1:
                    result.stdout = "1920x1080"  # Slide dimensions
                else:
                    result.stdout = "800x600"  # Different dimensions for thumbnail/last
            else:
                result.stdout = ""

            return result

        with (
            patch("scripts.prepare_slides.SCRIPT_DIR", temp_project),
            patch("scripts.prepare_slides.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.prepare_slides.THUMBNAILS_DIR", temp_project / "youtube" / "thumbnails"),
            patch("scripts.prepare_slides.LAST_SLIDE", sample_last_slide),
            patch("scripts.prepare_slides.run_cmd", side_effect=mock_run_cmd),
            patch("sys.argv", ["prepare_slides.py", "01"]),
        ):
            main()

        captured = capsys.readouterr()
        assert "Scaling from" in captured.out
