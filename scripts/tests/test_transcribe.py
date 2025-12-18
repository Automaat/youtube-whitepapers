"""Tests for transcribe.py script."""

import subprocess
from unittest.mock import MagicMock, patch


class TestTranscribeFile:
    """Tests for transcribe_file function."""

    def test_skips_existing_transcript(self, temp_project, sample_transcript):
        """Should skip transcription when output file already exists."""
        from scripts.transcribe import transcribe_file

        audio_path = temp_project / "youtube" / "pl" / "audio" / "01-attention-is-all-you-need.m4a"
        audio_path.write_bytes(b"fake audio")

        with patch(
            "scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"
        ):
            path, success, msg = transcribe_file(audio_path)

        assert success is True
        assert msg == "skipped (exists)"
        assert path == audio_path

    def test_transcribes_new_file(self, temp_project, sample_audio_files):
        """Should run whisper for new audio file."""
        from scripts.transcribe import transcribe_file

        audio_path = sample_audio_files[0]
        output_dir = temp_project / "youtube" / "pl" / "transcripts"

        mock_run = MagicMock()

        with (
            patch("scripts.transcribe.OUTPUT_DIR", output_dir),
            patch("subprocess.run", mock_run),
        ):
            _path, success, msg = transcribe_file(audio_path)

        assert success is True
        assert msg == "done"
        mock_run.assert_called_once()

        # Verify whisper command
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "whisper"
        assert str(audio_path) in call_args
        assert "--model" in call_args
        assert "--language" in call_args
        assert "--output_format" in call_args
        assert "json" in call_args

    def test_returns_failure_on_whisper_error(self, temp_project, sample_audio_files):
        """Should return failure when whisper command fails."""
        from scripts.transcribe import transcribe_file

        audio_path = sample_audio_files[0]
        output_dir = temp_project / "youtube" / "pl" / "transcripts"

        mock_run = MagicMock(
            side_effect=subprocess.CalledProcessError(1, "whisper", stderr=b"error message")
        )

        with (
            patch("scripts.transcribe.OUTPUT_DIR", output_dir),
            patch("subprocess.run", mock_run),
        ):
            path, success, msg = transcribe_file(audio_path)

        assert success is False
        assert "failed" in msg
        assert path == audio_path


class TestFindAudioFiles:
    """Tests for find_audio_files function."""

    def test_finds_m4a_files(self, temp_project, sample_audio_files):
        """Should find .m4a audio files."""
        from scripts.transcribe import find_audio_files

        with patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"):
            files = find_audio_files()

        assert len(files) == 3
        assert all(f.suffix == ".m4a" for f in files)

    def test_finds_multiple_formats(self, temp_project):
        """Should find mp3 and wav files too."""
        from scripts.transcribe import find_audio_files

        audio_dir = temp_project / "youtube" / "pl" / "audio"
        (audio_dir / "test1.m4a").write_bytes(b"audio")
        (audio_dir / "test2.mp3").write_bytes(b"audio")
        (audio_dir / "test3.wav").write_bytes(b"audio")

        with patch("scripts.transcribe.AUDIO_DIR", audio_dir):
            files = find_audio_files()

        assert len(files) == 3
        extensions = {f.suffix for f in files}
        assert extensions == {".m4a", ".mp3", ".wav"}

    def test_returns_sorted_list(self, temp_project, sample_audio_files):
        """Should return files sorted by name."""
        from scripts.transcribe import find_audio_files

        with patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"):
            files = find_audio_files()

        names = [f.name for f in files]
        assert names == sorted(names)

    def test_returns_empty_for_no_files(self, temp_project):
        """Should return empty list when no audio files exist."""
        from scripts.transcribe import find_audio_files

        with patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"):
            files = find_audio_files()

        assert files == []

    def test_ignores_other_extensions(self, temp_project):
        """Should ignore non-audio files."""
        from scripts.transcribe import find_audio_files

        audio_dir = temp_project / "youtube" / "pl" / "audio"
        (audio_dir / "test.m4a").write_bytes(b"audio")
        (audio_dir / "readme.txt").write_text("not audio")
        (audio_dir / "data.json").write_text("{}")

        with patch("scripts.transcribe.AUDIO_DIR", audio_dir):
            files = find_audio_files()

        assert len(files) == 1
        assert files[0].name == "test.m4a"


