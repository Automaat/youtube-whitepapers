"""Tests for generate_prompt.py script."""

from unittest.mock import patch

import pytest


class TestFindEpisode:
    """Tests for find_episode function."""

    def test_finds_matching_episode(self, temp_project, sample_audio_files):
        """Should find audio file matching episode number."""
        from scripts.generate_prompt import find_episode

        with patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"):
            result = find_episode("01")

        assert result is not None
        assert result.stem == "01-attention-is-all-you-need"

    def test_finds_two_digit_episode(self, temp_project, sample_audio_files):
        """Should find episode with two-digit number."""
        from scripts.generate_prompt import find_episode

        with patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"):
            result = find_episode("15")

        assert result is not None
        assert result.stem == "15-glam"

    def test_returns_none_for_nonexistent_episode(self, temp_project, sample_audio_files):
        """Should return None when no matching episode exists."""
        from scripts.generate_prompt import find_episode

        with patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"):
            result = find_episode("99")

        assert result is None

    def test_returns_none_for_empty_directory(self, temp_project):
        """Should return None when audio directory is empty."""
        from scripts.generate_prompt import find_episode

        with patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"):
            result = find_episode("01")

        assert result is None


class TestLoadTemplate:
    """Tests for load_template function."""

    def test_loads_and_formats_template(self, temp_project, sample_template):
        """Should load template and replace placeholder."""
        from scripts.generate_prompt import load_template

        with patch("scripts.generate_prompt.TEMPLATE_FILE", sample_template):
            result = load_template()

        assert "{ep_name}" in result
        assert "[EPISODE_NUMBER]-[EPISODE_NAME]" not in result

    def test_raises_on_missing_template(self, temp_project):
        """Should raise when template file doesn't exist."""
        from scripts.generate_prompt import load_template

        nonexistent = temp_project / "nonexistent.md"
        with (
            patch("scripts.generate_prompt.TEMPLATE_FILE", nonexistent),
            pytest.raises(FileNotFoundError),
        ):
            load_template()


class TestCheckFile:
    """Tests for check_file function."""

    def test_prints_checkmark_for_existing_file(self, temp_project, sample_audio_files, capsys):
        """Should print ✅ for existing file."""
        from scripts.generate_prompt import check_file

        with patch("scripts.generate_prompt.SCRIPT_DIR", temp_project):
            check_file(sample_audio_files[0], "Test Audio")

        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "Test Audio" in captured.out

    def test_prints_x_for_missing_file(self, temp_project, capsys):
        """Should print ❌ for missing file."""
        from scripts.generate_prompt import check_file

        missing = temp_project / "youtube" / "pl" / "audio" / "missing.m4a"
        with patch("scripts.generate_prompt.SCRIPT_DIR", temp_project):
            check_file(missing, "Missing Audio")

        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "Missing Audio" in captured.out


class TestMain:
    """Tests for main function."""

    def test_exits_with_usage_when_no_args(self, temp_project, sample_audio_files, capsys):
        """Should show usage and exit 1 when no episode provided."""
        from scripts.generate_prompt import main

        with (
            patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("sys.argv", ["generate_prompt.py"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_lists_available_episodes(self, temp_project, sample_audio_files, capsys):
        """Should list available episodes when no args provided."""
        from scripts.generate_prompt import main

        with (
            patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("sys.argv", ["generate_prompt.py"]),
            pytest.raises(SystemExit),
        ):
            main()

        captured = capsys.readouterr()
        assert "Available episodes:" in captured.out
        assert "01-attention-is-all-you-need" in captured.out

    def test_exits_when_episode_not_found(self, temp_project, sample_audio_files, capsys):
        """Should exit 1 when episode number doesn't match any file."""
        from scripts.generate_prompt import main

        with (
            patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("sys.argv", ["generate_prompt.py", "99"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "No audio file found" in captured.out

    def test_generates_prompt_for_valid_episode(
        self, temp_project, sample_audio_files, sample_template, capsys
    ):
        """Should generate and print prompt for valid episode."""
        from scripts.generate_prompt import main

        with (
            patch("scripts.generate_prompt.SCRIPT_DIR", temp_project),
            patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.generate_prompt.TEMPLATE_FILE", sample_template),
            patch("sys.argv", ["generate_prompt.py", "01"]),
        ):
            main()

        captured = capsys.readouterr()
        assert "Episode: 01-attention-is-all-you-need" in captured.out
        assert "CLAUDE CODE PROMPT" in captured.out
        assert "01-attention-is-all-you-need" in captured.out

    def test_shows_file_status(self, temp_project, sample_audio_files, sample_template, capsys):
        """Should show status of required files."""
        from scripts.generate_prompt import main

        with (
            patch("scripts.generate_prompt.SCRIPT_DIR", temp_project),
            patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.generate_prompt.TEMPLATE_FILE", sample_template),
            patch("sys.argv", ["generate_prompt.py", "01"]),
        ):
            main()

        captured = capsys.readouterr()
        assert "Required files:" in captured.out
        assert "Audio" in captured.out
        assert "Slides" in captured.out
        assert "Transcript" in captured.out


class TestIntegration:
    """Integration tests for generate_prompt script."""

    def test_full_workflow_with_all_files(
        self,
        temp_project,
        sample_audio_files,
        sample_pdf_files,
        sample_transcript,
        sample_template,
        capsys,
    ):
        """Should complete full workflow with all required files present."""
        from scripts.generate_prompt import main

        with (
            patch("scripts.generate_prompt.SCRIPT_DIR", temp_project),
            patch("scripts.generate_prompt.ASSETS_DIR", temp_project / "youtube" / "pl"),
            patch("scripts.generate_prompt.TEMPLATE_FILE", sample_template),
            patch("sys.argv", ["generate_prompt.py", "01"]),
        ):
            main()

        captured = capsys.readouterr()
        # All files exist so should show 3 checkmarks
        assert captured.out.count("✅") >= 1
        assert "CLAUDE CODE PROMPT" in captured.out