class TestMain:
    """Tests for main function."""

    def test_creates_output_directory(self, temp_project, capsys):
        """Should create output directory if it doesn't exist."""
        from scripts.transcribe import main

        output_dir = temp_project / "youtube" / "pl" / "transcripts"
        output_dir.rmdir()  # Remove to test creation
        assert not output_dir.exists()

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", output_dir),
            patch("sys.argv", ["transcribe.py"]),
        ):
            main()

        assert output_dir.exists()

    def test_prints_configuration(self, temp_project, capsys):
        """Should print transcription configuration."""
        from scripts.transcribe import main

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("sys.argv", ["transcribe.py"]),
        ):
            main()

        captured = capsys.readouterr()
        assert "Transcription Script" in captured.out
        assert "Model:" in captured.out
        assert "Language:" in captured.out
        assert "Parallel jobs:" in captured.out

    def test_returns_0_for_no_files(self, temp_project, capsys):
        """Should return 0 when no audio files to process."""
        from scripts.transcribe import main

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("sys.argv", ["transcribe.py"]),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "No audio files to process" in captured.out

    def test_uses_default_parallelism(self, temp_project, sample_audio_files, capsys):
        """Should use default 3 parallel jobs."""
        from scripts.transcribe import main

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("scripts.transcribe.transcribe_file") as mock_transcribe,
            patch("sys.argv", ["transcribe.py"]),
        ):
            mock_transcribe.return_value = (sample_audio_files[0], True, "done")
            main()

        captured = capsys.readouterr()
        assert "Parallel jobs: 3" in captured.out

    def test_accepts_custom_parallelism(self, temp_project, sample_audio_files, capsys):
        """Should accept custom parallel job count from args."""
        from scripts.transcribe import main

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("scripts.transcribe.transcribe_file") as mock_transcribe,
            patch("sys.argv", ["transcribe.py", "5"]),
        ):
            mock_transcribe.return_value = (sample_audio_files[0], True, "done")
            main()

        captured = capsys.readouterr()
        assert "Parallel jobs: 5" in captured.out

    def test_shows_skip_for_existing(
        self, temp_project, sample_audio_files, sample_transcript, capsys
    ):
        """Should show skip message for existing transcripts."""
        from scripts.transcribe import main

        # Rename sample transcript to match first audio file
        transcript_dir = temp_project / "youtube" / "pl" / "transcripts"
        existing = transcript_dir / "01-attention-is-all-you-need.json"
        sample_transcript.rename(existing)

        def mock_transcribe(path):
            if path.stem == "01-attention-is-all-you-need":
                return path, True, "skipped (exists)"
            return path, True, "done"

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", transcript_dir),
            patch("scripts.transcribe.transcribe_file", side_effect=mock_transcribe),
            patch("sys.argv", ["transcribe.py", "1"]),
        ):
            main()

        captured = capsys.readouterr()
        assert "Skip:" in captured.out

    def test_returns_1_on_failures(self, temp_project, sample_audio_files, capsys):
        """Should return 1 when any transcription fails."""
        from scripts.transcribe import main

        def mock_transcribe(path):
            if path.stem == "01-attention-is-all-you-need":
                return path, False, "failed: error"
            return path, True, "done"

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("scripts.transcribe.transcribe_file", side_effect=mock_transcribe),
            patch("sys.argv", ["transcribe.py", "1"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Failed:" in captured.out
        assert "transcription(s) failed" in captured.out

    def test_returns_0_on_all_success(self, temp_project, sample_audio_files, capsys):
        """Should return 0 when all transcriptions succeed."""
        from scripts.transcribe import main

        def mock_transcribe(path):
            return path, True, "done"

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("scripts.transcribe.transcribe_file", side_effect=mock_transcribe),
            patch("sys.argv", ["transcribe.py", "1"]),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "All transcriptions complete!" in captured.out


class TestParallelExecution:
    """Tests for parallel execution behavior."""

    def test_processes_files_in_parallel(self, temp_project, sample_audio_files):
        """Should process multiple files using ThreadPoolExecutor."""
        from scripts.transcribe import main

        processed = []

        def mock_transcribe(path):
            processed.append(path)
            return path, True, "done"

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("scripts.transcribe.transcribe_file", side_effect=mock_transcribe),
            patch("sys.argv", ["transcribe.py", "2"]),
        ):
            main()

        # All 3 files should be processed
        assert len(processed) == 3

    def test_handles_mixed_results(self, temp_project, sample_audio_files, capsys):
        """Should handle mix of success, skip, and failure."""
        from scripts.transcribe import main

        results = {
            "01-attention-is-all-you-need": ("skipped (exists)", True),
            "02-gpt": ("done", True),
            "15-glam": ("failed: error", False),
        }

        def mock_transcribe(path):
            msg, success = results[path.stem]
            return path, success, msg

        with (
            patch("scripts.transcribe.AUDIO_DIR", temp_project / "youtube" / "pl" / "audio"),
            patch("scripts.transcribe.OUTPUT_DIR", temp_project / "youtube" / "pl" / "transcripts"),
            patch("scripts.transcribe.transcribe_file", side_effect=mock_transcribe),
            patch("sys.argv", ["transcribe.py", "1"]),
        ):
            result = main()

        assert result == 1  # One failure
        captured = capsys.readouterr()
        assert "Skip:" in captured.out
        assert "Done:" in captured.out
        assert "Failed:" in captured.out
